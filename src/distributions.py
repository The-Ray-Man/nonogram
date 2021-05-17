import pickle

DUMP_FILE = "precomputation.pyb"

"""
Precomputes all possible distributions and serializes and stores the resulting hashmap in a file.
The file will be loaded during startup and queries will be looked up.
"""

def add_ball_to_boxes(bucket):
    new_bucket = set()
    for b in bucket:
        for i in range(len(b)):
            n = list(b)
            n[i] += 1
            new_bucket.add(tuple(n))
    return new_bucket

def _distribution(boxes, max_balls):
    """ Computes all possiblities to distribute 0-max_balls into boxes """
    table = {}
    bucket = {tuple(0 for _ in range(boxes))}
    table[0] = bucket.copy()
    for ball in range(1, max_balls + 1):
        new_bucket = add_ball_to_boxes(bucket)
        table[ball] = new_bucket.copy()
        bucket = new_bucket
    return table


def load():
    with open(DUMP_FILE, "rb") as f:
        return pickle.load(f)

def dump(table):
    with open(DUMP_FILE, "wb") as f:
        return pickle.dump(table, f)

# TODO find out what is needed for what board sizes in the worst case
def precompute(max_boxes, max_balls):
    table = {}
    for box in range(max_boxes + 1):
        table[box] = _distribution(box, max_balls)
    return dump(table)

lookup = load()

def distribution(boxes, balls):
  return lookup[boxes][balls]
