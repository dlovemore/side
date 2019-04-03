import code
import readline
import sys

ps1 = '>>> '
ps2 = '... '

class Console(code.InteractiveConsole):
    "Console that writes errors using print."
    def write(self, data):
        print(data, end='', file=getattr(self, 'stream', sys.stdout))
    def repl(self, prefix=""):
        prompt = ps1
        while True:
            self.write(prefix+prompt)
            try:
                line = input()
            except EOFError:
                print()
                break
            self.write(line+'\n')
            prompt = ps2 if self.push(line) else ps1


def console():
    console = Console().repl()

if __name__=='__main__':
    console()
