from functools import reduce
import os
from copy import copy


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()


grid = []
for row in rows:
    new_row = [int(x) for x in list(row)]
    grid.append(new_row)

def add_padding(grid):
    tb_padding = [-1 for x in range(len(grid[0]))]
    grid.insert(0, copy(tb_padding))
    grid.append(copy(tb_padding))

    for i in range(len(grid)):
        grid[i].insert(0, -1)
        grid[i].append(-1)

    return grid


grid = add_padding(grid)


def is_visible(x, y, x_d, y_d, grid):
    tree = grid[y][x]

    while True:
        x += x_d
        y += y_d

        if grid[y][x] >= tree:
            return False
        elif grid[y][x] == -1:
            return True



def visible_score(x, y, x_d, y_d, grid):
    tree = grid[y][x]
    total = 0

    while True:
        x += x_d
        y += y_d

        if grid[y][x] >= tree:
            return total + 1
        elif grid[y][x] == -1:
            return total
        else:
            total += 1


total_visible = 0  # part 1
view_scores = []  # part 2

DIRECTIONS = [
    [1, 0], [-1, 0], [0, 1], [0, -1]
]


for y, row in enumerate(grid):
    for x, tree in enumerate(row):
        if tree == -1:
            continue

        visible = False
        scores = []

        for dir in DIRECTIONS:
            if is_visible(x, y, dir[0], dir[1], grid):
                visible = True
            scores.append(visible_score(x, y, dir[0], dir[1], grid))

        if visible:
            total_visible += 1

        view_scores.append(reduce(lambda a, b: a * b, scores))

print("Part 1:", total_visible)
print("Part 2:", max(view_scores))
