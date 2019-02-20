import sys, pygame
import random
import copy 

board0 = []
board1 = []
board2 = []
dly = 50
d = 8
k = 8
eqCount = 0
background = 1, 1, 1

wrapx = True
wrapy = True

size = width, height = 64 * k, 32 * k
nx = int(width  / d)
ny = int(height / d)
#pal = [(0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 0, 255), (0, 255, 255), (0, 255, 255), (255, 255, 255)]
pal = [(0, 0, 0), 
       (255, 255, 255), (239, 239, 239), (223, 223, 223), (207, 207, 207), 
       (  0, 255, 255), (  0, 239, 239), (  0, 223, 223), (  0, 207, 207), 
       (255,   0, 255), (239,   0, 239), (223,   0, 223), (207,   0, 207), 
       (255, 255,   0), (239, 239,   0), (223, 223,   0), (207, 207,   0), 
       (  0,   0, 255), (  0,   0, 239), (  0,   0, 223), (  0,   0, 207), 
       (255,   0,   0), (239,   0,   0), (223,   0,   0), (207,   0,   0), 
       (  0, 255,   0), (  0, 239,   0), (  0, 223,   0), (  0, 207,   0), 
       (191, 191, 191), (175, 175, 175), (159, 159, 159), (143, 143, 143), 
       (191, 191, 191), (175, 175, 175), (159, 159, 159), (143, 143, 143), 
       (191, 191, 191), (175, 175, 175), (159, 159, 159), (143, 143, 143), 
       (191, 191, 191), (175, 175, 175), (159, 159, 159), (143, 143, 143), 
       (127, 127, 127), (111, 111, 111), (95, 95, 95),    (79, 79, 79)]

c = [ 32 * n - 1 for n in range(2, 9)]
b = [((a & 4) >> 2, (a & 2) >> 1, a & 1) for a in range(1, 8)]

def getPal0():
  pl = [(0, 0, 0)]
  for ic in reversed(c):
    for ib in b:
      pl.append((ib[0] * ic, ib[1] * ic, ib[2] * ic))
  return pl

def getColor(x):
  r = 0.0
  g = 0.0
  b = 1.0
  if (x >= 0.0 and x < 0.2):
    x = x / 0.2
    r = 0.0
    g = x
    b = 1.0
  elif (x >= 0.2 and x < 0.4):
    x = (x - 0.2) / 0.2
    r = 0.0
    g = 1.0
    b = 1.0 - x;
  elif (x >= 0.4 and x < 0.6):
    x = (x - 0.4) / 0.2
    r = x
    g = 1.0
    b = 0.0
  elif (x >= 0.6 and x < 0.8):
    x = (x - 0.6) / 0.2
    r = 1.0
    g = 1.0 - x;
    b = 0.0
  elif (x >= 0.8 and x <= 1.0):
    x = (x - 0.8) / 0.2
    r = 1.0
    g = 0.0
    b = x
  col = (int(255 * r), int(255 * g), int(255 * b))
#  print("{} -> ({})".format(x, col))
  return col

def getPal1(colCnt):
  pal = []
  for i in reversed(range(colCnt)):
     pal.append(getColor(1.0 * i / colCnt))
  return pal

def setIcon():
  icon = pygame.Surface((32,32))
  icon.set_colorkey((0,0,0)) #and call that color transparant
  icd = 4
  for i in range(0, 31, icd):
     for j in range(0, 31, icd):
#        icon.set_at((i,   j),   pal[random.randint(0, len(pal) - 1)])
        pygame.draw.rect(icon, pal[random.randint(0, len(pal) - 1)], (i, j, icd, icd), 0)
  pygame.display.set_icon(icon) #set wind

def initBoard(rnd):
  global board0, board1, board2
  print("initBoard({}, {}): {} {}".format(nx, ny, eqCount, len(board0)))
  pygame.display.set_caption("Life ({}, {})".format(nx, ny))
#  showDiffs()
  
  if len(board0) >= ny:
    board0 = board0[0:ny]

  while len(board0) < ny:
    board0.append(list())

  for y in range(ny):
    if len(board0[y]) >= nx:
      board0[y] = board0[y][0:nx]
    while len(board0[y]) < nx:
      board0[y].append(random.randint(0, 1))

  board2.clear()
  if (rnd):
    for y in range(ny):
      for x in range(nx):
        board0[y][x] = random.randint(0, 1)

def getNextState(board):
  rl = len(board)  
  ret = list()
  for iy in range(rl):
    row = list()
    for ix in range(len(board[iy])):
      s = 0
      for iiy in [-1, 0, 1]:
         if not(wrapy) and (iy + iiy < 0 or iy + iiy >= ny):
            continue
         for iix in [-1, 0, 1]:
           if not(wrapx) and (ix + iix < 0 or ix + iix >= nx):
              continue
           if board[(ny + iy + iiy) % ny][(nx + ix + iix) % nx] != 0 and not(iix == 0 and iiy == 0):
              s += 1
      if (s == 3):
        row.append(board[iy][ix] + 1)
      elif (s == 2 and board[iy][ix] != 0):
        row.append(board[iy][ix] + 1)
      else:
        row.append(0)
    ret.append(row)
  return ret 

