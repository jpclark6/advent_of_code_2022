import os
import json
from functools import cmp_to_key


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()
input = [json.loads(row) for row in rows if row != '']


def compare_ints(left, right):
    if left < right:
        return 1
    elif left == right:
        return 0
    else:
        return -1


def compare_lists(left, right):
    left_qty = len(left)
    right_qty = len(right)

    # check if we have anything to compare
    if left_qty == right_qty == 0:
        return 0
    elif left_qty == 0:
        return 1

    # if we compare, check if one is correct
    for i in range(len(left)):
        if i == right_qty:
            return -1
        ans = compare(left[i], right[i])
        if ans != 0:
            return ans

    # after compare, we still have items in right
    if right_qty > left_qty:
        return 1

    # everything shows they're equal, so continue
    return 0


def to_list(item):
    if type(item) == list:
        return item
    return [item]


def compare(left, right):
    if type(left) == type(right) == int:
        return compare_ints(left, right)
    else:
        return compare_lists(to_list(left), to_list(right))


def compare_runner(left, right):
    correct_order = compare(left, right)
    if correct_order == -1:  # wrong order
        return -1
    return 1  # correct order


### Part 1 ###
part_1 = 0
for i in range(0, len(input), 2):
    left = input[i]
    right = input[i + 1]
    correct_order = compare_runner(left, right)
    if correct_order == 1:
        part_1 += i // 2 + 1

print("Part 1:", part_1)


### Part 2 ###
part_2 = 0
input = list(filter(lambda x: x != '', input))

ADDITIONAL = [[[2]], [[6]]]
for to_add in ADDITIONAL:
    input.append(to_add)

input.sort(key=cmp_to_key(compare_runner), reverse=True)

part_2 = 1
for added in ADDITIONAL:
    part_2 *= (input.index(added) + 1)

print("Part 2:", part_2)
