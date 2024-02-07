
board = ['>', '>', '>', ' ', '<', '<', '<']
solution = board.copy()
solution.reverse()

def show():
  print('\n' * 4)
  print('+---+---+---+---+---+---+---+')
  print('| ' + ' | '.join(board) + ' |')
  print('+---+---+---+---+---+---+---+')
#  print('+-1-+-2-+-3-+-4-+-5-+-6-+-7-+')
  print(' [1] [2] [3] [4] [5] [6] [7]   ([0] - Exit)')


def ruch(n):
   idx = n - 1
   pos = board.index(' ')
#   print('Zły wybór: {} = "{}"'.format(n, board[idx]))
   if pos != idx and abs(pos - idx) < 3:
      cell = board[idx]
      board[idx] = board[pos]
      board[pos] = cell
      return True
   else:  
     print('Zły wybór: {} = "{}"'.format(n, board[idx]))
     return False

def check():
   if '-'.join(board) == '-'.join(solution):
     return True
   else:
     return False
      

sel = '7'
print(solution, '\n', board)
cnt = 0
while sel != '0':
  show()
  print('Wybierz: ', end = '')
  sel = input()
  print("n: {}".format(sel))
  
  try:
    nsel = int(sel)
    print('nsel: {}'.format(sel))
    if nsel in range(len(board) + 1):
      if ruch(nsel):
         cnt += 1
         if (check()):
           print('Sukces!!!!, ruchów: {}'.format(cnt))
           exit()
  except Exception as ex:
    print('Zły wybór: {}'.format(sel), str(ex))