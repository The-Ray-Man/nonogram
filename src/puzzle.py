import toml
from tabulate import tabulate

from constants import *
from board import Board

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

