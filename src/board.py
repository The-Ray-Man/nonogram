from constants import *

class Board(list):
  def __init__(self, size, data=None):
    w, h = size
    for y in range(h):
      if data is None:
        self.append([KEINE for x in range(w)])
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
