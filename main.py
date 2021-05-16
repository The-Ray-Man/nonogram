from example import get_example
from nanogram import *


def run_test(index):
  horizontal, vertical = get_example(index)
  N = Nanogram(horizontal, vertical)
  N.solve()

if __name__ == "__main__":
  run_test(2)