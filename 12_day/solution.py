import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    rows = f.read().splitlines()


TOPO = [list(x) for x in rows]
DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


def find_start(start="S"):
    points = []
    for y in range(len(TOPO)):
        for x in range(len(TOPO[y])):
            if TOPO[y][x] == start:
                points.append((x, y))
    return points


(x, y) = find_start()[0]
TOPO[y][x] = "a"


def find_next_moves(history):
    x = history[-1]["x"]
    y = history[-1]["y"]
    steps = history[-1]["steps"]
    steps += 1
    next_moves = []
    for dir in DIRS:
        next_x = x + dir[0]
        next_y = y + dir[1]
        if (
            next_x >= 0  # must be in the playing grid
            and next_y >= 0
            and next_x < len(TOPO[0])
            and next_y < len(TOPO)
            and (  # next step can be at max 1 above, unlimited below, but not the finish unless we're at "z"
                ord(TOPO[next_y][next_x]) - ord(TOPO[y][x]) <= 1
                and TOPO[next_y][next_x] != "E"
                or (TOPO[y][x] == "z" and TOPO[next_y][next_x] == "E")
            )
        ):
            new_history = history + [{"x": next_x, "y": next_y, "steps": steps}]
            next_moves.append(
                {"x": next_x, "y": next_y, "steps": steps, "history": new_history}
            )
    return next_moves


visited = {(x, y)}


def solve_part_1():
    next_moves = [
        {"x": x, "y": y, "steps": 0, "history": [{"x": x, "y": y, "steps": 0}]}
    ]
    temp_next_moves = []
    while True:
        try:
            next_move = next_moves.pop()
            for possible_move in find_next_moves(next_move["history"]):
                if (possible_move["x"], possible_move["y"]) in visited:
                    # we've already visited this spot in less moves
                    continue
                elif (
                    TOPO[next_move["y"]][next_move["x"]] == "z"
                    and TOPO[possible_move["y"]][possible_move["x"]] == "E"
                ):
                    # found the end
                    return possible_move
                elif TOPO[next_move["y"]][next_move["x"]] != "E":
                    # continue onwards
                    temp_next_moves.append(possible_move)
                    visited.add((possible_move["x"], possible_move["y"]))
        except IndexError:
            next_moves = temp_next_moves
            temp_next_moves = []


ans = solve_part_1()
print("Part 1:", ans["steps"])


### PART 2 ###

visited = set(find_start("a"))


def solve_part_2():
    next_moves = []
    for visit in visited:
        next_moves.append(
            {
                "x": visit[0],
                "y": visit[1],
                "steps": 0,
                "history": [{"x": visit[0], "y": visit[1], "steps": 0}],
            }
        )
    temp_next_moves = []
    while True:
        try:
            next_move = next_moves.pop()
            for possible_move in find_next_moves(next_move["history"]):
                if (possible_move["x"], possible_move["y"]) in visited:
                    # we've already visited this spot in less moves
                    continue
                elif (
                    TOPO[next_move["y"]][next_move["x"]] == "z"
                    and TOPO[possible_move["y"]][possible_move["x"]] == "E"
                ):
                    # found the end
                    return possible_move
                elif TOPO[next_move["y"]][next_move["x"]] != "E":
                    # continue onwards
                    temp_next_moves.append(possible_move)
                    visited.add((possible_move["x"], possible_move["y"]))
        except IndexError:
            next_moves = temp_next_moves
            temp_next_moves = []


ans = solve_part_2()
print("Part 2:", ans["steps"])
