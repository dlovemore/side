import sys
import io
import re
from side.console import *

ps1 = '>>> '
ps2 = '... '

def indent(s, prefix = '    '):
    return "".join([prefix+line for line in s.splitlines(keepends=True)])

def runfile(file, console=None):
    """
    Any interactive session can be recorded and rerun. The contents of
    the open file is copied to the output. Anything in the file starting
    with a python prompt is evaluated. The output is captured and added
    to the output after the echoed input.

        >>> 3+4
        7

    Anything indented is removed and replaced with new output. Anything not
    indented is kept.

    Sessions within comments are run:

        # >>> print('this')
        # this

    Double commented sessions are not:

        # # >>> print('that')
        # # this

    Use a diff tool on input and output to show changes and for checking against
    expected output.
    """
    console = console or Console()
    last_prefix = None
    prompt = ps1
    prompt_re = re.compile(r'^(\s*#?\s*)('+re.escape(ps1)+r'|'+re.escape(ps2)+r'|)(.*)')
    for line in file:
        mo = prompt_re.match(line)
        prefix, read_prompt, code = mo.groups()
        if read_prompt:
            print(prefix+prompt+code)
            stream = io.StringIO()
            stdout = sys.stdout
            try:
                sys.stdout = stream
                prompt = ps2 if console.push(code) else ps1
            finally:
                sys.stdout = stdout
            out = indent(stream.getvalue(), prefix=prefix)
            print(out, end='')
            last_prefix = prefix
            oldout = ''
        elif last_prefix is None or prefix < last_prefix:
            last_prefix = None
            prompt = ps1
            print(line, end='')
        else:
            oldout += line
    return last_prefix

def main(prog, filename=None):
    """
    side
    * To replay sessions from standard input.
    side file
    * To replay sessions from file.
    """
    file = open(filename) if filename else sys.stdin
    console = Console()
    last_prefix = runfile(file, console=console)

if __name__=='__main__':
    main(*sys.argv)
