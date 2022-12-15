import os
from collections import defaultdict
from copy import deepcopy


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    raw_ledges = f.read().splitlines()
ledges = [[[int(z) for z in y.split(',')] for y in x.split(' -> ')] for x in raw_ledges]


def find_rocks(r1, r2):
    rocks = []
    x1, y1 = r1
    x2, y2 = r2
    if x1 == x2:
        y1, y2 = sorted([y1, y2])
        for i in range(y2 - y1 + 1):
            rocks.append((x1, y1 + i))
    else:
        x1, x2 = sorted([x1, x2])
        for i in range(x2 - x1 + 1):
            rocks.append((x1 + i, y1))
    return rocks


def fill_in_rocks(ledges):
    all_rocks = set()
    for ledge in ledges:
        for i in range(len(ledge) - 1):
            rocks = find_rocks(ledge[i], ledge[i + 1])
            all_rocks.update(rocks)
    return all_rocks


rocks = fill_in_rocks(ledges)
_cave = defaultdict(lambda: '.')
for rock in rocks:
    _cave[rock] = '#'

cave = deepcopy(_cave)
SAND_START = (500, 0)
ABYSS = 0
for key in cave.keys():
    if key[1] > ABYSS:
        ABYSS = key[1]


def release_unit_of_sand():
    loc = SAND_START
    while loc[1] < ABYSS:
        next_loc_down = (loc[0], loc[1] + 1)
        next_loc_left = (loc[0] - 1, loc[1] + 1)
        next_loc_right = (loc[0] + 1, loc[1] + 1)
        if cave[next_loc_down] == '.':
            loc = next_loc_down
            continue
        else:
            if cave[next_loc_left] == '.':
                loc = next_loc_left
            elif cave[next_loc_right] == '.':
                loc = next_loc_right
            else:
                cave[loc] = 'o'
                return False
    return True


def printer(cave):
    print()
    for y in range(0, 13):
        line = []
        for x in range(480, 520):
            line.append(cave[(x, y)])
        print(''.join(line))


finished = False
sand = 0
while not finished:
    finished = release_unit_of_sand()
    sand += 1
    # printer(cave)
else:
    sand -= 1  # since we saw one fall off the cliff


print("Part 1:", sand)


### Part 2 ###
SOLID_FLOOR = ABYSS + 1
new_cave = deepcopy(_cave)

def release_unit_of_sand():
    loc = SAND_START
    cycles = -1
    while True:
        cycles += 1
        next_loc_down = (loc[0], loc[1] + 1)
        next_loc_left = (loc[0] - 1, loc[1] + 1)
        next_loc_right = (loc[0] + 1, loc[1] + 1)
        if new_cave[next_loc_down] == '.':
            loc = next_loc_down
            if loc[1] == SOLID_FLOOR:
                new_cave[loc] = 'o'
                return False
            continue
        else:
            if new_cave[next_loc_left] == '.':
                loc = next_loc_left
                if loc[1] == SOLID_FLOOR:
                    new_cave[loc] = 'o'
                    return False
            elif new_cave[next_loc_right] == '.':
                loc = next_loc_right
                if loc[1] == SOLID_FLOOR:
                    new_cave[loc] = 'o'
                    return False
            else:
                new_cave[loc] = 'o'
                if cycles == 0:
                    return True
                return False


from time import sleep

finished = False
sand = 0
while not finished:
    finished = release_unit_of_sand()
    sand += 1
    # printer(new_cave)
    # sleep(.05)


print("Part 2:", sand)