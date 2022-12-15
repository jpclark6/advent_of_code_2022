import os
import re
from collections import namedtuple

filename, ROW, LOW, HIGH = "example.txt", 10, 0, 20
filename, ROW, LOW, HIGH = "input.txt", 2000000, 0, 4000000
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()
p = re.compile('[-0-9]+')


Beacon = namedtuple('Beacon', 'x,y')
Sensor = namedtuple('Sensor', 'x,y')
Location = namedtuple('Location', 'x,y')

pairs = []
for line in input:
    x1, y1, x2, y2 = p.findall(line)
    pairs.append([
        Sensor(int(x1), int(y1)),
        Beacon(int(x2), int(y2)),
    ])
# In this example, in the row where y=10, there are 26 positions
# where a beacon cannot be present.

sensor = pairs[0][0]
beacon = pairs[0][1]

def find_distance(sensor, beacon):
    return abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

distance = find_distance(sensor, beacon)

def no_beacons(sensor, beacon, loc):
    distance = find_distance(sensor, loc)
    min_distance = find_distance(sensor, beacon)
    if distance <= min_distance:
        return False
    return True

def min_max_x(sensor, beacon):
    distance = find_distance(sensor, beacon)
    return sensor.x - distance, sensor.x + distance

def no_beacons_row_limits(sensor, beacon, y):
    delta_y = abs(y - sensor.y)
    distance = find_distance(sensor, beacon)
    delta_x = distance - delta_y
    if delta_x >= 0:
        min_x, max_x = sensor.x - delta_x, sensor.x + delta_x
        return min_x, max_x
    else:
        return None, None


min_x = pairs[0][0].x
max_x = pairs[0][0].x

for sensor, beacon in pairs:
    # update min and max y to look at later
    s_min_x, s_max_x = min_max_x(sensor, beacon)
    if s_min_x:
        min_x = s_min_x if s_min_x < min_x else min_x
        max_x = s_max_x if s_max_x > max_x else max_x



def do_magic(row):
    x_ranges = []

    for sensor, beacon in pairs:
        min_x, max_x = no_beacons_row_limits(sensor, beacon, ROW)
        if min_x is not None:
            x_ranges.append((min_x, max_x))

    nums = []
    for range in x_ranges:
        nums.append((range[0], 'r'))
        nums.append((range[1], 'l'))
    nums.sort(key=lambda x: x[0])

    stack = []
    ranges = []
    total = 0
    for i, num in enumerate(nums):
        if num[1] == 'r':
            if not stack:
                last_low = num[0]
                try:
                    if ranges[-1][1] == last_low:
                        last_low += 1
                except IndexError:
                    pass
            stack.append(num)
        if num[1] == 'l':
            if len(stack) == 1:
                last_high = num[0]
                ranges.append((last_low, last_high))
            stack.pop(0)

    def beacon_in_range(beacon, ranges):
        if beacon.y != ROW:
            return False
        for range in ranges:
            if beacon.x >= range[0] and beacon.x <= range[1]:
                return True
        return False

    to_remove = 0
    removed = set()
    for sensor, beacon in pairs:
        if beacon_in_range(beacon, ranges):
            if not beacon in removed:
                to_remove += 1
            removed.add(beacon)

    def get_total(ranges, to_remove):
        total = 0
        for range in ranges:
            total += range[1] - range[0]
            total += 1  # since we're inclusive of ends
        return total - to_remove

    part_1 = get_total(ranges, to_remove)
    return part_1

part_1 = do_magic(ROW)
print("Part 1:", part_1)



### Part 2 ###


def do_magic(row):
    x_ranges = []

    for sensor, beacon in pairs:
        min_x, max_x = no_beacons_row_limits(sensor, beacon, row)
        if min_x is not None:
            x_ranges.append((min_x, max_x))
    nums = []
    for range in x_ranges:
        nums.append((range[0], 'r'))
        nums.append((range[1], 'l'))
    nums.sort(key=lambda x: x[0])

    stack = []
    ranges = []
    total = 0
    for i, num in enumerate(nums):
        if num[1] == 'r':
            if not stack:
                last_low = num[0]
                try:
                    if ranges[-1][1] == last_low:
                        last_low += 1
                except IndexError:
                    pass
            stack.append(num)
        if num[1] == 'l':
            if len(stack) == 1:
                last_high = num[0]
                ranges.append((last_low, last_high))
            stack.pop(0)

    if len(ranges) > 1:
        for i, range in enumerate(ranges):
            try:
                if range[1] + 1 == ranges[i + 1][0]:
                    continue
                else:
                    return (range[1] + 1, row)
            except IndexError:
                continue

    return None

for i in range(LOW, HIGH):
    if i % 1000 == 0:
        print(i, '/', HIGH)
    part_2 = do_magic(i)

    if part_2:
        print("Part 2:", part_2, part_2[0] * 4000000 + part_2[1])
        break
