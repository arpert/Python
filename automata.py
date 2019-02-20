import msvcrt
import sys
import time
import ctypes
import random

from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

#==== GLOBAL VARIABLES ======================
gHandle = ctypes.windll.kernel32.GetStdHandle (c_long (-11))

def move (y, x):
   """Move cursor to position indicated by x and y."""
   value = (x + (y << 16))
   ctypes.windll.kernel32.SetConsoleCursorPosition (gHandle, c_ulong (value))


maxw = 120
stop = False
wrap = True
reset = False
speed = 20

a = list(([['0','1'][random.randrange(2)] for x in range(maxw)], [' ' for x in range(maxw)]))
cura = 0

c0 = ' '
c1 = '#'                             
all3p = ['000', '001', '010', '011', '100', '101', '110', '111']
pat0 =  ['000', '001', '010', '100']
pat1 =  ['100', '101', '001']
pat2 =  ['010', '100', '001', '101']
pat3 =  ['010', '111', '000', '101']
pat4 =  ['010', '100', '101', '001', '110', '011']

pat5 = ['00100', '01110', '11111', '00000', '11011', '01000', '00010', '10000', '00001']
pat6 = ['11011', '10001', '00000', '11111', '00100', '10111', '11101', '01111', '11110']
pat = pat4

print('pat = ', pat)

plen = len(pat[0])
print('plen = ', plen)
r = [x - (plen >> 1) for x in range(plen)]
print('r = ', r)

while not stop:
   print(''.join([c.replace('1', c1).replace('0', c0) for c in a[cura]]))
   
   for x in range(maxw):
     p = ''
     for dx in r:
       if x+dx >= 0 and x+dx < maxw:
         p += a[cura][x+dx]
       else:
          if wrap:
            p += a[cura][(x+dx+maxw) % maxw]
          else: 
            p += '0' 
     if p in pat:
        a[1 - cura][x] = '1'
     else:
        a[1 - cura][x] = '0'
   cura = 1 - cura

   if msvcrt.kbhit():
      bch = msvcrt.getch()
      if (ord(bch) == 27):
         stop = True
      ch = bch.decode()

      if (ch.upper() == 'W'):
         wrap = not wrap
#         print('wrap=', wrap)

      if (ch.upper() == 'N'):
         print(''.join(['=' for x in range(maxw)]) )
         a[cura] = [['0','1'][random.randrange(2)] for x in range(maxw)]

      elif (ch == ','):
         speed -= 1
         if speed < 1:
           speed = 1

      elif (ch == '.'):
         speed += 1
         if speed > 100:
           speed = 100

      elif (ch == '0'):
         pat = pat0
         reset = True

      elif (ch == '1'):
         pat = pat1
         reset = True

      elif (ch == '2'):
         pat = pat2
         reset = True

      elif (ch == '3'):
         pat = pat3
         reset = True

      elif (ch == '4'):
         pat = pat4
         reset = True

      elif (ch == '5'):
         pat = pat5
         reset = True

      elif (ch == '6'):
         pat = pat6
         reset = True

      if reset:
         plen = len(pat[0])
         r = [x - (plen >> 1) for x in range(plen)]
         reset = False

   time.sleep(2/speed)
   