import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    instructions = f.read().splitlines()


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f'<{name} {self.size}>'


class Directory:
    def __init__(self, name, parent_dir):
        self.name = name
        self.parent_dir = parent_dir
        self.contents = {}

    @property
    def size(self):
        total = 0
        for item in self.contents.values():
            total += item.size
        return total

    @property
    def pwd(self):
        if self.name == '/':
            return ''
        return self.parent_dir.pwd + '/' + self.name

    def __repr__(self) -> str:
        return f"<{self.name} {self.size}>"


top_directory = Directory('/', None)
current_dir = top_directory
instructions.pop(0) # hack to get rid of cd / for simplicity

while instructions:
    current_line = instructions.pop(0)

    if '$ cd' in current_line:
        next_dir = current_line.split(' ')[2]
        if next_dir == '..':
            current_dir = current_dir.parent_dir
        else:
            try:
                current_dir = current_dir.contents[next_dir]
            except KeyError:
                new_dir = Directory(next_dir, current_dir)
                current_dir.contents[next_dir] = new_dir
                current_dir = new_dir

    elif '$ ls' in current_line:
        if current_dir.contents:
            pass
        else:
            contents = {}
            to_parse = []
            while len(instructions) > 0 and instructions[0][0] != '$':
                to_parse.append(instructions.pop(0))
            for item in to_parse:
                name = item.split(' ')[1]
                if 'dir ' in item:
                    new_item = Directory(name, current_dir)
                else:
                    size = int(item.split(' ')[0])
                    new_item = File(name, size)
                contents[name] = new_item
            current_dir.contents = contents


MAX = 100000

total_small_size = 0
directories_to_search = [top_directory]
directory_sizes = []

while directories_to_search:
    current_dir = directories_to_search.pop()
    for item in current_dir.contents.values():
        if type(item) == Directory:
            size = item.size
            if size <= MAX:
                total_small_size += size
            directories_to_search.append(item)
            directory_sizes.append(size)


print("Part 1:", total_small_size)

TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000

free_space = TOTAL_SPACE - top_directory.size
required_delete = REQUIRED_SPACE - free_space
directory_sizes.sort()
for size in directory_sizes:
    if size > required_delete:
        dir_size_to_delete = size
        break

print("Part 2:", dir_size_to_delete)
