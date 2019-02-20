import msvcrt
import sys
import time
import ctypes
import random

from ctypes import c_long, c_wchar_p, c_ulong, c_void_p
from enum import Enum

global dx
global dy

#==== GLOBAL VARIABLES ======================
gHandle = ctypes.windll.kernel32.GetStdHandle(c_long (-11))

def setPos(x, y):
#   """Move cursor to position indicated by x and y."""
   value = (x + (y << 16))
   ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong (value))
#   print('setPos(%d, %d)' % (y, x))


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
  annotations = 1008
  boom = 1009
  showitems = 1010
  genitems = 1011
  sel1  = 1101
  sel2  = 1102
  sel3  = 1103
  sel4  = 1104

class Board:
  xpos = 0
  ypos = 0
  width = 60
  height = 25
  dirdispy = 0

  items = list()

  def Clear(self) -> None:
     setPos(0, 0)
     for i in range(Board.height):
        setPos(Board.xpos, Board.ypos + i)
        print(''.join(' ' for x in range(Board.width)))

  def drawBorder(self):
    setPos(Board.xpos, Board.ypos)
    print('+' + ''.join('-' for x in range(Board.width - 1)) + '+')
    for y in range(Board.height - 1):
       setPos(Board.xpos, Board.ypos + y + 1)
       print('|')
       setPos(Board.xpos + Board.width, Board.ypos + y + 1)
       print('|')

    setPos(Board.xpos, Board.ypos + Board.height)
    print('+' + ''.join('-' for x in range(Board.width - 1)) + '+')

  def showItems(self) -> None:
     for i in self.items:
        setPos(i[0], i[1])
        print(i[2])

  def genItems(self) -> None:
     ix = -1
     iy = -1
     for i in range(2 + random.randrange(10)):
        while next((x for x in self.items if x[0] == ix and x[1] == iy), None) != None or ix == -1 or iy == -1:
           ix = Board.xpos + random.randrange(Board.width - 2) + 1
           iy = Board.ypos + random.randrange(Board.height - 2) + 1
        iv = random.randrange(9) + 1
        Board.showLog('(%2d, %2d) -> %d' % (ix, iy, iv))
        self.items.append((ix, iy, iv))

     self.showItems()

  def showLog(msg:'string to display') -> """Display log message """:
#    return
    setPos(Board.xpos + Board.width + 1, Board.dirdispy)
    print(msg)
    Board.dirdispy = (Board.dirdispy + 1) % Board.height
    setPos(Board.xpos + Board.width + 1, Board.dirdispy)
    print('                                 ')
    
  def boom():
    w2 = (Board.width >> 1)
    h2 = (Board.height >> 1)
    x0 = Board.xpos + w2
    y0 = Board.ypos + h2
    Board.showLog('x0 = %d, y0 = %d' % (x0, y0))
    for i in range(1, h2+1):
       Board.showLog('i = %d' % i)
       for y in range(i):
          for x in range(2 * i):
             setPos(x0 - i + x, y0 - y)
             print('#')
             setPos(x0 - i + x, y0 + y)
             print('#')
    for i in range(1, h2+1):
       Board.showLog('i = %d' % i)
       for y in range(i):
          for x in range(2 * i):
             setPos(x0 - i + x, y0 - y)
             print(' ')
             setPos(x0 - i + x, y0 + y)
             print(' ')
#             time.sleep(.1)
    st = '----====#### B O O O M ###====----'
    setPos(x0 - (len(st) >> 1), y0)
    print(st)


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
     elif (ch.upper() == 'H'):
       ret = Command.help
     elif (ch.upper() == '1'):
       ret = Command.sel1
     elif (ch.upper() == '2'):
       ret = Command.sel2
     elif (ch.upper() == '3'):
       ret = Command.sel3
     elif (ch.upper() == '4'):
       ret = Command.sel4
     elif (ch.upper() == 'M'):
       ret = Command.menu
     elif (ch.upper() == 'G'):
       ret = Command.genitems
     elif (ch.upper() == 'S'):
       ret = Command.showitems
     elif (ch.upper() == 'A'):
       ret = Command.annotations
     elif (ch.upper() == 'B'):
       ret = Command.boom

   return ret

class MySnake(): 

  """Snake main class """
  def __init__(self)  -> """Initialize class attributes """:
#     print('Init', self)
     self.snakeLen = 5
     self.snakeBody = [(10, 10), (10, 10)]
     self.setDir(1, 0)
  
  def setDir(self, dirx: 'New X direction', diry:'New Y direction')  -> """Set new direction """:
    Board.showLog('setDir(%d, %d)'% (dirx, diry))

    hx = self.snakeBody[len(self.snakeBody)-1][0]
    hy = self.snakeBody[len(self.snakeBody)-1][1]
    if hx + dirx > Board.xpos and hx + dirx < Board.xpos + Board.width and \
       hy + diry > Board.ypos and hy + diry < Board.ypos + Board.height:
      self.dx = dirx
      self.dy = diry


  def moveSnake(self) -> 'Move snake by one step in set direction':
    """Direction set by setDir method """
