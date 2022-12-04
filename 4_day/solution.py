import os
from time import time
from contextlib import contextmanager


start = time()

filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    pairs = f.read().splitlines()


full_overlap = 0
partial_overlap = 0
for pair in pairs:
    elf_1, elf_2 = pair.split(",")
    elf_1_start, elf_1_end = [int(x) for x in elf_1.split("-")]
    elf_2_start, elf_2_end = [int(x) for x in elf_2.split("-")]
    elf_1_seg = set(range(elf_1_start, elf_1_end + 1))
    elf_2_set = set(range(elf_2_start, elf_2_end + 1))

    if len(elf_1_seg - elf_2_set) == 0 or len(elf_2_set - elf_1_seg) == 0:
        full_overlap += 1

    if len(elf_1_seg | elf_2_set) != (len(elf_1_seg) + len(elf_2_set)):
        partial_overlap += 1


print("Part 1:", full_overlap)
print("Part 2:", partial_overlap)
end = time()
print('Total time was', end - start, 'seconds')
