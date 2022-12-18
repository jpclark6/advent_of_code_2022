import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    _cubes = f.read().splitlines()


class Cube:
    def __init__(self, xyz):
        self.x = int(xyz.split(',')[0])
        self.y = int(xyz.split(',')[1])
        self.z = int(xyz.split(',')[2])
        self.sides = 6

    @property
    def max_coord(self):
        return max([self.x, self.y, self.z])

    @property
    def min_coord(self):
        return min([self.x, self.y, self.z])

    def reset(self):
        self.sides = 6

    def __repr__(self) -> str:
        return f'<{self.x},{self.y},{self.z}>'


# Find the boundaries of a large cube that
# contains all small cubes
min_coord = 0
max_coord = 0
cubes = {}
for _cube in _cubes:
    cube = Cube(_cube)
    if cube.min_coord < min_coord:
        min_coord = cube.min_coord
    if cube.max_coord > max_coord:
        max_coord = cube.max_coord
    cubes[(cube.x, cube.y, cube.z)] = cube
min_coord -= 2
max_coord += 2


for cube in cubes.values():
    side_x = (cube.x - 1, cube.y, cube.z)
    side_y = (cube.x, cube.y - 1, cube.z)
    side_z = (cube.x, cube.y, cube.z - 1)
    for side in [side_x, side_y, side_z]:
        if side in cubes:
            # if another cube is present on side of cube,
            # one side on each cube is touching another cube
            # so both cubes lose one side
            cube.sides -= 1
            cubes[side].sides -= 1

all_sides = [c.sides for c in cubes.values()]
total = sum(all_sides)
print("Part 1:", total)


## Part 2 ##
[cube.reset() for coord, cube in cubes.items()]  # make 6 sides again

class Dir:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

dirs = [
    Dir(1, 0, 0), Dir(-1, 0, 0),  # x directions
    Dir(0, 1, 0), Dir(0, -1, 0),  # y directions
    Dir(0, 0, 1), Dir(0, 0, -1),  # z directions
]

visited = set()
enclosed = set()
not_enclosed = set()

for coord in cubes.keys():
    visited.add(coord)

def is_enclosed(coord):
    if coord in enclosed:
        return True
    if coord in not_enclosed:
        return False

    this_grouping = [coord]
    to_check = [coord]

    while to_check:
        coord = to_check.pop()
        for dir in dirs:
            space = (
                coord[0] + dir.x,
                coord[1] + dir.y,
                coord[2] + dir.z,
            )
            if space in visited:
                if space in enclosed:
                    for group in this_grouping:
                        enclosed.add(group)
                    return True
                if space in not_enclosed:
                    for group in this_grouping:
                        not_enclosed.add(group)
                    return False
                continue
            this_grouping.append(space)
            visited.add(space)

            if any([
                space[0] > max_coord, space[0] < min_coord,
                space[1] > max_coord, space[1] < min_coord,
                space[2] > max_coord, space[2] < min_coord,
            ]):
                for group in this_grouping:
                    not_enclosed.add(group)
                return False

            to_check.append(space)

    for group in this_grouping:
        enclosed.add(group)
    return True


for coord, cube in cubes.items():
    for dir in dirs:
        space = (
            cube.x + dir.x,
            cube.y + dir.y,
            cube.z + dir.z,
        )
        if space in cubes:
            cube.sides -= 1
        else:
            if is_enclosed(space):
                cube.sides -= 1

all_sides = [c.sides for c in cubes.values()]
total = sum(all_sides)

print("Part 2:", total)
