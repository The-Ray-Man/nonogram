from random import choice, shuffle

from board import Board

rng = lambda: choice([-1, 1])

# Experiment with distributions
class RandomBoard(Board):
    def __init__(self, size):
        x, y = size
        def row():
            row = [1] + [rng() for x in range(x - 1)]
            shuffle(row)
            return row
        data = [row() for y in range(y)]
        super().__init__(size, data)