from tabulate import tabulate
from distributions import distribution
from time import sleep
import toml

SLEEP = .05

SQUARE = 1
CROSS = -1
KEINE = 0

# TODO verify function

def translate(row):
    row = ["■" if e == SQUARE else e for e in row]
    row = ["⛌" if e == CROSS else e for e in row]
    return ["" if e == KEINE else e for e in row]

class Nanogram:
  def __init__(self, horizontal, vertical, **kwargs):
    self.horizontal = horizontal
    self.vertical = vertical
    self.board = [[KEINE for v in range(len(self.vertical))] for h in range(len(self.horizontal))]
    self.sleep = kwargs["sleep"] or SLEEP
    self._old = None

  @classmethod
  def load(cls, path, **kwargs):
    data = toml.load(path)
    return cls(data["horizontal"], data["vertical"], **kwargs)

  def __str__(self):
    field = [[v] + translate(row) for v, row in zip(self.vertical, self.board)]
    return tabulate(field, headers=self.horizontal, tablefmt="fancy_grid", stralign="center")

  def _check(self, speile, info, offset, row):
      # if info is 1 2 1
      # there needs to be at least a cross in the interior gaps: 1 x 2 x 1
      mask = [KEINE] + [SQUARE for _ in range(len(info) -1 )] + [KEINE]
      balls = len(speile) - sum(mask) - sum(info)
      boxes = len(mask)
      common_square = [  1 for _ in speile]
      common_cross  = [ -1 for _ in speile]
      for dist in distribution(boxes, balls):
        dist = [ di + mi for di, mi in zip(dist, mask)]
        data = [[CROSS] * d + [SQUARE] * i for i, d in zip(info, dist)]
# [[CROSS] * dist[0]]
        print(info, dist, data)
        if not self.compare_speile(data, speile):
          continue 
        for i in range(len(data)):
          common_square[i] &= data[i] if data[i] == SQUARE else 0
          if common_cross[i] == -1:
            common_cross[i] = -1 if data[i] == -1 else 0 
      self.set(offset, [cx + cs for cx, cs in zip(common_cross, common_square)], row=row)
      # self.pprint()

  def step(self):
    for y, row in enumerate(self.board):
      self._check(row, self.vertical[y], y, row=True)
    for x in range(len(self.board)):
      temp = [self.board[y][x] for y in range(len(self.board))]
      self._check(temp, self.horizontal[x], x, row=False)
    

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

