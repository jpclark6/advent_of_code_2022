import os
from collections import namedtuple


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()

TOPO = [list(x) for x in rows]
Dir = namedtuple('Dir', ['x', 'y'])
DIRS = [Dir(0, 1), Dir(0, -1), Dir(1, 0), Dir(-1, 0)]
Position = namedtuple('Position', ['x', 'y'])


class Path:
    def __init__(self, start="S"):
        self.next_positions = self.find_start_positions(start)
        self.positions = []
        self.steps = 0
        self.visited = set()
        for position in self.next_positions:
            self.visit(position)

    def find_start_positions(self, start):
        positions = []
        for y in range(len(TOPO)):
            for x in range(len(TOPO[y])):
                if TOPO[y][x] == start:
                    positions.append(Position(x, y))
        return positions

    def is_end(self, position):
        return TOPO[position.y][position.x] == "E"

    def visit(self, position):
        self.visited.add((position.x, position.y))

    def find_end(self):
        while True:
            self.take_step()
            for position in self.positions:
                for next_position in self.find_next_positions(position):
                    if self.is_end(next_position):
                        return self.steps
                    else:
                        self.next_positions.append(next_position)

    def take_step(self):
        self.positions = self.next_positions
        self.next_positions = []
        self.steps += 1

    def in_topo(self, position):
        return (
            position.x >= 0
            and position.y >= 0
            and position.x < len(TOPO[0])
            and position.y < len(TOPO)
        )

    def possible_position(self, p1, p2):
        # if we've visited it already then ignore it
        if (p2.x, p2.y) in self.visited:
            return False

        # must be within 1 if going up, unlimited if going down unless it's
        # the end, in which case we must be on 'z'
        in_topo = self.in_topo(p2)
        if not in_topo:
            return False

        elevation_valid = (
            ord(TOPO[p2.y][p2.x]) - ord(TOPO[p1.y][p1.x]) <= 1
            or TOPO[p1.y][p1.x] == 'S' and TOPO[p2.y][p2.x] == 'a'
        )
        is_ending = TOPO[p2.y][p2.x] == "E"
        ready_for_ending = TOPO[p1.y][p1.x] == "z"
        return (
            elevation_valid and not is_ending
            or is_ending and ready_for_ending
        )

    def find_next_positions(self, position):
        next_positions222 = []
        for dir in DIRS:
            next_position = Position(
                position.x + dir.x,
                position.y + dir.y,
            )
            if self.possible_position(position, next_position):
                next_positions222.append(next_position)
                self.visit(next_position)
        return next_positions222


path_1 = Path(start='S')
print("Part 1:", path_1.find_end())

path_2 = Path(start='a')
print("Part 2:", path_2.find_end())
