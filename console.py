import code
import readline

ps1 = '>>> '
ps2 = '... '

class Console(code.InteractiveConsole):
    "Console that writes errors using print."
    def write(self, data): print(data, end='')

def console():
    console = Console()
    prompt = ps1
    while True:
        try:
            line = input(prompt)
        except EOFError:
            print()
            break
        print(line)
        prompt = ps2 if console.push(line) else ps1

if __name__=='__main__':
     console()
