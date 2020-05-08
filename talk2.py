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

fout=open('stdout_talk2','wb',buffering=0)
ferr=open('stdout_talk2','wb',buffering=0)

ri,wi=os.pipe2(os.O_NONBLOCK)

# nonblock(si)
# nonblock(mi)

pr=Popen(['side'],stdin=ri,stdout=fout,stderr=ferr,bufsize=0)

os.write(wi,b'abc\n')
os.write(wi,b'def\n')
os.write(wi,b'>>> 1+4+9\n')

out=open('stdout_talk2','r')
print(pr.poll())
print(out.read())
print(out.readline())

