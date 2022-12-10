import os
from copy import copy


filename = "example_1.txt"  # -1
filename = "example_2.txt"  # 13140
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    instructions = f.read().splitlines()


class Circuit:
    def __init__(self, x=1):
        self.x = x
        self.cycle_count = 1
        self.values = {self.cycle_count: self.x}

    def cycle(self, instruction):
        if instruction == 'noop':
            self.increment_cycle_count(1)
        elif 'addx' in instruction:
            self.increment_cycle_count(2)
            value = int(instruction.split(' ')[1])
            self.x += value

    def increment_cycle_count(self, amount):
        for _ in range(amount):
            self.cycle_count += 1
            self.values[self.cycle_count] = self.x

    def value_during(self, cycle):
        return self.values[cycle + 1]


circuit = Circuit()

for i in instructions:
    circuit.cycle(i)
circuit.increment_cycle_count(1)


CYCLES = [20, 60, 100, 140, 180, 220]
part_1 = 0
for cycle in CYCLES:
    part_1 += cycle * circuit.value_during(cycle)

print("Part 1:", part_1)


# Part 2
pixels = []
for x in range(1, 241):
    val = circuit.value_during(x)
    sprite = [val - 1, val, val + 1]

    if (x - 1) % 40 in sprite:
        pixels.append('{#')
    else:
        pixels.append('  ')

print('\nPart 2:\n')
for x in range(0, 240, 40):
    print(''.join(pixels[x:x+40]))
