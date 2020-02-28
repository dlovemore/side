import code
import readline
import sys
import inspect

ps1 = '>>> '
ps2 = '... '

def reportexcinfo(startat=None, limit=72):
    import inspect
    def reportvars(vs,limit):
        def reportvar(v,val):
            nonlocal limit
            s='    '
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
    last_type, last_value, last_traceback = sys.exc_info()
    traceback=last_traceback
    s=''
    on=False
    while traceback:
        frame = traceback.tb_frame
        frameself=frame.f_locals.get('self')
        if on:
            s+=str(inspect.getfile(frame.f_code))+':'
            s+=str(traceback.tb_lineno)+':'
            s+=' '+str(last_value)
            s+='\n'
            # s+=reportvars(frame.f_globals,limit=limit)
            s+=reportvars(frame.f_locals,limit=limit)
        if startat==frameself:
            on=True
        traceback=traceback.tb_next
    return s

class Console(code.InteractiveConsole):
    "Console that writes errors using print."
    def write(self, data):
        print(data, end='', file=getattr(self, 'stream', sys.stdout))
    def showtraceback(self):
        self.write(reportexcinfo(startat=self))
    def showsyntaxerror(self, filename=None):
        last_type, last_value, last_traceback = sys.exc_info()
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

# >>> i=1
# >>> j
# <console>:1: name 'j' is not defined
#     i=1
# >>> 
# >>> x
# <console>:1: name 'x' is not defined
#     i=1
# >>> 
# >>> 
# >>> x/0
# <console>:1: name 'x' is not defined
#     i=1
# >>> x/0
# <console>:1: name 'x' is not defined
#     i=1
# >>> 3/0
# <console>:1: division by zero
#     i=1
# >>> class ee:
# ...     def __str__(self): q
# ... 
# >>> e=ee()
# >>> e
# <__console__.ee object at 0x7f36a49b64e0>
# >>> q
# <console>:1: name 'q' is not defined
#     i=1
#     ee=<class '__console__.ee'>
#     e=ERROR
# >>> def f(x):
# ...    y=3+x
# ...    q
# ... 
# >>> f(1)
# <console>:1: name 'q' is not defined
#     i=1
#     ee=<class '__console__.ee'>
#     e=ERROR
#     f=<function f at 0x7f36a49a57b8>
# <console>:3: name 'q' is not defined
#     y=4
#     x=1
# >>> 
