# import subprocess
import fcntl
from auto import *
from subprocess import *
from queue import *
from threading import *

def nonblock(fd):
    flags=fcntl.fcntl(fd, fcntl.F_GETFL)
    flags |= os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

ro,wo=pty.openpty()
nonblock(ro)

ri,wi=pty.openpty()
nonblock(wi)
# nonblock(ri)

# nonblock(si)
# nonblock(mi)

pr=Popen(['python3', '-iq',],stdin=ri,stdout=wo,stderr=wo,bufsize=0)
os.close(ri)
os.close(wo)
out=os.fdopen(ro,'rb+',buffering=0)
inp=os.fdopen(wi,'wb',buffering=0)
# ot=io.TextIOWrapper(out)

inp.write(b'"abc"\n')
inp.write(b'"def"\n')
inp.write(b'1+4+9\n')
inp.write(b'1/4+9\n')
inp.write(b'print(1/4+9)\n')

print(pr.poll())
# print(out.read())
#print(out.readline())

prompt=''
def fdlines(file):
    global prompt
    fd = file if isinstance(file,int) else fd.fileno()
    buf=b''
    bufsize=io.DEFAULT_BUFFER_SIZE
    bufsize=10
    while True:
        select.select({fd},{},{})
        try:
            r=os.read(fd,bufsize)
        except OSError:
            r=None
            return 'EOF'
        if r==None: return 'no read'
        if not r: return 'end'
        buf+=r
        ls=io.TextIOWrapper(io.BytesIO(buf)).readlines()
        yield from ls
        buf=b''

g=lines(out)
it=iter(g)

# >>> from talk4 import *
# >>> 
