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

ro,wo=os.pipe2(os.O_NONBLOCK)

ri,wi=pty.openpty()
nonblock(wi)
# nonblock(ri)

# nonblock(si)
# nonblock(mi)

pr=Popen(['python3','-i'],stdin=ri,stdout=wo,stderr=wo,bufsize=0)
out=os.fdopen(ro,'rb+',buffering=0)

os.write(wi,b'"abc"\n')
os.write(wi,b'"def"\n')
os.write(wi,b'1+4+9\n')
os.write(wi,b'1/4+9\n')
os.write(wi,b'print(1/4+9)\n')

print(pr.poll())
# print(out.read())
#print(out.readline())

