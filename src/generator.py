from random import choice

from board import Board

rng = lambda: choice([-1, 1])

class RandomBoard(Board):
    def __init__(self, size):
        data = [[rng() for x in range(size[0])] for y in range(size[1])]
        super().__init__(size, data)
