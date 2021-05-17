import itertools

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

def precompute(boxes, balls):
    table = {}
    for b in range(boxes + 1):
        table[b] = _distribution(b, balls)
    return table

lookup = precompute(7, 16)

def distribution(boxes, balls):
  return lookup[boxes][balls]
