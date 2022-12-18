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
        self.chamber = {}
        for w in range(self.WIDTH):
            self.chamber[(w, 0)] = None
        self.cycles = 0
        self.top = 0

    def has_overlap(self, rock):
        for spot in rock:
            if spot in self.chamber:
                return True
        return False

    def push_wind(self, rock):
        dir = next(self.wind)
        push = 1 if dir == ">" else -1
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
            self.chamber[spot] = None
            if spot[1] > self.top:
                self.top = spot[1]

    def find_starting_loc(self):
        starting_y = self.top + self.Y_OFFSET
        starting_x = self.X_OFFSET
        rock_coords = next(self.rocks)
        rock = []
        for val in rock_coords:
            rock.append(
                (
                    val[0] + starting_x,
                    val[1] + starting_y,
                )
            )
        return rock


chamber = Chamber(rocks, wind)


def print_chamber(chamber):
    chamber = chamber.keys()
    printer = []
    for y in range(30):
        row = "|"
        if y == 0:
            row += 7 * "-"
        else:
            for x in range(7):
                next_char = ""
                for rock in chamber:
                    if rock[0] == x and rock[1] == y:
                        next_char = "#"
                        break
                if not next_char:
                    next_char = "."
                row += next_char
        row += "|"
        printer.insert(0, "".join(row))
    for row in printer:
        print(row)


## Part 1 ##
for i in range(2022):
    chamber.run_rock_drop()

print("Part 1:", chamber.top)


## Part 2 ##
chamber = Chamber(rocks, wind)
GUESS = 10000


"""
Make an array of heights so we can find if the heights
repeat at some point, which will let us extrapolate
"""
heights = []
for i in range(GUESS):
    chamber.run_rock_drop()
    heights.append(chamber.top)

"""
Find the repeat pattern. Take a slice of heights normalized
to the smallest height, find the hash, and see if you start
to see the same thing over and over. Find an initial offset
and how many rocks are in the sequence
"""
height_pattern_hashes = []
sequence_length = 100
unique_order = None
end_of_sequence = 0
for i in range(sequence_length, GUESS):
    sequence = heights[i - sequence_length : i]
    normalized_sequence = tuple([x - sequence[0] for x in sequence])
    if normalized_sequence in height_pattern_hashes:
        if unique_order is None:
            unique_order = height_pattern_hashes.index(normalized_sequence)
            end_of_sequence = unique_order
        else:
            if height_pattern_hashes.index(normalized_sequence) >= end_of_sequence:
                end_of_sequence = height_pattern_hashes.index(normalized_sequence)
                start_check_here = i
            else:
                break
    height_pattern_hashes.append(normalized_sequence)

rocks_in_cycle = end_of_sequence - unique_order + 1
initial_offset = unique_order

"""
Do math to calculate height. It's really that final 'else'
that is all that is needed to calculate big numbers, but
this lets you calculate any height based on the number of rocks
"""
rock_height = 1000000000000
rock_height -= 1  # To correct for off by 1. Because...?

if rock_height < initial_offset + 5:
    height = heights[rock_height]
else:
    if rock_height < initial_offset + rocks_in_cycle:
        height = 0
        height += heights[initial_offset]
        height += heights[rock_height] - heights[initial_offset]
    else:
        multi = heights[start_check_here + rocks_in_cycle] - heights[start_check_here]
        height = 0
        height += heights[initial_offset]
        height += multi * ((rock_height - initial_offset) // rocks_in_cycle)
        remainder = (rock_height - initial_offset) % rocks_in_cycle
        height += heights[initial_offset + remainder] - heights[initial_offset]

print("Part 2:", height)
