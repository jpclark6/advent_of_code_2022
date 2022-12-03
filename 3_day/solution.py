from string import ascii_letters
import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + '/' + filename

with open(filepath, "r") as f:
    rucksacks = f.read().splitlines()


def find_points(letter):
    return {k: v for k, v in zip(ascii_letters, range(1, len(ascii_letters) + 1))}[letter]


total = 0
for sack in rucksacks:
    middle = int(len(sack) / 2)
    first = sack[:middle]
    second = sack[middle:]
    letter = list(set(first) & set(second))[0]
    points = find_points(letter)
    total += points


print("Part 1:", total)


total = 0
iterations = int(len(rucksacks) / 3)
for i in range(iterations):
    f, s, t = rucksacks[i * 3], rucksacks[i * 3 + 1], rucksacks[i * 3 + 2]
    letter = list(set(f) & set(s) & set(t))[0]
    points = find_points(letter)
    total += points


print("Part 2:", total)
