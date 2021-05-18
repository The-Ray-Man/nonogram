import click

from nanogram import Puzzle, Solver

@click.command()
@click.argument('puzzles', nargs=-1, type=click.File('rt'))
@click.option("-s", "--sleep", default=0.1)
def solve(puzzles, sleep):
  for puzzle in puzzles:
    puzzle = Puzzle.load(puzzle)
    s = Solver(puzzle, sleep=sleep)
    s.solve()

if __name__ == "__main__":
  solve()
