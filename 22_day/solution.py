import os
import re
from copy import copy
from pprint import pprint as pp

filename = "example_2.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()

directions_raw = input.pop()
directions = re.split('([LR])', directions_raw)
input.pop()

puzzle = [
    list(row) for row in input
]
max_line = max([len(y) for y in input])
for line in puzzle:
    if len(line) < max_line:
        for _ in range(max_line - len(line)):
            line.append(' ')

def get_password(loc, dir):
    row = loc['y'] + 1
    column = loc['x'] + 1
    facing_key = {
        '>': 0,
        'v': 1,
        '<': 2,
        '^': 3,
    }
    return 1000 * row + 4 * column + facing_key[dir]

def find_start(puzzle):
    row0 = puzzle[0]
    for x, tile in enumerate(row0):
        if tile == '.':
            return {'x': x, 'y': 0}, '>'

dir_rotation_key = {
    '>': {'R': 'v', 'L': '^'},
    'v': {'R': '<', 'L': '>'},
    '<': {'R': '^', 'L': 'v'},
    '^': {'R': '>', 'L': '<'},
}
dir_move_key = {
    '>': {'x': 1, 'y': 0},
    'v': {'x': 0, 'y': 1},
    '<': {'x': -1, 'y': 0},
    '^': {'x': 0, 'y': -1},
}

def next_spot(loc, dir):
    new_loc = copy(loc)
    while True:
        new_loc = {
            'x': new_loc['x'] + dir_move_key[dir]['x'],
            'y': new_loc['y'] + dir_move_key[dir]['y'],
        }
        if new_loc['x'] < 0:
            new_loc['x'] = len(puzzle[loc['y']]) - 1
        if new_loc['y'] < 0:
            new_loc['y'] = len(puzzle) - 1

        elif new_loc['x'] >= len(puzzle[loc['y']]):
            new_loc['x'] = 0
        elif new_loc['y'] >= len(puzzle):
            new_loc['y'] = 0


        if puzzle[new_loc['y']][new_loc['x']] == '.':
            return new_loc
        elif puzzle[new_loc['y']][new_loc['x']] == '#':
            return loc
        else:
            continue

loc, dir = find_start(puzzle)
for direction in directions:
    try:
        amount = int(direction)
        for _ in range(amount):
            loc = next_spot(loc, dir)
    except ValueError:
        dir = dir_rotation_key[dir][direction]

print("Part 1:", get_password(loc, dir))


## Part 2 ## (Only works on input)

def rotate_clockwise(square):
    result = []
    for y in len(result):
        row = []
        for x in len(result[0]):
            row.append(' ')
        result.append(row)

    # iterate through rows
    for i in range(len(square)):
        # iterate through columns
        for j in range(len(square[0])):
            result[j][i] = square[i][j]

    return result


SIDE = len(puzzle) // 4

SIDES = dict(
    SIDE_1_MIN_X = SIDE,
    SIDE_1_MAX_X = 2 * SIDE - 1,
    SIDE_1_MIN_Y = 0,
    SIDE_1_MAX_Y = SIDE - 1,

    SIDE_2_MIN_X = 2 * SIDE,
    SIDE_2_MAX_X = 3 * SIDE - 1,
    SIDE_2_MIN_Y = 0,
    SIDE_2_MAX_Y = SIDE - 1,

    SIDE_3_MIN_X = SIDE,
    SIDE_3_MAX_X = 2 * SIDE - 1,
    SIDE_3_MIN_Y = SIDE,
    SIDE_3_MAX_Y = 2 * SIDE - 1,

    SIDE_4_MIN_X = SIDE,
    SIDE_4_MAX_X = 2 * SIDE - 1,
    SIDE_4_MIN_Y = 2 * SIDE,
    SIDE_4_MAX_Y = 3 * SIDE - 1,

    SIDE_5_MIN_X = 0,
    SIDE_5_MAX_X = SIDE - 1,
    SIDE_5_MIN_Y = 2 * SIDE,
    SIDE_5_MAX_Y = 3 * SIDE - 1,

    SIDE_6_MIN_X = 0,
    SIDE_6_MAX_X = SIDE - 1,
    SIDE_6_MIN_Y = 3 * SIDE,
    SIDE_6_MAX_Y = 4 * SIDE - 1,
)

def on_face(face, loc):
    side_min_x = f'SIDE_{str(face)}_MIN_X'
    side_max_x = f'SIDE_{str(face)}_MAX_X'
    side_min_y = f'SIDE_{str(face)}_MIN_Y'
    side_max_y = f'SIDE_{str(face)}_MAX_Y'
    if (
        loc['x'] >= SIDES[side_min_x]
        and loc['x'] <= SIDES[side_max_x]
        and loc['y'] >= SIDES[side_min_y]
        and loc['y'] <= SIDES[side_max_y]
    ):
        return True
    return False


