import os
from collections import defaultdict


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()

buffer = '#' * len(input[0])
input.append(buffer)
input.insert(0, buffer)

state = {}
for y, row in enumerate(input):
    for x, spot in enumerate(row):
        if spot == '#':
            state[x, y] = spot
        elif spot == '>':
            state[x, y] = 'r'
        elif spot == '<':
            state[x, y] = 'l'
        elif spot == '^':
            state[x, y] = 'u'
        elif spot == 'v':
            state[x, y] = 'd'
        else:
            state[x, y] = ''


def printer(state):
    for y in range(max(state.keys(), key=lambda x: x[1])[1] + 1):
        row = ''
        for x in range(max(state.keys(), key=lambda x: x[0])[0] + 1):
            if state[x, y]:
                if len(state[x, y]) != 1:
                    row += str(len(state[x, y]))
                else:
                    row += state[x, y]
            else:
                row += '.'
        print(row)
    print()

STATES = 1000
puzzle = []
puzzle.append(state)

for i in range(STATES):
    if i % 100 == 0:
        print(i, '/', STATES)
    next_state = {}
    for y, row in enumerate(input):
        for x, spot in enumerate(row):
            next_state[x, y] = ''
    for (x, y), z in state.items():
        if z == '#' or not z:
            next_state[x, y] += z
        else:
            dirs = list(z)
            for dir in dirs:
                if dir == 'l':
                    if state[x-1, y] == '#':
                        next_state[len(input[0]) - 2, y] += 'l'
                    else:
                        next_state[x-1, y] += 'l'
                elif dir == 'r':
                    if state[x+1, y] == '#':
                        next_state[1, y] += 'r'
                    else:
                        next_state[x+1, y] += 'r'
                elif dir == 'u':
                    if state[x, y-1] == '#':
                        next_state[x, len(input) - 3] += 'u'
                    else:
                        next_state[x, y-1] += 'u'
                elif dir == 'd':
                    if state[x, y+1] == '#':
                        next_state[x, 2] += 'd'
                    else:
                        next_state[x, y+1] += 'd'
    state = next_state
    puzzle.append(state)
    # printer(state)


DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
END = (len(input[0]) - 2, len(input) - 2)
START = (1, 1)
locations = [START]
part_1 = True
part_2 = False
part_3 = False
for round in range(STATES):
    # if round % 100 == 0:
    #     print(round, '/', STATES, len(locations), max(locations), max(locations, key=lambda x: x[1]))
    next_locations = set()
    while locations:
        location = locations.pop()
        for dir in DIRS:
            next_location = (location[0] + dir[0], location[1] + dir[1])
            if puzzle[round + 1][next_location] == '':
                next_locations.add(next_location)
    if part_1:
        if END in next_locations:
            print("Part 1:", round + 1)
            part_1 = False
            part_2 = True
            next_locations = [END]
    elif part_2:
        if START in next_locations:
            part_2 = False
            part_3 = True
            next_locations = [START]
    elif part_3:
        if END in next_locations:
            print("Part 2:", round + 1)
            break
    locations = list(next_locations)

# import pdb; pdb.set_trace()