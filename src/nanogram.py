from tabulate import tabulate
from distributions import distribution
from time import sleep
import toml

SLEEP = .05

SQUARE = 1
CROSS = -1
KEINE = 0

class Nanogram:
  @classmethod
  def load(cls, path, **kwargs):
    data = toml.load(path)
    return cls(data["horizontal"], data["vertical"], **kwargs)

  def __init__(self, horizontal, vertical, **kwargs):
    self.horizontal = horizontal
    self.vertical = vertical
    self.board = [[KEINE for v in range(len(self.vertical))] for h in range(len(self.horizontal))]
    self.sleep = kwargs["sleep"] or SLEEP
    self._old = None

  def __str__(self):
    field = [[self.vertical[y]] + self.board[y] for y in range(len(self.board))]
    field = [["■" if e == SQUARE else e for e in row] for row in field]
    field = [["⛌" if e == CROSS else e for e in row] for row in field]
    field = [["" if e == KEINE else e for e in row] for row in field]
    return tabulate(field, headers=self.horizontal, tablefmt="fancy_grid", stralign="center")

  def step(self):
    for y, row in enumerate(self.board):
      self._check(row, self.vertical[y], y, row=True)
    for x in range(len(self.board)):
      temp = [self.board[y][x] for y in range(len(self.board))]
      self._check(temp, self.horizontal[x], x, row=False)
    
  def _check(self, speile, info, offset, row):
      mask = [KEINE] + [SQUARE for _ in range(len(info) -1 )] + [KEINE]
      ball_in_mask = sum(mask)
      ball_left = len(speile) - ball_in_mask - sum(info)
      boxes = len(mask)
      dists =  distribution(boxes, ball_left)
      
      overall_data_square = [ 1 for i in range(len(speile) )]
      overall_data_cross = [ -1 for i in range(len(speile) )]
      overall_data = [ 0 for i in range(len(speile) )]
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
      self.pprint()

  def pprint(self):
      print(chr(27) + "[2J" + str(self), end='\n\r')
      sleep(self.sleep)

  @staticmethod
  def compare_speile(data, speile):
    for i_data, i_speile in zip(data, speile):
      if i_data != KEINE and i_speile != KEINE and i_speile != i_data:
        return False
    return True

  def done(self):
    if self.hash() == self._old:
      return True
    self._old = self.hash()
    for line in self.board:
      for x in line:
        if x == KEINE:
          return False
    return True

  def set(self, offset, speile, row=True):
    if row:
      self.board[offset] = speile
    else:
      for i in range(len(self.board)):
        self.board[i][offset] = speile[i]

  def hash(self):
    return "".join(map(str, self.board))

  def solve(self):
    while not self.done():
      self.step()

