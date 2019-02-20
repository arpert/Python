import math
import random
import sys

##############################################################################
imgLoc = "{{imgLoc"
t = [None, None, None, None, None]
toRoll = [True, True, True, True, True]

def showDices(tb):
#   print('  ' + '     '.join(map((lambda f: '#' if f else ' '), toRoll)))
   l1 = ['   ', '   ', '*  ', '*  ', '* *', '* *', '* *']
   l2 = ['   ', ' * ', '   ', ' * ', '   ', ' * ', '* *']
   l3 = ['   ', '   ', '  *', '  *', '* *', '* *', '* *']
   for i in range(0, len(tb)):
      print('+---+ ', end = '')
   print()

   for i in range(0, len(tb)):
      print('|%s| ' % l1[tb[i]], end = '')
   print()
   for i in range(0, len(tb)):
      print('|%s| ' % l2[tb[i]], end = '')
   print()
   for i in range(0, len(tb)):
      print('|%s| ' % l3[tb[i]], end = '')
   print()

   for i in range(0, len(tb)):
      print('+---+ ', end = '')
   print()
   for i in range(0, len(tb)):
      if toRoll[i]:
         print('  %d   ' % (i + 1), end = '')
      else:
         print(' [%d]  ' % (i + 1), end = '')
   print()

     

def doRoll():
#      alert("Rolling...")
   for i in range(0, 5):
      if toRoll[i]:
        n = random.randint(1, 6)
        t[i] = n;
   
   t.sort();
   print('  ' + '     '.join([str(l) for l in t]))

   showDices(t)
   
   calcResults(t);


def calcResults(roll):
  hstr = "";
  
  n_1 = 0;
  n_2 = 0;
  n_3 = 0;
  n_4 = 0;
  n_5 = 0;
  n_6 = 0;
  sum = 0;
  for i in range(0, len(roll)):
     if (roll[i] == 1): n_1 += 1;
     if (roll[i] == 2): n_2 += 1;
     if (roll[i] == 3): n_3 += 1;
     if (roll[i] == 4): n_4 += 1;
     if (roll[i] == 5): n_5 += 1;
     if (roll[i] == 6): n_6 += 1;
     sum += roll[i];
  
  # Aces: The sum of dice with the number 1
  hstr += "Aces . . . . . . : " + "%2d" % (1 * n_1) + "\n";

  # Twos: The sum of dice with the number 2
  hstr += "Twos . . . . . . : " + "%2d" % (2 * n_2) + "\n";

  # Threes: The sum of dice with the number 3
  hstr += "Threes . . . . . : " + "%2d" % (3 * n_3) + "\n";

  # Fours: The sum of dice with the number 4
  hstr += "Fours  . . . . . : " + "%2d" % (4 * n_4) + "\n";

  # Fives: The sum of dice with the number 5
  hstr += "Fives  . . . . . : " + "%2d" % (5 * n_5) + "\n";

  # Sixes: The sum of dice with the number 6
  hstr += "Sixes  . . . . . : " + "%2d" % (6 * n_6) + "\n";

  #Three Of A Kind: At least three dice the same - Sum of all dice
  n = 0;
  if (n_1 >= 3 or n_2 >= 3 or n_3 >= 3 or n_4 >= 3 or n_5 >= 3 or n_6 >= 3):
     n = sum;
  hstr += "Three Of A Kind  : " + "%2d" % (n) + "\n";

  #Four Of A Kind: At least four dice the same - Sum of all dice
  n = 0;
  if (n_1 >= 4 or n_2 >= 4 or n_3 >= 4 or n_4 >= 4 or n_5 >= 4 or n_6 >= 4):
     n = sum;
  hstr += "Four Of A Kind . : " + "%2d" % (n) + "\n";

  #Full House: Three of one number and two of another 25
  if (  (n_1 > 2 and (           n_2 > 1 or n_3 > 1 or n_4 > 1 or n_5 > 1 or n_6 > 1))
     or (n_2 > 2 and (n_1 > 1            or n_3 > 1 or n_4 > 1 or n_5 > 1 or n_6 > 1))
     or (n_3 > 2 and (n_1 > 1 or n_2 > 1            or n_4 > 1 or n_5 > 1 or n_6 > 1))
     or (n_4 > 2 and (n_1 > 1 or n_2 > 1 or n_3 > 1            or n_5 > 1 or n_6 > 1))
     or (n_5 > 2 and (n_1 > 1 or n_2 > 1 or n_3 > 1 or n_4 > 1            or n_6 > 1))
     or (n_6 > 2 and (n_1 > 1 or n_2 > 1 or n_3 > 1 or n_4 > 1 or n_5 > 1           )) ):
    n = 25
  else: n = 0;
  hstr += "Full House . . . : " + "%2d" % (n) + "\n";

  n = 0;
  smSt = 0
  if (  (n_1 > 0 and n_2 > 0 and n_3 > 0 and n_4 > 0) 
     or (n_2 > 0 and n_3 > 0 and n_4 > 0 and n_5 > 0) 
     or (n_3 > 0 and n_4 > 0 and n_5 > 0 and n_6 > 0) ):
    smSt = 30

  # Small Straight: Four sequential dice (1-2-3-4, 2-3-4-5, or 3-4-5-6) - 30
  if (smSt > 0):
     n = 30;
  else: n = 0
  hstr += "Small Straight . : " + "%2d" % (n) + "\n";

  lgSt = 0
  if (  (n_1 > 0 and n_2 > 0 and n_3 > 0 and n_4 > 0 and n_5 > 0) 
     or (n_2 > 0 and n_3 > 0 and n_4 > 0 and n_5 > 0 and n_6 > 0) ):
    lgSt = 40
  # Large Straight: Five sequential dice (1-2-3-4-5 or 2-3-4-5-6) - 40
  if (lgSt > 0):
     n = 40;
  else: n = 0
  hstr += "Large Straight . : " + "%2d" % (n) + "\n";
  # Yahtzee: All five dice the same - 50
  n = 0
  if (n_1 == 5 or n_2 == 5 or n_3 == 5 or n_4 == 5 or n_5 == 5 or n_6 == 5):
     n = 50;
  hstr += "Yahtzee  . . . . : " + "%2d" % (n) + "\n";
  # Chance: Sum of all dice
  hstr += "Chance . . . . . : " + "%2d" % (sum) + "\n";

  print(hstr)

def doSelect():
  print("Enter dice numbers for roll : ", end = '')
  sel = input()
  st = []
  for i in range(0, len(toRoll)):
     toRoll[i] = False
  for sn in sel:
    if (sn >= '1' and sn <= '5'):
      si = int(sn)
      if si not in st:
        st.append(si)
        toRoll[si-1] = True
  print("Selected: %s" % str(st))
  
  doRoll()
  for i in range(0, len(toRoll)):
     toRoll[i] = True


def showHelp():
  print('Active keys:')
  print('[Enter] - Roll dices')
  print('S       - Select dice to roll')
  print('H       - Show help')
  print('[Space] - Exit')
  print('Q       - Quit ;)')
  print()


##############################################################################
def main():
   ch = 'h'
   start = True
   run = True
   while run:
     if (start):
       start = False
     else:
       ch = input()
     if (ch >= '0' and ch <= '9'):
       n = int(ch)
       showDices([n])
     elif (ch == ''):
       doRoll();
     elif (ch == 's' or ch == 'S'):
       doSelect();
     elif (ch.lower() == 'h'):
       showHelp();
     elif ch == ' ':
       run = False
     elif ch.lower() == 'q':
       run = False

if __name__ == '__main__':
    sys.exit(main())
