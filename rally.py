import msvcrt
import sys
import time
import random
from enum import Enum

maxw = 80
stop = False
dl = 1
dr = 1
nl = 10
nr = 40
n = int((nl + nr) / 2)
dn = 0
speed = 20

class Command(Enum):
  unknown = -1
  left  = 1001
  right = 1002
  down  = 1003
  up    = 1004
  exit  = 27
  help  = 1005
  menu  = 1006

def readCommand():
   ch = msvcrt.getch()
   ret = Command.unknown
   if (ord(ch) == 27):
     ret = Command.exit
   elif ch == b'\xe0':
     d = msvcrt.getch()
     if ord(d) == ord('K'):
        ret = Command.left
     elif ord(d) == ord('M'):
        ret = Command.right
     elif ord(d) == ord('H'):
        ret = Command.up
     elif ord(d) == ord('P'):
        ret = Command.down

   return ret

while not stop:
   line = [' ' for x in range(maxw)]
   line[nl] = '>'
   line[nr] = '<'
   line[n]  = '#'
#   print('>'.join('' for x in range(nl-1))+ '.'.join('' for x in range(nr - nl - 1)) + '<'.join('' for x in range(maxw - nr - 1)))
   print(''.join(line))
   if msvcrt.kbhit():
      cm = readCommand()
      if (cm == Command.exit):
         stop = True
      elif cm == Command.left:
         dn = -1
      elif cm == Command.right:
         dn = 1
      elif cm == Command.up:
        speed += 1
        if speed > 100:
          speed = 100
      elif cm == Command.down:
         speed -= 1
         if speed < 5:
           speed = 5     

   time.sleep(1/speed)
   nl += dl
   nr += dr
   n += dn

   if (nr - nl <= 15):
      dr = -dr
      dl = -dl
   else:
     if (nl < 1 or nl > maxw - 3 or random.randrange(15) == 0):
        dl = -dl

     if (nr < 1 or nr > maxw - 3 or random.randrange(15) == 0):
        dr = -dr

   if n <= nl:
     n = nl + 1
     dn = -dn

   if n >= nr:
     n = nr - 1
     dn = -dn  

