import os
from copy import copy


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()


def transform_to_unit_instructions(rows):
    moves = {
        'R': (1, 0),
        'U': (0, -1),
        'L': (-1, 0),
        'D': (0, 1),
    }
    instructions = []
    for r in rows:
        dir = r.split(' ')[0]
        for _ in range(int(r.split(' ')[1])):
            instructions.append(moves[dir])
    return instructions


instructions = transform_to_unit_instructions(rows)


def print_state(ropes):
    # for debugging
    qty = 40
    array = []
    for _ in range(qty):
        row = copy(list('*' * qty))
        array.append(row)
    zero_loc = qty // 2
    for rope in ropes:
        array[rope.y + zero_loc][rope.x + zero_loc] = rope.name
    for line in array:
        print(''.join(line))


class Rope:
    def __init__(self, name='0', x=0, y=0):
        self.name = str(name)
        self.x = x
        self.y = y
        self.visited = {(self.x, self.y)}

    def set_coords(self, x, y):
        self.visited.add((x, y))
        self.x = x
        self.y = y

    def take_instruction(self, inst):
        x = self.x + inst[0]
        y = self.y + inst[1]
        self.set_coords(x, y)

    def find_diff(self, other_rope):
        return {
            'x': other_rope.x - self.x,
            'y': other_rope.y - self.y
        }

    def move_towards(self, other_rope):
        diff = self.find_diff(other_rope)
        delta_x = 0
        delta_y = 0
        if diff['x'] * diff['y'] == 0:  # vert or horizontal difference
            # if 2 spaces away, move 1, else move 0
            if abs(diff['x']) == 2 or abs(diff['y']) == 2:
                delta_x = diff['x'] // 2
                delta_y = diff['y'] // 2
        else:  # diagonally separated
            # go diagonally towards other rope if it's not touching other rope
            if not (abs(diff['x']) == abs(diff['y']) == 1):
                delta_x = abs(diff['x']) // diff['x']
                delta_y = abs(diff['y']) // diff['y']
        self.set_coords(
            self.x + delta_x,
            self.y + delta_y
        )


# Part 1
h = Rope()
t = Rope()

for i in instructions:
    h.take_instruction(i)
    t.move_towards(h)

print("Part 1:", len(t.visited))


# Part 2
sections = 10
ropes = []
for name in range(sections):
    ropes.append(Rope(name))

for i in instructions:
    ropes[0].take_instruction(i)
    for x in range(1, len(ropes)):
        ropes[x].move_towards(ropes[x - 1])

print("Part 2:", len(ropes[-1].visited))
