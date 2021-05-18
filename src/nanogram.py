from tabulate import tabulate
from time import sleep
import toml

from distributions import distribution
from constants import *
from board import Board

# TODO verify function


class Puzzle:
  def __init__(self, horizontal, vertical, **kwargs):
    self.horizontal = horizontal
    self.vertical = vertical
    self.board = Board((len(self.horizontal), len(self.vertical)))

  def __str__(self):
    def translate(row):
      row = ["■" if e == SQUARE else e for e in row]
      row = ["⛌" if e == CROSS else e for e in row]
      return ["" if e == KEINE else e for e in row]
    field = [[v] + translate(row) for v, row in zip(self.vertical, self.board)]
    return tabulate(field, headers=self.horizontal, tablefmt="fancy_grid", stralign="center")

  @classmethod
  def load(cls, path, **kwargs):
    data = toml.load(path)
    return cls(data["horizontal"], data["vertical"], **kwargs)


class Solver:
  def __init__(self, puzzle, sleep=0):
    self.puzzle = puzzle
    self.sleep = sleep or False

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
        self.puzzle.board.set(offset, changes, row=row)
        self.pprint()
    for y, row in enumerate(self.puzzle.board):
      handle(y, self.substep(row, self.puzzle.vertical[y]), row=True)
    for x in range(len(self.puzzle.board)):
      handle(x, self.substep([self.puzzle.board[y][x] for y in range(len(self.puzzle.board))], self.puzzle.horizontal[x]), row=False)

  def pprint(self):
      print(chr(27) + "[2J" + str(self.puzzle), end='\n\r') # Print inplace and the escape sequence clears the screen
      if self.sleep:
        sleep(self.sleep)

  def solve(self):
    # Iteratively applies constraints
    while not self.puzzle.board.done():
      self.step()