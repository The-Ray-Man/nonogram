import toml
import click

from nanogram import Nanogram

def load_puzzle(path):
    data = toml.load(path)
    return Nanogram(data["horizontal"], data["vertical"])


@click.command()
@click.argument('puzzle', default="../examples/piggy.toml", type=click.File('rt'))
@click.option("-s", "--sleep", default=0.1)
def solve(puzzle, sleep):
    print(puzzle, sleep)
    N = load_puzzle(puzzle)
    N.solve()

if __name__ == "__main__":
  solve()
