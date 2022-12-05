import os
from collections import defaultdict
from copy import deepcopy


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    puzzle = f.read()

crates, directions = puzzle.split('\n\n')

directions = [
    {
        'amount': int(x[0].split(' ')[1]),
        'start': x[1].split(' to ')[0],
        'end': x[1].split(' to ')[1],
    }
    for x in [d.split(' from ') for d in directions.split('\n')]
]

crates = [list(x) for x in crates.split('\n')]

stacks = defaultdict(list)
for i, number in enumerate(crates[-1]):
    if number not in [' ', '[', ']']:
        for row in crates[:-1]:
            try:
                if row[i] not in [' ', '[', ']']:
                    stacks[number].insert(0, row[i])
            except IndexError:
                pass

stacks_2 = deepcopy(stacks)

for direction in directions:
    for _ in range(direction['amount']):
        crate = stacks[direction['start']].pop()
        stacks[direction['end']].append(crate)

part_1 = ''
for x in crates[-1]:
    if x not in [' ', '[', ']']:
        part_1 += stacks[x][-1]

print("Part 1:", part_1)


stacks = stacks_2

for direction in directions:
    intermediate = []
    for _ in range(direction['amount']):
        intermediate.append(stacks[direction['start']].pop())
    while intermediate:
        crate = intermediate.pop()
        stacks[direction['end']].append(crate)

part_2 = ''
for x in crates[-1]:
    if x not in [' ', '[', ']']:
        part_2 += stacks[x][-1]

print("Part 2:", part_2)
