import click

from solver import Solver
from puzzle import Puzzle

@click.command()
@click.argument('puzzles', nargs=-1, type=click.File('rt'))
@click.option("-s", "--sleep", default=0.1)
def solve(puzzles, sleep):
  for puzzle in puzzles:
    puzzle = Puzzle.load(puzzle)
    s = Solver(puzzle, verbose=True, sleep=sleep)
    s.solve()

if __name__ == "__main__":
  solve()
