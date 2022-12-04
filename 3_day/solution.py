from string import ascii_letters
import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rucksacks = f.read().splitlines()


def find_points(letter):
    return ascii_letters.index(letter) + 1


total = 0
for sack in rucksacks:
    middle = len(sack) // 2
    first = sack[:middle]
    second = sack[middle:]
    letter = (set(first) & set(second)).pop()
    points = find_points(letter)
    total += points


print("Part 1:", total)


total = 0
for i in range(0, len(rucksacks), 3):
    f, s, t = rucksacks[i], rucksacks[i + 1], rucksacks[i + 2]
    letter = (set(f) & set(s) & set(t)).pop()
    points = find_points(letter)
    total += points


print("Part 2:", total)
