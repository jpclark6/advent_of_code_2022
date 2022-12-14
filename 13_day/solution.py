import os
import json


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()
input = [json.loads(row) for row in rows if row != '']

'''
When comparing two values, the first value is called left and the second value is called right. Then:

If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
'''

def is_correct(left, right):
    # import pdb; pdb.set_trace()
    for i in range(len(left)):
        wizard = ''
        try:
            if type(left[i]) == list and type(right[i]) == int:
                return is_correct(left[i], [right[i]])
            elif type(right[i]) == list and type(left[i]) == int:
                return is_correct([left[i]], right[i])
            elif type(right[i]) == list and type(left[i]) == list:
                return is_correct(left[i], right[i])
            else:
                if left[i] < right[i]:
                    return True
                elif left[i] == right[i]:
                    continue
                else:
                    return False
        except IndexError:
            # right side ran out of values
            return False
    return True  # left side ran out of values

part_1 = 0
for i in range(0, len(input), 2):
    left = input[i]
    right = input[i + 1]
    correct_order = is_correct(left, right)
    if correct_order:
        part_1 += i // 2 + 1

print("Part 1:", part_1)
