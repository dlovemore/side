import sys
import io
import re
import os
from console import *

ps1 = '>>> '
ps2 = '... '

def indent(s, prefix = '    '):
    return "".join([prefix+line for line in s.splitlines(keepends=True)])

def testfile(filename, console=None):
    """
    Any interactive session can be recorded and rerun. The contents of the file
    is copied to the output. Anything in the file starting with a python prompt
    is evaluated. The output is captured and added to the output after the
    echoed input.

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
    filename = sys.stdin if filename == '-' else open(filename)
    console = console or Console()
    last_prefix = None
    prompt = ps1
    prompt_re = re.compile(r'^(\s*#?\s*)('+re.escape(ps1)+r'|'+re.escape(ps2)+r'|)(.*)')
    for line in filename:
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

def main():
    """
    side file
    * To output contents of file with sessions replayed.
    side -i file
    * To replay session and extend it by reading from console,
    file can be - to read from stdin.
    """
    console = Console()
    args = sys.argv
    filename = '-' if len(args)==1 else args[-1]
    last_prefix = testfile(filename, console=console)

if __name__=='__main__':
    main()
# >>> t=4
# >>> t
# 4
# >>> t
# 4
