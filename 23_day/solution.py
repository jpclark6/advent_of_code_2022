import os
from collections import Counter

filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()

positions = set()
for y, line in enumerate(input):
    for x, spot in enumerate(list(line)):
        if spot == '#':
            positions.add((x, y))


def min_max(positions):
    min_x = min(positions, key=lambda spot: spot[0])[0]
    min_y = min(positions, key=lambda spot: spot[1])[1]
    max_x = max(positions, key=lambda spot: spot[0])[0]
    max_y = max(positions, key=lambda spot: spot[1])[1]
    return min_x, max_x, min_y, max_y

def printer(positions):
    min_x, max_x, min_y, max_y = min_max(positions)
    spots = set(positions)
    for y in range(min_y, max_y + 1):
        row = ''
        for x in range(min_x, max_x + 1):
            if (x, y) in spots:
                row += '#'
            else:
                row += '.'
        print(''.join(row))

def nobody_in_direction(elf, positions, condition):
    for c in condition.split('_'):
        next_check = [0, 0]
        if 'n' in c:
            next_check[1] -= 1
        if 'e' in c:
            next_check[0] += 1
        if 's' in c:
            next_check[1] += 1
        if 'w' in c:
            next_check[0] -= 1
        next_check = tuple([elf[0] + next_check[0], elf[1] + next_check[1]])
        if next_check in positions:
            return False
    return True


def part_1_and_2(positions, rounds):
    conditions = [{'dir': 'n_ne_nw', 'coords': (0, -1)}, {'dir': 's_se_sw', 'coords': (0, 1)}, {'dir': 'w_nw_sw', 'coords': (-1, 0)}, {'dir': 'e_ne_se', 'coords': (1, 0)}]
    # printer(positions)
    part_2 = set()
    for r in range(rounds):
        next_positions = {}
        for elf in positions:
            if nobody_in_direction(elf, positions, 'n_ne_e_se_s_sw_w_nw'):
                next_positions[elf] = elf
                continue
            dont_move = True
            for condition in conditions:
                if nobody_in_direction(elf, positions, condition['dir']):
                    next_positions[elf] = (elf[0] + condition['coords'][0], elf[1] + condition['coords'][1])
                    dont_move = False
                    break
            else:
                if dont_move:
                    next_positions[elf] = elf

        position_counts = Counter()
        for _, position in next_positions.items():
            position_counts[position] += 1
        new_positions = {}
        for elf, next_position in next_positions.items():
            if position_counts[next_position] != 1:
                new_positions[elf] = elf
            else:
                new_positions[elf] = next_position

        positions = set(new_positions.values())

        if positions in part_2:
            return str(r + 1) + ' rounds'
        part_2.add(frozenset(positions))

        first = conditions.pop(0)
        conditions.append(first)

        # print('*'*30)
        # printer(positions)

    min_x, max_x, min_y, max_y = min_max(positions)
    count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) in positions:
                continue
            else:
                count += 1
    return count


print("Part 1:", part_1_and_2(positions, 10))
print("Part 2:", part_1_and_2(positions, 100000))