import click

from nanogram import Nanogram

@click.command()
@click.argument('puzzles', nargs=-1, type=click.File('rt'))
@click.option("-s", "--sleep", default=0.1)
def solve(puzzles, sleep):
  for puzzle in puzzles:
    N = Nanogram.load(puzzle, sleep=sleep)
    N.solve()

if __name__ == "__main__":
  solve()
