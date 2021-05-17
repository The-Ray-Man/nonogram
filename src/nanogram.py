from tabulate import tabulate
from distributions import distribution
from time import sleep

SLEEP = .05

SQUARE = 1
CROSS = -1
KEINE = 0

class Nanogram:
  def __str__(self):
    # trans = str.maketrans({SQUARE: "■", KEINE: "", CROSS: "⛌"})
    field = [[self.vertical[y]] + self.board[y][1:-1] for y in range(1, len(self.board) - 1)]
    field = [["■" if e == SQUARE else e for e in row] for row in field]
    field = [["⛌" if e == CROSS else e for e in row] for row in field]
    field = [["" if e == KEINE else e for e in row] for row in field]
    return tabulate(field, headers=self.horizontal[1:-1], tablefmt="fancy_grid", stralign="center")

  def __init__(self, horizontal, vertical):
    self.horizontal = [[0]] + horizontal + [[0]]
    self.vertical = [[0]] + vertical  + [[0]]
    self.board = [[KEINE for v in range(len(self.vertical))] for h in range(len(self.horizontal))]
    self.pre_dists = {
      "ROW": [None for _ in self.board],
      "COL": [None for _ in self.board],
    }
    for i in range(len(self.board[0])):
      self.board[0][i] = CROSS
      self.board[-1][i] = CROSS
    for i in range(len(self.board)):
      self.board[i][0] = CROSS
      self.board[i][-1] = CROSS
       

  def check(self):
    for y, row in enumerate(self.board):
      if y==0 or y==len(self.board)-1:
        continue
      self._check(row, self.vertical[y], y, row=True)
    for x in range(len(self.board)):
      if x==0 or x==len(self.board)-1:
        continue
      temp = [self.board[y][x] for y in range(len(self.board))]
      self._check(temp, self.horizontal[x], x, row=False)
    
  def _check(self, speile, info, offset, row):
      mask = [KEINE] + [SQUARE for _ in range(len(info) -1 )] + [KEINE]
      ball_in_mask = sum(mask)
      ball_left = len(speile) - 2 - ball_in_mask - sum(info)
      boxes = len(mask)
      dists =  distribution(boxes, ball_left)
      
      overall_data_square = [ 1 for i in range(len(speile) - 2)]
      overall_data_cross = [ -1 for i in range(len(speile) - 2)]
      overall_data = [ 0 for i in range(len(speile) - 2)]
      for d in dists:
        d = [ d[i] + mask[i] for i in range(len(d))]
        data = [CROSS] * d[0]
        for ih, h in enumerate(info):
          data.extend([SQUARE] * h)
          data.extend([CROSS] * d[ih+1])
        if not self.compare_speile(data, speile):
          continue 
        # data += [CROSS] * d[-1]
        for i in range(len(data)):
          overall_data_square[i] &= data[i] if data[i] == SQUARE else 0
          if overall_data_cross[i] == -1:
            overall_data_cross[i] = -1 if data[i] == -1 else 0 
      for i in range(len(overall_data_cross)):
        overall_data[i] = overall_data_cross[i] + overall_data_square[i]
      self.set(offset, overall_data,row=row)
      print(chr(27) + "[2J" + str(self), end='\r')
      sleep(SLEEP)


  @staticmethod
  def compare_speile(data, speile):
    for i_data, i_speile in zip(data, speile[1:-1]):
      if i_data != KEINE and i_speile != KEINE and i_speile != i_data:
        return False
    return True

  def done(self):
    for line in self.board:
      for x in line:
        if x == KEINE:
          return False
    return True

  def set(self, offset, speile, row=True):
    speile = [CROSS] + speile + [CROSS]
    if row:
      self.board[offset] = speile
    else:
      for i in range(len(self.board)):
        self.board[i][offset] = speile[i]

  def hash(self):
    return "".join(map(str, self.board))

  def solve(self):
    old = self.hash()
    while True:
      self.check()
      if self.hash() == old:
        break
      old = self.hash()
      if self.done():
        break




if __name__ == "__main__":
  N = Nanogram(
    [[0],[1,3],[5],[2,2],[5],[1,1],[0]],
        [[0],[4],[4],[2,1],[5],[4],[0]])
  N.solve()