#    Board.showLog('MoveSnake %d, %d, [%d]' % (self.dx, self.dy, self.snakeLen))
    hx = self.snakeBody[len(self.snakeBody)-1][0]
    hy = self.snakeBody[len(self.snakeBody)-1][1]

    if hx + self.dx <= Board.xpos or hx + self.dx >= Board.xpos + Board.width:
      if hy > (Board.ypos + Board.height >> 1):
#        self.setDir(0, -1)
        self.dx = 0
        self.dy = -1
      else:
#        self.setDir(0, 1)
        self.dx = 0
        self.dy = 1

    elif hy + self.dy <= Board.ypos or hy + self.dy >= Board.ypos + Board.height:
      if hx > Board.xpos + Board.width >> 1:
#        self.setDir(-1, 0)
        self.dx = -1
        self.dy = 0
      else:
#        self.setDir(1, 0)
        self.dx = 1
        self.dy = 0

    newx = hx + self.dx
    newy = hy + self.dy
#    Board.showLog('len(Board.items) = %d' % len(Board.items))
    for i in range(len(Board.items)):
      bi = Board.items[i]
      if (bi[0] == newx and bi[1] == newy):
         Board.showLog('%d %s' % (i, Board.items[i]) )
         Board.showLog('AAAAAAM (%d) -> %d' % (bi[2], len(Board.items) - 1))
         self.snakeLen += int(bi[2])
         del Board.items[i]
         break

    self.snakeBody.append((newx, newy))
    n = 0
    while len(self.snakeBody) > self.snakeLen + 1:
       setPos(self.snakeBody[0][0], self.snakeBody[0][1])
       print(' ')
       del self.snakeBody[0]
       n += 1
       if (n > 1):
         break
  
  def showSnake(self):
     setPos(Board.xpos + 1, Board.ypos + Board.height + 1)
     st = 'snake %d, %s, (%d, %d)' % (len(self.snakeBody), str(self.snakeBody[len(self.snakeBody)-1]), self.dx, self.dy)
     print(st + ''.join([' ' for x in range(Board.width - len(st))]))
     n = len(self.snakeBody)
     for i in range(n):
       p = self.snakeBody[i]
       setPos(p[0], p[1])
       if (i == 0):
          print(' ')
       else:
          if (i == n - 1):
            print('O')
          else:
            print('o')
  
def menu(menuItems, sel):
  setPos(Board.xpos, Board.ypos + Board.height + 2)
  n = 0
  w = 20
  st = '+-----M-E-N-U-----' + str(sel)
  print(st + ''.join([' ' for x in range(w - len(st))]))
  for mi in menuItems:
    st = '| ' + mi
    if (n==sel):
      st += ' <=='
    print(st + ''.join([' ' for x in range(w - len(st) - 1)]) + '|')
    n += 1
  st = '+'
  print(st + ''.join(['-' for x in range(w - len(st) - 1)]) + '+')
    


mnu = ['C - Czyść', '1 - Wybór 1', '2 - Wybór 2', '3 - Wybór 3', '4 - Wybór 4', 'H - Pomoc', ' ', '[Esc] - wyjście']
sel = -1
cm = Command.unknown 
stepMode=False
stop = False
speed = 0.2
d = '0'

def doGame():
  global stop
  global speed

  s = MySnake()
  b = Board()
  print('Begin', s.dx, s.dy)
  b.Clear()
  b.drawBorder()
  b.genItems()
  s.showSnake()

  while not stop:
     if msvcrt.kbhit() or stepMode:
        cm = readCommand()
  #      print('Command: ', cm)
        if (cm == Command.exit):
           print('Exiting')
           stop = True
        elif (cm == Command.help):
           setPos(Board.xpos, Board.ypos + Board.height + 2)
           print('To jest pomoc!')
        elif cm == Command.left:
           s.setDir(-1, 0)
        elif cm == Command.right:
           s.setDir(1, 0)
        elif cm == Command.up:
           s.setDir(0, -1)
        elif cm == Command.down:
           s.setDir(0, 1)
        elif cm == Command.clear:
          b.Clear()
          b.drawBorder()
        elif cm == Command.menu:
          sel = -1
          menu(mnu, sel)
        elif cm == Command.sel1:
          sel = 1
          speed = 0.1
          menu(mnu, sel)
        elif cm == Command.sel2:
          sel = 2
          speed = 0.2
          menu(mnu, sel)
        elif cm == Command.sel3:
          sel = 3
          s.snakeLen += 1
          menu(mnu, sel)
        elif cm == Command.sel4:
          sel = 4
          s.snakeLen -= 1
          if (s.snakeLen < 2):
            s.snakeLen = 2
          menu(mnu, sel)
        elif cm == Command.genitems:
          b.genItems()
        elif cm == Command.showitems:
          b.showItems()
        elif cm == Command.boom:
          Board.boom()
#          input("---- B O O O O M ----\nPress [Enter]")
#          stop = True 
        elif cm == Command.annotations:
          setPos(0, 30)
          print('\n'.join('\n\n\n\n\n\n'))
#          help(Board)
          help(MySnake)
          input("Press [Enter]")

     time.sleep(speed)

     s.moveSnake()
     s.showSnake()

if __name__ == '__main__':
   doGame()
