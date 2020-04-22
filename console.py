import code
import readline
import sys
import inspect

ps1 = '>>> '
ps2 = '... '

def sstr(s):
    try:
        return str(s)
    except Exception as e:
        try:
            return '***Error in str: '+str(e)
        except: pass
    return '???'

def leadin(s):
    i=0
    for c in s:
        if c==' ': i+=1
        elif c=='\t': i=(i&~7)+8
        elif c=='\n': return None
        else: return i
    return None

def codetext(code):
    if hasattr(code,'f_code'): code = code.f_code
    elif hasattr(code,'__code__'): code = code.__code__
    filename=inspect.getfile(code)
    if filename[0] in '<_': return
    with open(filename) as f:
        t=f.readlines()
    fun=t[code.co_firstlineno-1:]
    lead=leadin(fun[0])
    for i,l in enumerate(fun[1:], start=1):
        ll=leadin(l)
        if ll is not None and ll<=lead:
            fun=fun[:i]
            break
    return (''.join(fun))

def reportexcinfo(startat=None, limit=72):
    def trim(s):
        nonlocal limit
        if limit:
            if len(s)>limit-2: s=s[:limit-3]+'...'
            return s[:limit]
        return s
    def indent(s,prefix='  '):
        return ''.join([prefix+l if l else l for l in s.splitlines(keepends=True)])
    def trims(s):
        return '\n'.join(map(trim,s.split('\n')))
    def reportvar(v,val):
        s=sstr(v)+'='
        s+=sstr(val)
        return trim(s)
    def reportvars(vs):
        return indent(''.join([reportvar(v,val)+'\n' for v,val in vs.items()]),prefix='    ')
    def reportcall(fname,args):
        nonlocal limit
        if fname=='<module>' and not args: return ''
        rargs=[reportvar(k,v) for k,v in args.items()]
        # print('rargs: ',rargs)
        r=fname+'('+", ".join(rargs)+')'
        if len(r)>limit:
            r=fname+'(\n'+indent('\n'.join(rargs))+'\n)'
        return indent(r)+'\n'
    def reportframe(frame):
        code = frame.f_code
        fname=code.co_name
        vars=code.co_varnames
        freevars=code.co_freevars
        locals=frame.f_locals
        globals=frame.f_globals
        varitems=[]
        vars+=freevars
        for k in vars:
            try:
                if k in locals:
                    varitems+=[(k,locals[k])]
                elif k in globals:
                    varitems+=[(k,globals[k])]
            except:
                varitems[k]=(k,'??')
        argcount = code.co_argcount
        args,vars=varitems[:argcount],varitems[argcount:]
        s=reportcall(fname,dict(args))
        s+=reportvars(dict(vars))
        return trims(s)

    last_type, last_value, last_traceback = sys.exc_info()
    traceback=last_traceback
    s=''
    on=False
    first=True
    while traceback:
        frame = traceback.tb_frame
        frameself=frame.f_locals.get('self')
        code = frame.f_code
        filename=inspect.getfile(frame.f_code)
        if on:
            s+=sstr(filename)+':'
            s+=sstr(traceback.tb_lineno)+':'
            s+=' '+last_type.__name__
            if sstr(last_value): s+=': '+sstr(last_value)
            s+='\n'
            s+=reportframe(frame)
        if startat==frameself:
            on=True
        traceback=traceback.tb_next
    return s

class Console(code.InteractiveConsole):
    "Console that writes errors using print."
    def __init__(self,*args,**kwargs):
        self.npush=0
        super().__init__(*args,**kwargs)
    def write(self, data):
        print(data, end='', file=getattr(self, 'stream', sys.stdout))
    def showtraceback(self):
        self.write(reportexcinfo(startat=self))
        try:
            pass
        except:
            self.write('Console: Error in traceback report\n')
    def runsource(self,t,filename,*args,**kwargs):
        if filename=='<console>': filename='<'+str(self.npush)+'>'
        return super().runsource(t,filename,*args,**kwargs)
    def push(self,code,*args,**kwargs):
        self.npush+=1
        r=super().push(code,*args,**kwargs)
        self.npush-=r and 1
        return r
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
                self.write('\n')
                break
            self.write(line+'\n')
            prompt = ps2 if self.push(line) else ps1


