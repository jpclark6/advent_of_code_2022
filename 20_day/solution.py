import os
from copy import copy
from functools import cache

filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    _input = f.read().splitlines()


def cycle_list(num_cycles, multiplyer=1):
    original = [int(x) * multiplyer for x in _input]
    to_cycle = []
    for i, num in enumerate(original):
        to_cycle.append({'num': num, 'id': i})

    def move_nums(to_cycle, index):
        num = to_cycle.pop(index)
        new_index = index + num['num']
        new_index = new_index % len(to_cycle)
        to_cycle.insert(new_index, num)
        return to_cycle

    for _ in range(num_cycles):
        for i in range(len(original)):
            for j, nums in enumerate(to_cycle):
                if nums['id'] == i:
                    index = j
                    break
            move_nums(to_cycle, index)

    for i, num in enumerate(to_cycle):
        if num['num'] == 0:
            zero = i
            break

    grove = [1000, 2000, 3000]
    ans = 0
    for g in grove:
        index = (zero + g) % len(to_cycle)
        ans += to_cycle[index]['num']

    return ans


part_1 = cycle_list(1)
print("Part 1:", part_1)

part_2 = cycle_list(10, 811_589_153)
print("Part 2:", part_2)
