# nonogram

## Installation
With [Poetry](https://github.com/python-poetry/poetry)
```
git clone https://github.com/The-Ray-Man/nonogram.git
cd nonogram
poetry install
```
## Running
```
cd src
python main.py ../examples/pharaoh.toml
```
## Puzzle format
```toml
name = "piggy"
size = [5,5]
horizontal = [[1,3],[5],[2,2],[5],[1,1]]
vertical = [[4],[4],[2,1],[5],[4]]
```
