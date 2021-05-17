import click

from nanogram import Nanogram

@click.command()
@click.argument('puzzle', default="../examples/piggy.toml", type=click.File('rt'))
@click.option("-s", "--sleep", default=0.1)
def solve(puzzle, sleep):
    print(puzzle, sleep)
    N = Nanogram.load(puzzle, sleep=sleep)
    N.solve()

if __name__ == "__main__":
  solve()
