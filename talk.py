# import subprocess
import fcntl
from auto import *
from subprocess import *
from queue import *
from threading import *

mi,si = os.openpty()

def nonblock(fd):
    flags=fcntl.fcntl(fd, fcntl.F_GETFL)
    flags |= os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def nq(out,q):
    for line in iter(out.readline, b''):
        q.put(line)
    out.close()

# pr=Popen(['side'],stdin=PIPE,stdout=PIPE,bufsize=1)

nonblock(si)
nonblock(mi)

pr=Popen(['side'],stdin=si,stdout=PIPE,bufsize=1)

os.close(si)
os.write(mi,b'123\n')


