import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()
puzzle = [x[::-1] for x in input]
max_length = len(max(puzzle, key=lambda x: len(x)))

totals = ['' for x in range(max_length)]

for i in range(max_length):
    for line in puzzle:
        try:
            totals[i] += line[i]
        except IndexError:
            pass

key = {
    # '=': -2,
    # '-': -1,
    # '0': 0,
    # '1': 1,
    # '2': 2,
    '=': -4,
    '-': -2,
    '0': 0,
    '1': 2,
    '2': 4,
}

total = [0 for x in range(len(totals))]
for i, digits in enumerate(totals):
    for digit in digits:
        total[i] += key[digit]

def to_base_5(n):
    s = ""
    while n:
        s = str(n % 5) + s
        n //= 5
    return s

# from copy import copy
# _total = copy(total)
# for i, n in enumerate(_total):
#     while total[i] < 0:
#         total[i] += 5
#         total[i + 1] -= 1

new_total = 0
for i, n in enumerate(total):
    adding = 5**i * n
    new_total += adding

decimal = new_total // 2
base_5 = to_base_5(decimal)

reverse_base_5 = base_5[::-1]

'00233301104441314121' # reverse_base_5
'002=--1110-002=2-221' # reverse_base_5 to snafu (by hand)
print('002=--1110-002=2-221'[::-1])
