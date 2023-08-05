from __future__ import unicode_literals, absolute_import

from prompt_toolkit.layout.controls import TokenListControl

from pygments.token import Token


class PdbLeftMargin(TokenListControl):
    """
    Pdb prompt.

    Show "(pdb)" when we have a pdb command or '>>>' when the user types a
    Python command.
    """
    def __init__(self, pdb_commands):
        def get_tokens(cli):
            b = cli.buffers['default']

            command = b.document.text.lstrip()
            if command:
                command = command.split()[0]

            if any(c.startswith(command) for c in pdb_commands):
                return [(Token.Prompt, '(pdb) ')]
            else:
                return [(Token.Prompt, '  >>> ')]

        super(PdbLeftMargin, self).__init__(get_tokens)
