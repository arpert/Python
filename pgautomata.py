import sys, pygame
import random

line0 = []
line1 = []
pat = []
dly = 30

def changePat(n):
  if n in pat:
    pat.remove(n)
  else:
    pat.append(n) 

def initLine():
  global line0, line1
  line0.clear()
  for i in range(n):
    line0.append(random.randint(0, 1))

def getNextState(row):
  rl = len(row)  
  ret = []
  for i in range(rl):
    il = (i - 1 + rl) % rl
    ir = (i + 1 + rl) % rl
    s = row[il] + row[i] + row[ir]
    if (s in pat):
       ret.append(1)
    else:
       ret.append(0)
  return ret 

def doNext():
  global line0, line1
  line1 = getNextState(line0)
  if (line0 == line1):
    initLine()
    pygame.draw.rect(screen, (224, 0, 0), (0, height - d, width, d), 0)
    screen.scroll(0, -d)
    pygame.time.delay(dly)
  else:
    line0 = line1
#  print("".join([str(n) for n in line1]))  
  pygame.draw.rect(screen, (0, 0, 0), (0, height - d, width, d), 0)
  for i in range(len(line0)):
    if line0[i] == 1:
      pygame.draw.rect(screen, (127, 255, 127), (0 + d * i, height - d, d - 1, d - 1), 0)
  screen.scroll(0, -d)
  pygame.display.flip()

pygame.init()

k = 5
size = width, height = 64 * k, 48 * k
d = 4
n = int(width / d)

black = 32, 32, 32

screen = pygame.display.set_mode(size, pygame.RESIZABLE)

initLine()

pygame.display.flip()

while 1:
    for event in pygame.event.get():
        print(event)
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
           elif event.key == pygame.K_UP:
             screen.scroll(0, -d)
             pygame.display.flip()
           elif event.key == pygame.K_DOWN:
             screen.scroll(0, d)
             pygame.display.flip()
           elif event.key == pygame.K_RIGHT:
             screen.scroll(d, 0)
             pygame.display.flip()
           elif event.key == pygame.K_LEFT:
             screen.scroll(-d, 0)
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
#        if event.type == pygame.MOUSEBUTTONUP: 
#           sys.exit()
        elif event.type == pygame.VIDEORESIZE:
          width = event.w
          height = event.h
          size = width, height 
          n = int(width / d)
          initLine()
          screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    doNext()
    pygame.time.delay(dly)