def next_spot_2(loc, dir, iterator = 0):
    new_loc = copy(loc)
    while True:
        new_loc = {
            'x': new_loc['x'] + dir_move_key[dir]['x'],
            'y': new_loc['y'] + dir_move_key[dir]['y'],
        }
        new_dir = dir

        # Side 1 - Checked
        if on_face(1, loc):
            if new_loc['x'] < SIDES['SIDE_1_MIN_X']:
                new_loc['x'] = SIDES['SIDE_5_MIN_X']
                new_loc['y'] = 3 * SIDE - loc['y'] - 1
                # y0 - y11, y3 - y8
                new_dir = '>'
            elif new_loc['y'] < SIDES['SIDE_1_MIN_Y']:
                new_loc['x'] = SIDES['SIDE_6_MIN_X']
                new_loc['y'] = loc['x'] + 2 * SIDE
                # x4 - y12, x7 - y15
                new_dir = '>'
        # Side 2
        elif on_face(2, loc):
            if new_loc['y'] < SIDES['SIDE_2_MIN_Y']:
                new_loc['y'] = SIDES['SIDE_6_MAX_Y']
                new_loc['x'] = loc['x'] - 2 * SIDE
                # x8 - x0, x11, x3
                new_dir = '^'
            elif new_loc['x'] > SIDES['SIDE_2_MAX_X']:
                new_loc['x'] = SIDES['SIDE_4_MAX_X']
                new_loc['y'] = 3 * SIDE - loc['y'] - 1
                # y0 - y11, y3 - y8
                new_dir = '<'
            elif new_loc['y'] > SIDES['SIDE_2_MAX_Y']:
                new_loc['x'] = SIDES['SIDE_3_MAX_X']
                new_loc['y'] = loc['x'] - SIDE
                # 8x - 4y, 11x - 7y
                new_dir = '<'
        # Side 3
        elif on_face(3, loc):
            if new_loc['x'] < SIDES['SIDE_3_MIN_X']:
                new_loc['x'] = loc['y'] - SIDE
                # 4y - 0x, 7y - 3x
                new_loc['y'] = SIDES['SIDE_5_MIN_Y']
                new_dir = 'v'
            elif new_loc['x'] > SIDES['SIDE_3_MAX_X']:
                new_loc['x'] = loc['y'] + SIDE
                # 4y - 8x, 7y - 11x
                new_loc['y'] = SIDES['SIDE_2_MAX_Y']
                new_dir = '^'
        # Side 4
        elif on_face(4, loc):
            if new_loc['x'] > SIDES['SIDE_4_MAX_X']:
                new_loc['x'] = SIDES['SIDE_2_MAX_X']
                new_loc['y'] = 3 * SIDE - loc['y'] - 1
                # y8 - y3, y11 - y0
                new_dir = '<'
            elif new_loc['y'] > SIDES['SIDE_4_MAX_Y']:
                new_loc['x'] = SIDES['SIDE_6_MAX_X']
                new_loc['y'] = loc['x'] + 2 * SIDE
                # 4x - 12y, 7x - 15y
                new_dir = '<'
        # Side 5
        elif on_face(5, loc):
            if new_loc['x'] < SIDES['SIDE_5_MIN_X']:
                new_loc['x'] = SIDES['SIDE_1_MIN_X']
                new_loc['y'] = 3 * SIDE - loc['y'] - 1
                # y8 - y3, y11 - y0
                new_dir = '>'
            elif new_loc['y'] < SIDES['SIDE_5_MIN_Y']:
                new_loc['x'] = SIDES['SIDE_3_MIN_X']
                new_loc['y'] = loc['x'] + SIDE
                # x0 - y4, x3 - y7
                new_dir = '>'
        # Side 6
        elif on_face(6, loc):
            if new_loc['x'] < SIDES['SIDE_6_MIN_X']:
                new_loc['x'] = loc['y'] - 2 * SIDE
                # y12 - x4, y15 - x7
                new_loc['y'] = SIDES['SIDE_1_MIN_Y']
                new_dir = 'v'
            elif new_loc['x'] > SIDES['SIDE_6_MAX_X']:
                new_loc['x'] = loc['y'] - 2 * SIDE
                # y12 - x4, y15 - x7
                new_loc['y'] = SIDES['SIDE_4_MAX_Y']
                new_dir = '^'
            elif new_loc['y'] > SIDES['SIDE_6_MAX_Y']:
                new_loc['x'] = loc['x'] + 2 * SIDE
                # x0 - x8, x3 - x11
                new_loc['y'] = SIDES['SIDE_2_MIN_Y']
                new_dir = 'v'

        if puzzle[new_loc['y']][new_loc['x']] == '.':
            return new_loc, new_dir
        elif puzzle[new_loc['y']][new_loc['x']] == '#':
            return loc, dir
        else:
            continue

i = 'start'
direction = 'none'
loc, dir = find_start(puzzle)

for iterator, direction in enumerate(directions):
    try:
        amount = int(direction)
        for i in range(amount):
            loc, dir = next_spot_2(loc, dir, iterator)
            # print(i + 1, "/", direction, loc, dir, iterator)
    except ValueError:
        dir = dir_rotation_key[dir][direction]
        # print("New dir", dir)

print("Part 2:", get_password(loc, dir))
