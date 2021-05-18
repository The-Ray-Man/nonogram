SQUARE = 1
CROSS = -1
KEINE = 0

def translate(row):
    row = ["■" if e == SQUARE else e for e in row]
    row = ["⛌" if e == CROSS else e for e in row]
    return ["" if e == KEINE else e for e in row]
