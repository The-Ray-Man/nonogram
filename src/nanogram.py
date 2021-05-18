from tabulate import tabulate
from distributions import distribution
from time import sleep
import toml

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
    self.sleep = kwargs["sleep"] or False
    self._old = None

  @classmethod
  def load(cls, path, **kwargs):
    data = toml.load(path)
    return cls(data["horizontal"], data["vertical"], **kwargs)

  def __str__(self):
    field = [[v] + translate(row) for v, row in zip(self.vertical, self.board)]
    return tabulate(field, headers=self.horizontal, tablefmt="fancy_grid", stralign="center")

  def substep(self, speile, info):
      # if info is 1 2 1
      # there needs to be at least a cross in the interior gaps: 1 x 2 x 1
      mask = [KEINE] + [SQUARE for _ in range(len(info) -1 )] + [KEINE]
      balls = len(speile) - sum(mask) - sum(info)
      boxes = len(mask)
      common_square = [  1 for _ in speile]
      common_cross  = [ -1 for _ in speile]

      def inflate(crosses, info):
        data = [CROSS] * crosses[0]
        for i, d in zip(info, crosses[1:]):
          data.extend([SQUARE] * i + [CROSS] * d)
        return data

      def compatible(guess, speile):
        for i_data, i_speile in zip(guess, speile):
          if i_data != KEINE and i_speile != KEINE and i_speile != i_data:
            return False
        return True

      for dist in distribution(boxes, balls):
        # Add the mask and Convert the 'compressed' representation of crosses and squares to a row
        guess = inflate([d + m for d, m in zip(dist, mask)], info)

        # Checks if the guess is compatible with the partial solution
        if not compatible(guess, speile):
          continue 

        # Merge the common solution
        common_square = [SQUARE if c == SQUARE and g == SQUARE else KEINE for c, g in zip(common_square, guess)]
        common_cross =  [CROSS  if c == CROSS  and g == CROSS  else KEINE for c, g in zip(common_cross, guess)]
      # Add the common cells together
      return [cx + cs for cx, cs in zip(common_cross, common_square)]

  def step(self):
    def handle(offset, changes, row):
      if any(changes):
        self.set(offset, changes, row=row)
        self.pprint()
    for y, row in enumerate(self.board):
      handle(y, self.substep(row, self.vertical[y]), row=True)
    for x in range(len(self.board)):
      handle(x, self.substep([self.board[y][x] for y in range(len(self.board))], self.horizontal[x]), row=False)

  def pprint(self):
      print(chr(27) + "[2J" + str(self), end='\n\r') # Print inplace and the escape sequence clears the screen
      if self.sleep:
        sleep(self.sleep)

  def done(self):
    return all(i != KEINE for line in self.board for i in line)

  def set(self, offset, speile, row=True):
    if row:
      self.board[offset] = speile
    else:
      for b, s in zip(self.board, speile):
        b[offset] = s

  def hash(self):
    return "".join(map(str, self.board))

  def solve(self):
    # Iteratively applies constraints
    while not self.done():
      self.step()

