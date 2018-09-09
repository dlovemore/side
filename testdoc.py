import sys
import io
import re
from console import Console

ps1 = '>>> '
ps2 = '... '

def indent(s, prefix = '    '):
    return "".join([prefix+line for line in s.splitlines(keepends=True)])

def testfile(filename):
    console = Console()
    last_prefix = None
    prompt = ps1
    prompt_re = re.compile(r'^(\s*)('+re.escape(ps1)+r'|'+re.escape(ps2)+r'|)(.*)')
    for line in open(filename):
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


if __name__=='__main__':
    testfile(sys.argv[-1])
