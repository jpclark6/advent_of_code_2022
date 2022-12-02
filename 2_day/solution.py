# Day 2


key = {'X': 0, 'Y': 1, 'Z': 2, 'A': 0, 'B': 1, 'C': 2}
reversed = {0: 'X', 1: 'Y', 2: 'Z'}
win_guide = {'X': 2, 'Y': 0, 'Z': 1}


def find_game_score(them, me):
    if key[them] == key[me]:
        return 3
    if (key[them] + 1) % 3 == key[me]:
        return 6
    else:
        return 0


def find_shape_score(me):
    return key[me] + 1


def find_shape(them, me):
    num = (key[them] + win_guide[me]) % 3
    return reversed[num]


for puzzle in ['example.txt', 'input.txt']:
    with open(puzzle, 'r') as f:
        games = f.read().splitlines()

    total = 0
    total_part_2 = 0
    for game in games:
        them, me = game.split(' ')

        # part 1
        game_score = find_game_score(them, me)
        shape_score = find_shape_score(me)
        total += (game_score + shape_score)

        # part 2
        game_score = {'X': 0, 'Y': 3, 'Z': 6}[me]
        shape = find_shape(them, me)
        shape_score = find_shape_score(shape)
        total_part_2 += (game_score + shape_score)


    print("Part 1", puzzle, total)
    print("Part 2", puzzle, total_part_2)
