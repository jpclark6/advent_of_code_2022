import os
from itertools import cycle
from pprint import pprint as pp

filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    wind = f.read()

# ####
rock_1 = [(0, 0), (1, 0), (2, 0), (3, 0)]

# .#.
# ###
# .#.
rock_2 = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]


# ..#
# ..#
# ###
rock_3 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

# #
# #
# #
# #
rock_4 = [(0, 0), (0, 1), (0, 2), (0, 3)]

# ##
# ##
rock_5 = [(0, 0), (1, 0), (0, 1), (1, 1)]

rocks = [rock_1, rock_2, rock_3, rock_4, rock_5]


class Chamber:
    WIDTH = 7
    Y_OFFSET = 3 + 1
    X_OFFSET = 2

    def __init__(self, rocks, wind):
        self.rocks = cycle(rocks)
        self.wind = cycle(list(wind))
        self.chamber = []
        for w in range(self.WIDTH):
            self.chamber.append((w, 0))
        self.cycles = 0

    def has_overlap(self, rock):
        for spot in rock:
            if spot in self.chamber:
                return True
        return False

    def push_wind(self, rock):
        dir = next(self.wind)
        push = 1 if dir == '>' else -1
        new_rock = []
        for spot in rock:
            new_rock.append((spot[0] + push, spot[1]))
        if any([x < 0 for x, y in new_rock]):
            return rock
        elif any([x >= self.WIDTH for x, y in new_rock]):
            return rock
        elif self.has_overlap(new_rock):
            return rock
        else:
            return new_rock

    def check_finished(self, rock):
        for spot in rock:
            if (spot[0], spot[1] - 1) in self.chamber:
                return True
        return False

    def fall_unit(self, rock):
        new_rock = []
        for spot in rock:
            new_rock.append((spot[0], spot[1] - 1))
        return new_rock

    def drop_rock(self, rock):
        rock = self.push_wind(rock)
        rock_finished = self.check_finished(rock)
        if rock_finished:
            return True, rock
        rock = self.fall_unit(rock)
        return False, rock

    def run_rock_drop(self):
        rock = self.find_starting_loc()
        finished = False
        while not finished:
            finished, rock = self.drop_rock(rock)
        self.add_to_chamber(rock)

    def add_to_chamber(self, rock):
        for spot in rock:
            self.chamber.append(spot)

    def find_starting_loc(self):
        # Each rock appears so that its left edge is two
        # units away from the left wall and its bottom edge
        # is three units above the highest rock in the room
        # (or the floor, if there isn't one).
        top_rock = max(self.chamber, key=lambda x: x[1], default=0)
        starting_y = top_rock[1] + self.Y_OFFSET
        starting_x = self.X_OFFSET
        rock_coords = next(self.rocks)
        rock = []
        for val in rock_coords:
            rock.append((
                val[0] + starting_x,
                val[1] + starting_y,
            ))
        return rock


chamber = Chamber(rocks, wind)

def print_chamber(chamber):
    printer = []
    for y in range(30):
        row = '|'
        if y == 0:
            row += 7*'-'
        else:
            for x in range(7):
                next_char = ''
                for rock in chamber:
                    if rock[0] == x and rock[1] == y:
                        next_char = '#'
                        break
                if not next_char:
                    next_char = '.'
                row += next_char
        row += '|'
        printer.insert(0, ''.join(row))
    for row in printer:
        print(row)


# for i in range(2022):
#     chamber.run_rock_drop()
#     # print_chamber(chamber.chamber)

# print("Part 1:", max(chamber.chamber, key=lambda x: x[1])[1])

GUESS = 11000

heights = []
for i in range(GUESS):
    if i % 100 == 0:
        print("1st part:", i, "/", GUESS)
    chamber.run_rock_drop()
    # print_chamber(chamber.chamber)
    heights.append(max(chamber.chamber, key=lambda x: x[1])[1])

# heights = max height after each rock is dropped

diffs = []

hashes = []
start_round = 100
min_thing = None
max_thing = 0
for i in range(start_round, GUESS):
    if i % 100 == 0:
        print("2nd part:", i, "/", GUESS)
    to_hash_pre = heights[i - start_round:i]
    to_hash = tuple([x - to_hash_pre[0] for x in to_hash_pre])
    if to_hash in hashes:
        if min_thing is None:
            min_thing = hashes.index(to_hash)
            max_thing = min_thing
        else:
            if hashes.index(to_hash) >= max_thing:
                max_thing = hashes.index(to_hash)
                starter = i
            else:
                break
    hashes.append(to_hash)


def equalizeit(a):
    print([x - a[0] for x in a])

rocks = max_thing - min_thing + 1
offset = min_thing

rock = 1000000000000 - 1

if rock < offset + 5:
    height = heights[rock]
else:
    if rock < offset + rocks:
        height = 0
        height += heights[offset]
        height += heights[rock] - heights[offset]
    else:
        multi = heights[starter + rocks] - heights[starter]
        height = 0
        height += heights[offset]
        height += multi * ((rock - offset) // rocks)
        remainder = (rock - offset) % rocks
        height += heights[offset + remainder] - heights[offset]
        # if heights[rock] != height:
        #     import pdb; pdb.set_trace()
    # more = (rock - offset) // rocks % rocks
    # height += heights[offset + more]
    # height += (rock - offset) // rocks * rocks
print("Part 2:", height)

# 1514285714288
# 1514285714288

