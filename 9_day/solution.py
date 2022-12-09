import os


filename = "input.txt"
filename = "example.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()

def transform_to_instructions(rows):
    moves = {
        'R': (1, 0),
        'U': (0, -1),
        'L': (-1, 0),
        'D': (0, 1),
    }
    instructions = []
    for r in rows:
        dir = r.split(' ')[0]
        for x in range(int(r.split(' ')[1])):
            instructions.append(moves[dir])
    return instructions

instructions = transform_to_instructions(rows)


class Rope:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.visited = {(self.x, self.y)}
        self.visited2 = [(self.x, self.y)]

    def set_coords(self, x, y):
        self.visited.add((x, y))
        self.visited2.append((x, y))
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
        if diff['x'] * diff['y'] == 0:
            # go 0 or 1 in direction towards other rope
            if (abs(diff['x']) == 2 or abs(diff['y']) == 2):
                self.set_coords(
                    self.x + diff['x'] // 2,
                    self.y + diff['y'] // 2
                )
            else:
                # they are touching
                pass
        else:
            # go diagonally towards other rope
            # if not touching
            if abs(diff['x']) == abs(diff['y']) == 1:
                # do nothing since they're touching
                x = 0
                y = 0
            elif abs(diff['x']) == 2:
                x = diff['x'] // 2
                y = diff['y']
            else:
                y = diff['y'] // 2
                x = diff['x']
            self.set_coords(
                self.x + x,
                self.y + y
            )

h = Rope()
t = Rope()

for i in instructions:
    h.take_instruction(i)
    t.move_towards(h)

print("Part 1:", len(t.visited))


sections = 10
ropes = []
for _ in range(sections):
    ropes.append(Rope())

for i in instructions:
    ropes[0].take_instruction(i)
    for x in range(1, len(ropes)):
        import pdb; pdb.set_trace()
        ropes[x].move_towards(ropes[x - 1])

print("Part 2:", len(ropes[-1].visited))
from pprint import pprint as pp
pp(ropes[-1].visited2)
