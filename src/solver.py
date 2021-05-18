from time import sleep

from puzzle import Puzzle
from constants import *

class Solver:
  def __init__(self, puzzle, verbose=False, sleep=False):
    self.puzzle = puzzle
    self.verbose = verbose
    self.sleep = sleep

  def substep(self, speile, info):
      # if info is 1 2 1
      # there needs to be at least a cross in the interior gaps: 1 x 2 x 1
      common_square = [  1 for _ in speile]
      common_cross  = [ -1 for _ in speile]
      for guess in self.puzzle.candidates(info, speile):
        # Merge the common solution
        common_square = [SQUARE if c == SQUARE and g == SQUARE else KEINE for c, g in zip(common_square, guess)]
        common_cross =  [CROSS  if c == CROSS  and g == CROSS  else KEINE for c, g in zip(common_cross, guess)]
      # Add the common cells together
      return [cx + cs for cx, cs in zip(common_cross, common_square)]

  def step(self):
    def handle(offset, changes, row):
      if any(changes):
        self.puzzle.board.set(offset, changes, row=row)
        if self.verbose:
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
    old = None
    while not self.puzzle.verify():
      if self.puzzle.board == old:
        return self.puzzle
      old = self.puzzle.board[:]
      self.step()
    return True