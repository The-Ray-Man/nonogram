from constants import KEINE, translate
from itertools import groupby
from tabulate import tabulate

class Board(list):
    def __init__(self, size, data=None):
        self.w, self.h = size
        for y in range(self.h):
            if data is None:
                self.append([KEINE for x in range(self.w)])
            else:
                self.append(data[y])

    def __str__(self):
        return tabulate(list(map(translate, self)), tablefmt="fancy_grid", stralign="center")

    def done(self):
        return all(i != KEINE for line in self for i in line)

    def set(self, offset, speile, row=True):
        if row:
            self[offset] = speile
        else:
            for b, s in zip(self, speile):
                b[offset] = s

    def constraints(self):
        def transform(group):
            return list(map(lambda x: x[1], filter(lambda x: x[0]==1, ((k, len(list(g))) for k, g in group))))
        vertical = [transform(groupby(row)) for row in self]
        cols = [[self[y][x] for y in range(self.h)] for x in range(self.w)]
        horizontal = [transform(groupby(col)) for col in cols]
        return horizontal, vertical
