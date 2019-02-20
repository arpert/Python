import msvcrt
import sys
import time
import ctypes
import random
from enum import Enum

from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

#==== GLOBAL VARIABLES ======================
gHandle = ctypes.windll.kernel32.GetStdHandle(c_long (-11))

def move (y, x):
   """Move cursor to position indicated by x and y."""
   value = (x + (y << 16))
   ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong (value))


maxh = 37
maxw = 120
stop = False
dl = 1
dr = 1
nl = 10
nr = 40
speed = 30
ratio = 10

class Command(Enum):
  unknown = -1
  left  = 1001
  right = 1002
  down  = 1003
  up    = 1004
  exit  = 27
  help  = 1005
  menu  = 1006
  clear = 1007

def readCommand():
   gb = msvcrt.getch()
   ret = Command.unknown
   if gb == b'\xe0':
     d = msvcrt.getch()
     if ord(d) == ord('K'):
        ret = Command.left
     elif ord(d) == ord('M'):
        ret = Command.right
     elif ord(d) == ord('H'):
        ret = Command.up
     elif ord(d) == ord('P'):
        ret = Command.down
   else: 
     ch = chr(ord(gb))
#     print('ch = ', ch.upper(), ch)
     if (ord(ch) == 27):
       ret = Command.exit
     elif (ch.upper() == 'C'):
       ret = Command.clear

   return ret

while not stop:
   move(random.randrange(maxh), random.randrange(maxw)) 
   print(' ')
   
   if random.randrange(ratio) == 0:
     move(random.randrange(maxh), random.randrange(maxw)) 
     print('*')

   move(maxh, 0)
   print('speed=%d, ratio=%d  ' % (speed, ratio))

   if msvcrt.kbhit():
      cm = readCommand()
      print('Command: ', cm)
      if (cm == Command.exit):
         stop = True
      elif cm == Command.left:
         ratio -= 1
         if ratio < 1:
           ratio = 1
      elif cm == Command.right:
         ratio += 1
         if ratio > 50:
           ratio = 50
      elif cm == Command.up:
        speed += 1
        if speed > 100:
          speed = 100
      elif cm == Command.down:
         speed -= 1
         if speed < 5:
           speed = 5
      elif cm == Command.clear:
        move(0, 0)
        for i in range(maxh+1):
          print(''.join(' ' for x in range(maxw+1)))


   time.sleep(1/speed)
   nl += dl
   nr += dr
   if (nr - nl <= 15):
      dr = -dr
      dl = -dl
   else:
     if (nl < 1 or nl > maxw - 3):
        dl = -dl

     if (nr < 1 or nr > maxw - 3):
        dr = -dr
#   move(10, 10)
   