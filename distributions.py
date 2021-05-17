import itertools
import pickle

DUMP_FILE = "precomputation.pyb"

# Old and inefficient version
def ddistribution(boxes, balls):
  rng = list(range(balls + 1)) * boxes
  dist = set(i for i in itertools.permutations(rng, boxes) if sum(i) == balls)
  return dist


def _distribution(boxes, balls):
    table = {}
    bucket = {tuple(0 for i in range(boxes))}
    for x in range(balls + 1):
        new_bucket = set()
        for b in bucket:
            for i in range(len(b)):
                n = list(b)
                n[i] += 1
                new_bucket.add(tuple(n))
        temp = bucket.copy()
        table[x] = temp
        bucket = new_bucket
    return table


def load():
    with open(DUMP_FILE, "rb") as f:
        return pickle.load(f)

def dump(table):
    with open(DUMP_FILE, "wb") as f:
        return pickle.dump(table, f)

# TODO find out what is needed for what board sizes in the worst case
# 10, 20
def precompute(boxes, balls):
    table = {}
    for b in range(boxes + 1):
        table[b] = _distribution(b, balls)
    return dump(table)

lookup = load()

def distribution(boxes, balls):
  return lookup[boxes][balls]
