import os


                              # part 1; part 2
# filename = "example_1.txt"  # 5; 23
# filename = "example_2.txt"  # 6; 23
# filename = "example_3.txt"  # 10; 29
# filename = "example_4.txt"  # 11; 26
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    puzzle = f.read()


def find_marker(part, unique):
    for i in range(len(puzzle)):
        x = set(puzzle[i:i + unique])
        if len(x) == unique:
            print(f"Part {part}:", i + unique)
            break


find_marker(1, 4)
find_marker(2, 14)