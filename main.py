import itertools
from tabulate import tabulate
from printField import printField

    
class Nanogram:
  def __str__(self):
    info = list()
    for y in range(len(self.board)):
        if len(self.vertical[y]) > 1:
            print(self.vertical[y])
            info.append([" ".join([ str(i) for i in self.vertical[y]])])
            print(info)
        else:
            print(self.vertical[y])
            info.append([str(self.vertical[y])])

    field = [info[y] + self.board[y] for y in range(len(self.board))]
    return tabulate(field, headers=self.horizontal)

  def __init__(self, horizontal, vertical):
    self.horizontal = horizontal
    self.vertical = vertical
    self.board = [[0 for v in range(len(vertical))] for h in range(len(horizontal))]
    # Initialize the board with padding
    # 1 : presente
    # 0 : idk
    #-1 : keine
    for i in range(len(self.board[0])):
      self.board[0][i] = -1
    for i in range(len(self.board)):
      self.board[i][0] = -1
      self.board[i][-1] = -1
    for i in range(len(self.board[-1])):
      self.board[-1][i] = -1

  def check(self):
    for y, row in enumerate(self.board):
      self._check(row, self.vertical[y], y, row=True)
    for x in range(len(self.board)):
      temp = [self.board[y][x] for y in range(len(self.board))]
      self._check(temp, self.horizontal[x], x, row=False)
  
      

    
  def _check(self, speile, info, offset, row):
      mask = [0] + [1 for _ in range(len(info) -1 )] + [0]
      ball_in_mask = sum(mask)
      ball_left = len(speile) - 2 - ball_in_mask - sum(info)
      boxes = len(mask)
      dist = distribution(boxes, ball_left)
      print("Row: ", offset, info)
      for d in dist:
        new = [ d[i] + mask[i] for i in range(len(d))]
        print(new, end=" ")
      print()
      if len(dist) == 1:
    
        data = [-1] + [-1] * new[0]
        for ih, h in enumerate(info):
          data.extend([1] * h)
          data.extend([-1] * new[ih+1])
          print(new[ih+1])
        data += [-1] * new[-1] + [-1]
        print("data", data)
        self.set(offset, data,row=row)

  def set(self, offset, speile, row=True):
    if row:
      self.board[offset] = speile
    else:
      for i in range(len(self.board)):
        print(speile[i])
        print(self.board[i][offset])
        self.board[i][offset] = speile[i]


def distribution(boxes, balls):
    rng = list(range(balls + 1)) * boxes
    dist = set(i for i in itertools.permutations(rng, boxes) if sum(i) == balls)
    return dist

N = Nanogram([[0],[1,3],[5],[2,2],[5],[1,1],[0]],
        [[0],[4],[4],[2,1],[5],[4],[0]])
print(N)
N.check()
print(N)
N.check()
print(N)