def doNext():
  global board0, board1, board2, eqCount
  board2 = copy.deepcopy(board1)
  board1 = copy.deepcopy(board0)
  board0 = getNextState(board0)

#  showDiffs()
  eq01 = False
  eq02 = False
  if (compare(board0, board1)):
#    print('board0 == board1 ({:9}, {:9}, {:9})'.format(id(board0), id(board1), id(board2)))
    eq01 = True
  if (compare(board0, board2)):
#    print('board0 == board2 ({:9}, {:9}, {:9})'.format(id(board0), id(board1), id(board2)))
    eq02 = True

  if (eq01 or eq02):
    eqCount += 1
    if (eqCount > 9):
#      initBoard(True)
      pattern(-1)
      eqCount = 0

  screen.fill((32, 64, 32))  

  for iy in range(len(board0)):
    for ix in range(len(board0[iy])):
      if (board0[iy][ix] != 0):
         pygame.draw.rect(screen, pal[board0[iy][ix] % len(pal)], (0 + d * ix, height - d - d * iy, d - 1, d - 1), 0)
      else:
         pygame.draw.rect(screen, background, (0 + d * ix, height - d - d * iy, d - 1, d - 1), 0)
  pygame.display.flip()

def showDiffs():
  for y in range(min(len(board0), len(board1), len(board2))):
    if (board0[y] != board1[y] or board0[y] != board2[y]):
      print("row {}".format(y))
      print("".join([str(d) for d in board0[y]]))
      print("".join([str(d) for d in board1[y]]))
      print("".join([str(d) for d in board2[y]]))

def compare(a0, a1):
  l = len(a0)
  if (len(a1) != l):
    return False
  for y in range(l):
    ll = len(a0[y])
    if (len(a1[y]) != ll):
      return False
    for x in range(ll):
      if ((a0[y][x] != 0 and a1[y][x] == 0) or (a0[y][x] == 0 and a1[y][x] != 0)):
        return False
  return True

def pattern(sel):
  global board0
  lx = int(nx / 2)
  ly = int(ny / 2)
  if sel == -1:
    sel = random.randint(0, 1)

  if sel == 0:
    board0[ly + 0][lx + 0] = 3  #
    board0[ly + 1][lx + 0] = 3 #
    board0[ly + 2][lx + 1] = 3 ###
    board0[ly + 0][lx + 1] = 3
    board0[ly + 0][lx + 2] = 3
  if sel == 1:
    board0[ly + 0][lx + 0] = 3  #  #
    board0[ly + 1][lx + 0] = 3 #
    board0[ly + 2][lx + 0] = 3 #   #
    board0[ly + 3][lx + 1] = 3 ####
    board0[ly + 0][lx + 1] = 3
    board0[ly + 0][lx + 2] = 3
    board0[ly + 0][lx + 3] = 3
    board0[ly + 1][lx + 4] = 3
    board0[ly + 4][lx + 4] = 3

#pal = getPal0()
pal = getPal1(32)
  
pygame.init()

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

initBoard(True)

pygame.display.flip()

while 1:
    for event in pygame.event.get():
#        print(event)
        if event.type == pygame.QUIT: 
           sys.exit()
        elif event.type == pygame.KEYUP:
           if event.key == 27: 
             sys.exit() 
           elif event.key == pygame.K_0:
             changePat(0)
           elif event.key == pygame.K_1:
             changePat(1)
           elif event.key == pygame.K_2:
             changePat(2)
           elif event.key == pygame.K_3:
             changePat(3)
           elif event.key == pygame.K_g:
             pattern(-1)
           elif event.key == pygame.K_s:
             showDiffs()
           elif event.key == pygame.K_x:
             wrapx = not(wrapx)
             print("wrapx = {}".format(wrapx))
           elif event.key == pygame.K_y:
             wrapy = not(wrapy)
             print("wrapy = {}".format(wrapy))
           elif event.key == pygame.K_SPACE:
             initBoard(True)
           elif event.key == pygame.K_UP:
             pygame.display.flip()
           elif event.key == pygame.K_DOWN:
             pygame.display.flip()
           elif event.key == pygame.K_RIGHT:
             pygame.display.flip()
           elif event.key == pygame.K_LEFT:
             pygame.display.flip()
           elif event.key == pygame.K_EQUALS:
             dly = int(dly * .8)
             print("delay: {}".format(dly))
           elif event.key == pygame.K_MINUS:
             if (dly == int(dly * 1.2)):
                dly += 1
             else:
                dly = int(dly * 1.2)
             print("delay: {}".format(dly))
        if event.type == pygame.MOUSEBUTTONUP: 
          mnx = int(event.pos[0] / d)
          mny = int((height - event.pos[1] - 1) / d)
          print('mouse: {}, ({}, {})'.format(event.pos, mnx, mny))
          board0[mny][mnx] = 1

#           sys.exit()
        elif event.type == pygame.VIDEORESIZE:
          width = event.w
          height = event.h
          size = width, height 
          nx = int(width  / d)
          ny = int(height / d)
          setIcon()
          initBoard(False)
          screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    doNext()
    pygame.time.delay(dly)
