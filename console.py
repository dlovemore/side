import code
import readline
import sys

ps1 = '>>> '
ps2 = '... '

def reportexcinfo(stopat=None, limit=None):
    import inspect
    def reportvars(vs,limit=72):
        def reportvar(v,val):
            nonlocal limit
            s='  '
            try:
                s+=str(v)+'='
                s+=str(val)
            except Exception:
                s+='ERROR'
            if limit:
                if len(s)>limit-2: s=s[:limit-3]+'...'
            return s[:limit]
        return ''.join([reportvar(v,val)+'\n'
            for v,val in vs.items() if v.find('_')!=0])
    last_typei, last_value, last_traceback = sys.exc_info()
    traceback=last_traceback
    s=''
    while traceback:
        frame = traceback.tb_frame
        s+=str(inspect.getfile(frame.f_code))+':'
        s+=str(traceback.tb_lineno)+':'
        traceback=traceback.tb_next
        if not traceback: s+=' '+str(last_value)
        s+='\n'
        s+=reportvars(frame.f_globals,limit=limit)
        s+=reportvars(frame.f_locals,limit=limit)
        s+=str(frame.f_locals.get('self'))+'\n'
        s+=str(stopat.f_locals.get('self'))+'\n'
    return s

class Console(code.InteractiveConsole):
    "Console that writes errors using print."
    def write(self, data):
        print(data, end='', file=getattr(self, 'stream', sys.stdout))
    def showtraceback(self):
        import inspect
        self.write(reportexcinfo(stopat=inspect.currentframe()))
    def showsyntaxerror(self, filename=None):
        last_typei, last_value, last_traceback = sys.exc_info()
        s=str(last_value)
        self.write(s+'\n')
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

# >>> 
# >>> x
# /usr/lib/python3.6/code.py:91:
#   sys=<module 'sys' (built-in)>
#   traceback=<module 'traceback' from '/usr/lib/python3.6/traceback.py'>
#   argparse=<module 'argparse' from '/usr/lib/python3.6/argparse.py'>
#   CommandCompiler=<class 'codeop.CommandCompiler'>
#   compile_command=<function compile_command at 0x7f7a060bb9d8>
#   InteractiveInterpreter=<class 'code.InteractiveInterpreter'>
#   InteractiveConsole=<class 'code.InteractiveConsole'>
#   interact=<function interact at 0x7f7a06109158>
#   code=<code object <module> at 0x7f7a061aaed0, file "<console>", line 1>
#   self=<console.Console object at 0x7f7a07e67978>
# <console.Console object at 0x7f7a07e67978>
# <console.Console object at 0x7f7a07e67978>
# <console>:1: name 'x' is not defined
# None
# <console.Console object at 0x7f7a07e67978>
# >>> 
# >>> 
# >>> x/0
# /usr/lib/python3.6/code.py:91:
#   sys=<module 'sys' (built-in)>
#   traceback=<module 'traceback' from '/usr/lib/python3.6/traceback.py'>
#   argparse=<module 'argparse' from '/usr/lib/python3.6/argparse.py'>
#   CommandCompiler=<class 'codeop.CommandCompiler'>
#   compile_command=<function compile_command at 0x7fa934fab9d8>
#   InteractiveInterpreter=<class 'code.InteractiveInterpreter'>
#   InteractiveConsole=<class 'code.InteractiveConsole'>
#   interact=<function interact at 0x7fa934ff9158>
#   code=<code object <module> at 0x7fa93509aed0, file "<console>", line 1>
#   self=<console.Console object at 0x7fa936d57978>
# <console.Console object at 0x7fa936d57978>
# <console.Console object at 0x7fa936d57978>
# <console>:1: name 'x' is not defined
# None
# <console.Console object at 0x7fa936d57978>
# >>> 3/0
# /usr/lib/python3.6/code.py:91:
#   sys=<module 'sys' (built-in)>
#   traceback=<module 'traceback' from '/usr/lib/python3.6/traceback.py'>
#   argparse=<module 'argparse' from '/usr/lib/python3.6/argparse.py'>
#   CommandCompiler=<class 'codeop.CommandCompiler'>
#   compile_command=<function compile_command at 0x7f2ad64249d8>
#   InteractiveInterpreter=<class 'code.InteractiveInterpreter'>
#   InteractiveConsole=<class 'code.InteractiveConsole'>
#   interact=<function interact at 0x7f2ad6472158>
#   code=<code object <module> at 0x7f2ad6497420, file "<console>", line 1>
#   self=<console.Console object at 0x7f2ad81d0908>
# <console.Console object at 0x7f2ad81d0908>
# <console.Console object at 0x7f2ad81d0908>
# <console>:1: division by zero
# None
# <console.Console object at 0x7f2ad81d0908>
# >>> 
