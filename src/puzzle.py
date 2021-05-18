import toml
from tabulate import tabulate

from constants import *
from board import Board
from distributions import distribution

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

    def verify(self):
        """ Checks if all constrains are fulfilled """
        for group, constraint in zip(self.board.verify(), self.vertical + self.horizontal):
            squares = list(map(lambda x: x[1], filter(lambda x: x[0]==1, group)))
            if not constraint == squares:
                return False
        return self.board.done()

    def candidates(self, info, speile):
        mask = [KEINE] + [SQUARE for _ in range(len(info) -1 )] + [KEINE]
        balls = len(speile) - sum(mask) - sum(info)
        boxes = len(mask)
        def compatible(guess, speile):
            for i_data, i_speile in zip(guess, speile):
                if i_data != KEINE and i_speile != KEINE and i_speile != i_data:
                    return False
            return True
        def inflate(crosses, info):
            data = [CROSS] * crosses[0]
            for i, d in zip(info, crosses[1:]):
                data.extend([SQUARE] * i + [CROSS] * d)
            return data

        for dist in distribution(boxes, balls):
            # Add the mask and Convert the 'compressed' representation of crosses and squares to a row
            guess = inflate([d + m for d, m in zip(dist, mask)], info)
            # Checks if the guess is compatible with the partial solution
            if compatible(guess, speile):
                yield guess 

