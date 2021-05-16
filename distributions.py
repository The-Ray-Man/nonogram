import itertools
from dists import pc

def distribution(boxes, balls):
  return pc[boxes][balls]

def _distribution(boxes, balls):
  rng = list(range(balls + 1)) * boxes
  dist = set(i for i in itertools.permutations(rng, boxes) if sum(i) == balls)
  return dist


def precompute():
  table = {}
  for box in range(6):
    table[box] = {}
    for ball in range(20-box):
      print(box, ball)
      table[box][ball] = _distribution(box, ball)
  with open("dists.py", "wt") as f:
    f.write(str(table))

