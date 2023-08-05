#!/usr/bin/env python
"""
Python debugger prompt.
Enhanced version of Pdb, using a prompt-toolkit front-end.

Usage::

    from prompt_toolkit.contrib.pdb import set_trace
    set_trace()
"""
from __future__ import unicode_literals, absolute_import
from pygments.lexers import PythonLexer

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.contrib.regular_languages.validation import GrammarValidator
from prompt_toolkit.document import Document
from prompt_toolkit.filters import IsDone
from prompt_toolkit.history import FileHistory
from prompt_toolkit.layout.containers import HSplit, Window, ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.completion import Completer
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.validation import Validator
from prompt_toolkit.shortcuts import create_eventloop

from ptpython.completer import PythonCompleter
from ptpython.python_input import PythonInput
from ptpython.validator import PythonValidator
from ptpython.layout import CompletionVisualisation

from .commands import commands_with_help, shortcuts
from .completers import PythonFileCompleter, PythonFunctionCompleter, BreakPointListCompleter, AliasCompleter, PdbCommandsCompleter
from .grammar import create_pdb_grammar
from .key_bindings import load_custom_pdb_key_bindings
from .layout import PdbLeftMargin
from .toolbars import PdbShortcutsToolbar, FileLocationToolbar
from .completion_hints import CompletionHint
from .style import get_ui_style

import linecache
import os
import pdb
import sys
import weakref


__all__ = (
    'PtPdb',
    'set_trace',
)


class DynamicCompleter(Completer):
    """
    Proxy to a real completer which we can change at runtime.
    """
    def __init__(self, get_completer_func):
        self.get_completer_func = get_completer_func

    def get_completions(self, document, complete_event):
        for c in self.get_completer_func().get_completions(document, complete_event):
            yield c


class DynamicValidator(Validator):
    """
    Proxy to a real validator which we can change at runtime.
    """
    def __init__(self, get_validator_func):
        self.get_validator_func = get_validator_func

    def validate(self, document):
        return self.get_validator_func().validate(document)


class PtPdb(pdb.Pdb):
    def __init__(self):
        pdb.Pdb.__init__(self)

        # Cache for the grammar.
        self._grammar_cache = None  # (current_pdb_commands, grammar) tuple.

        self._cli_history = FileHistory(os.path.expanduser('~/.ptpdb_history'))

        self.completer = None
        self.validator = None

        self.python_input = PythonInput(
                get_locals=lambda: self.curframe.f_locals,
                get_globals=lambda: self.curframe.f_globals,
                _completer=DynamicCompleter(lambda: self.completer),
                _validator=DynamicValidator(lambda: self.validator),
                _python_prompt_control=PdbLeftMargin(self._get_current_pdb_commands()),
                _extra_buffers={'source_code': Buffer()},
                _extra_buffer_processors=[CompletionHint()],
                _extra_sidebars=[
                    HSplit([
                        FileLocationToolbar(weakref.ref(self)),
                        ConditionalContainer(
                            Window(
                                BufferControl(
                                    buffer_name='source_code',
                                    lexer=PythonLexer,
                                ),
                            ),
                            filter=~IsDone()),
                        PdbShortcutsToolbar(weakref.ref(self)),
                    ]),
                ],
        )

        # Set UI styles.
        self.python_input.ui_styles = {
            'ptpdb': get_ui_style(),
        }
        self.python_input.use_ui_colorscheme('ptpdb')

        # Set autocompletion style. (Multi-column works nicer.)
        self.python_input.completion_visualisation = CompletionVisualisation.MULTI_COLUMN
        self.python_input.complete_while_typing = False

        # Load additional key bindings.
        load_custom_pdb_key_bindings(self.python_input.key_bindings_registry)

        self.cli = CommandLineInterface(
            eventloop=create_eventloop(),
            application=self.python_input.create_application())

    def cmdloop(self, intro=None):
        """
        Copy/Paste of pdb.Pdb.cmdloop. But using our own CommandLineInterface
        for reading input instead.
        """
        self.preloop()

        if intro is not None:
            self.intro = intro
        if self.intro:
            self.stdout.write(str(self.intro)+"\n")
        stop = None
        while not stop:
            if self.cmdqueue:
                line = self.cmdqueue.pop(0)
            else:
                if self.use_rawinput:
                    line = self._get_input()

            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def _get_current_pdb_commands(self):
        return (
            list(commands_with_help.keys()) +
            list(shortcuts.keys()) +
            list(self.aliases.keys()))

    def _create_grammar(self):
        """
        Return the compiled grammar for this PDB shell.

        The grammar of PDB depends on the available list of PDB commands (which
        depends on the currently defined aliases.) Therefor we generate a new
        grammar when it changes, but cache it otherwise. (It's still expensive
        to compile.)
        """
        pdb_commands = self._get_current_pdb_commands()

        if self._grammar_cache is None or self._grammar_cache[0] != pdb_commands:
            self._grammar_cache = [
                pdb_commands,
                create_pdb_grammar(pdb_commands)]

        return self._grammar_cache[1]

    def _get_input(self):
        """
        Read PDB input. Return input text.
        """
        # Reset multiline/paste mode every time.
        self.python_input.paste_mode = False
        self.python_input.currently_multiline = False

        # Make sure not to start in Vi navigation mode.
        self.python_input.key_bindings_manager.reset()  # XXX: we should not have to do this here...

        # Set source code document.
        self.cli.buffers['source_code'].document = Document(self._get_source_code())

        # Set up a new completer and validator for the new grammar.
        g = self._create_grammar()

        self.completer = GrammarCompleter(g, completers={
            'enabled_breakpoint': BreakPointListCompleter(only_enabled=True),
            'disabled_breakpoint': BreakPointListCompleter(only_disabled=True),
            'alias_name': AliasCompleter(self),
            'python_code': PythonCompleter(lambda: self.curframe.f_globals, lambda: self.curframe.f_locals),
            'breakpoint': BreakPointListCompleter(),
            'pdb_command': PdbCommandsCompleter(self),
            'python_file': PythonFileCompleter(),
            'python_function': PythonFunctionCompleter(self),
        })
        self.validator = GrammarValidator(g, {
            'python_code': PythonValidator()
        })

        try:
            return self.cli.run().text
        except EOFError:
            # Turn Control-D key press into a 'quit' command.
            return 'q'

    def _get_source_code(self):
        """
        Return source code around current line as string.
        (Partly taken from Pdb.do_list.)
        """
        filename = self.curframe.f_code.co_filename
        breaklist = self.get_file_breaks(filename)

        first = max(1,  self.curframe.f_lineno - 3)
        last = first + 12 # 6

        result = []

        for lineno in range(first, last+1):
            line = linecache.getline(filename, lineno, self.curframe.f_globals)
            if not line:
                line = '[EOF]'
                break
            else:
                s = repr(lineno).rjust(3)
                if len(s) < 4:
                    s = s + ' '
                if lineno in breaklist:
                    s = s + 'B'
                else:
                    s = s + ' '
                if lineno == self.curframe.f_lineno:
                    s = s + '->'
                else:
                    s = s + '  '

                result.append(s + ' ' + line)

        return ''.join(result)

def set_trace():
    PtPdb().set_trace(sys._getframe().f_back)
