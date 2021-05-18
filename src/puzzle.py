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
        field = [[v] + translate(row) for v, row in zip(self.vertical, self.board)]
        return tabulate(field, headers=self.horizontal, tablefmt="fancy_grid", stralign="center")

    @classmethod
    def load(cls, path, **kwargs):
        data = toml.load(path)
        return cls(data["horizontal"], data["vertical"], **kwargs)

    @classmethod
    def from_board(cls, board):
        constraints = board.constraints()
        return cls(*constraints)

    def verify(self):
        """ Checks if all constrains are fulfilled """
        hor, ver = self.board.constraints()
        if ver != self.vertical or hor != self.horizontal:
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

