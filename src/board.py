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
            k, g = group
            m = len(list(g))
            return list(map(lambda x: x[1], filter(lambda x: x[0]==1, (k, m))))
        horizonal = [[transform(groupby(row))] for row in self]
        vertical = [[transform(groupby(col))] for _ range(self.w)]
        return horizonal, vertical

    def __str__(self):
        field = [translate(row) for row in self]
        return tabulate(field, tablefmt="fancy_grid", stralign="center")

