from generator import RandomBoard
from puzzle import Puzzle
from solver import Solver

# b = RandomBoard((10, 10))
# print(b)
# c = b.constraints()
# print(c)
# p = Puzzle(*c)
# print(p)
# s = Solver(p)
# s.solve()

# unsolv = [[1, 1, 1, 1], [1, 2], [2, 2], [2, 2], [1, 2, 1, 1], [1, 3, 2], [2, 3, 1], [2, 1, 1, 1], [2, 1, 1], [2, 1]], [[1, 1, 1, 1], [1, 1, 1, 3], [1, 1, 1], [1, 2, 1], [1, 2, 1], [3, 3], [1, 1, 2], [4, 1], [1, 1], [1, 1, 1, 3]]
# up = Puzzle(*unsolv)
# s = Solver(up)
# s.solve()
# empties = s.puzzle.board.empty()
# print(empties)


# How to make a solution unique
# One option would be hints

# Not working anymore
# def unique_solution(board):
    # constraints = board.constraints()
    # puzzle = Puzzle(*constraints)
    # solver = Solver(puzzle)
    # res = solver.solve()
    # if res is True:
        # return True, solver.puzzle
    # return False, solver.puzzle

# Fuzzing
while True:
    print("Generating random board")
    r = RandomBoard((9, 15))
    print(r)
    p = Puzzle.from_board(r)
    print("Generated a puzzle from it")
    print(p)
    input()
    s = Solver(p, verbose=True)
    s.solve()
    print("Solved it")
    input()