def console():
    console = Console().repl()

if __name__=='__main__':
    console()

# >>> i=1
# >>> 'abc\n123\n'.split('\n')
# ['abc', '123', '']
# >>> 
# >>> j
# <4>:1: NameError: name 'j' is not defined
# >>> 
# >>> x
# <6>:1: NameError: name 'x' is not defined
# >>> 
# >>> x/0
# <8>:1: NameError: name 'x' is not defined
# >>> x/0
# <9>:1: NameError: name 'x' is not defined
# >>> 3/0
# <10>:1: ZeroDivisionError: division by zero
# >>> class ee:
# ...     def __str__(self): q
# ... 
# >>> e=ee()
# >>> e
# <__console__.ee object at 0xb65befd0>
# >>> q
# <14>:1: NameError: name 'q' is not defined
# >>> def f(x):
# ...    y=3+x
# ...    q
# ... 
# >>> f(1)
# <16>:1: NameError: name 'q' is not defined
# <15>:3: NameError: name 'q' is not defined
#   f(x=1)
#     y=4
# >>> z=12
# >>> def g(x):
# ...    nonlocal z
# no binding for nonlocal 'z' found (<18>, line 2)
# >>> 
# >>> def g(x):
# ...     z=12
# ...     def f(y):
# ...         nonlocal z
# ...         try:
# ...             return z/y
# ...         except ZeroDivisionError:
# ...             raise ValueError(str(y))
# ...     return f(x)
# ... 
# >>> 
# >>> 
# >>> g(12)
# 1.0
# >>> g(0)
# <24>:1: ValueError: 0
# <20>:9: ValueError: 0
#   g(x=0)
#     f=<function g.<locals>.f at 0xb65cdb28>
# <20>:8: ValueError: 0
#   f(y=0)
#     z=12
# >>> 
# >>> 
# >>> g(2)
# 6.0
# >>> 
# >>> from console import *
# >>> 
# >>> sstr(1/0)
# <31>:1: ZeroDivisionError: division by zero
# >>> g('x'*10)
# <32>:1: TypeError: unsupported operand type(s) for /: 'int' and 'str'
# <20>:9: TypeError: unsupported operand type(s) for /: 'int' and 'str'
#   g(x=xxxxxxxxxx)
#     f=<function g.<locals>.f at 0xb65cddf8>
# <20>:6: TypeError: unsupported operand type(s) for /: 'int' and 'str'
#   f(y=xxxxxxxxxx)
#     z=12
# >>> g('x'*100)
# <33>:1: TypeError: unsupported operand type(s) for /: 'int' and 'str'
# <20>:9: TypeError: unsupported operand type(s) for /: 'int' and 'str'
#   g(
#     x=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...
#   )
#     f=<function g.<locals>.f at 0xb65cdc48>
# <20>:6: TypeError: unsupported operand type(s) for /: 'int' and 'str'
#   f(
#     y=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...
#   )
#     z=12
# >>> 
# >>> codetext
# <function codetext at 0xb659bcd8>
# >>> codetext(codetext.__code__)
# "def codetext(code):\n    if hasattr(code,'f_code'): code = code.f_code\n    elif hasattr(code,'__code__'): code = code.__code__\n    filename=inspect.getfile(code)\n    if filename[0] in '<_': return\n    with open(filename) as f:\n        t=f.readlines()\n    fun=t[code.co_firstlineno-1:]\n    lead=leadin(fun[0])\n    for i,l in enumerate(fun[1:], start=1):\n        ll=leadin(l)\n        if ll is not None and ll<=lead:\n            fun=fun[:i]\n            break\n    return (''.join(fun))\n\n"
# >>> codetext(codetext)
# "def codetext(code):\n    if hasattr(code,'f_code'): code = code.f_code\n    elif hasattr(code,'__code__'): code = code.__code__\n    filename=inspect.getfile(code)\n    if filename[0] in '<_': return\n    with open(filename) as f:\n        t=f.readlines()\n    fun=t[code.co_firstlineno-1:]\n    lead=leadin(fun[0])\n    for i,l in enumerate(fun[1:], start=1):\n        ll=leadin(l)\n        if ll is not None and ll<=lead:\n            fun=fun[:i]\n            break\n    return (''.join(fun))\n\n"
# >>> codetext.__code__.co_firstlineno
# 27
# >>> codetext.__code__.co_lnotab
# b'\x00\x01\n\x00\x08\x01\n\x00\x06\x01\n\x01\x0c\x00\x04\x01\n\x01\x12\x01\x12\x01\x0c\x01\x1e\x01\x08\x01\x10\x01\x0c\x01\x06\x01'
# >>> len(_)/2
# 17.0
# >>> 1G
# invalid syntax (<41>, line 1)
# >>> 
# >>> codetext(7)
# <43>:1: TypeError: module, class, method, function, traceback, frame, or code object was expected, got int
# /home/pi/python/side/console.py:30: TypeError: module, class, method, function, traceback, frame, or code object was expected, got int
#   codetext(code=7)
# /usr/lib/python3.7/inspect.py:666: TypeError: module, class, method, function, traceback, frame, or code object was expected, got int
#   getfile(object=7)
# >>> 
# >>> codetext.__code__.co_names
# ('hasattr', 'f_code', '__code__', 'inspect', 'getfile', 'open', 'readlines', 'co_firstlineno', 'leadin', 'enumerate', 'join')
# >>> print(codetext(codetext))
# def codetext(code):
#     if hasattr(code,'f_code'): code = code.f_code
#     elif hasattr(code,'__code__'): code = code.__code__
#     filename=inspect.getfile(code)
#     if filename[0] in '<_': return
#     with open(filename) as f:
#         t=f.readlines()
#     fun=t[code.co_firstlineno-1:]
#     lead=leadin(fun[0])
#     for i,l in enumerate(fun[1:], start=1):
#         ll=leadin(l)
#         if ll is not None and ll<=lead:
#             fun=fun[:i]
#             break
#     return (''.join(fun))
# 
# 
# >>> codetext(Console.__init__)
# '    def __init__(self,*args,**kwargs):\n        self.npush=0\n        super().__init__(*args,**kwargs)\n'
# >>> leadin('  \t\tx')
# 16
# >>> codetext(leadin)
# "def leadin(s):\n    i=0\n    for c in s:\n        if c==' ': i+=1\n        elif c=='\\t': i=(i&~7)+8\n        elif c=='\\n': return None\n        else: return i\n    return None\n\n"
# >>> print(codetext(Console.__init__))
#     def __init__(self,*args,**kwargs):
#         self.npush=0
#         super().__init__(*args,**kwargs)
# 
# >>> Console.runsource.__code__
# <code object runsource at 0xb65fe2e0, file "/home/pi/python/side/console.py", line 127>
# >>> 
# >>> Console().compile.__class__.__init__.__code__
# <code object __init__ at 0xb66082e0, file "/usr/lib/python3.7/codeop.py", line 146>
# >>> compile
# <built-in function compile>
# >>> help(compile)
# Help on built-in function compile in module builtins:
# 
# compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)
#     Compile source into a code object that can be executed by exec() or eval().
#     
#     The source code may represent a Python module, statement or expression.
#     The filename will be used for run-time error messages.
#     The mode must be 'exec' to compile a module, 'single' to compile a
#     single (interactive) statement, or 'eval' to compile an expression.
#     The flags argument, if present, controls which future statements influence
#     the compilation of the code.
#     The dont_inherit argument, if true, stops the compilation inheriting
#     the effects of any future statements in effect in the code calling
#     compile; if absent or false these statements do influence the compilation,
#     in addition to any features explicitly specified.
# 
# >>> compile('\n\n\ndef x(y): return y\n',filename='xx',mode='exec')
# <code object <module> at 0xb649c7b0, file "xx", line 4>
# >>> 
# >>> 
# >>> x
# <59>:1: NameError: name 'x' is not defined
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
# >>> 
