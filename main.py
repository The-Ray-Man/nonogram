import itertools
from printField import printField


horizontal = [[0],[1,3],[5],[2,2],[5],[1,1],[0]]
vertical = [[0],[4],[4],[2,1],[5],[4],[0]]

# 0 => unknown
# 1 => box
# -1 => no box
field = [[0 for v in range(len(vertical))] for h in range(len(horizontal))]

for i in range(len(field[0])):
    field[0][i] = -1

for i in range(len(field)):
    field[i][0] = -1
    field[i][-1] = -1

for i in range(len(field[-1])):
    field[-1][i] = -1


def distribution(boxes, balls):
    rng = list(range(balls + 1)) * boxes
    dist = set(i for i in itertools.permutations(rng, boxes) if sum(i) == balls)
    return dist

def check(field, horizontal, vertical):
    for y, line in enumerate(field):
        mask = [0] + [1 for _ in range(len(horizontal[y]) -1 )] + [0]
        ball_in_mask = sum(mask)
        ball_left = len(line) - 2 - ball_in_mask - sum(horizontal[y])
        boxes = len(mask)
        dist = distribution(boxes, ball_left)
        for d in dist:
            print([ d[i] + mask[i] for i in range(len(d))], end=" ")
        print()
        if len(dist) == 1:


def set(field, )

printField(field, horizontal, vertical)

check(field, horizontal, vertical)