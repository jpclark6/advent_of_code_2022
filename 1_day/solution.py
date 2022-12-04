# Day 1


def find_calories(filepath):
    with open(filepath, "r") as f:
        input = f.read()

    elves = [[int(y) for y in x.split("\n")] for x in input.split("\n\n")]
    elves_totals = []
    for calories in elves:
        elves_totals.append(sum(calories))

    return sorted(elves_totals, reverse=True)


def run_puzzle():
    for input in ["example.txt", "input.txt"]:
        solved = find_calories(input)
        print("*" * 5, input, "*" * 5)
        print(f"Part 1 {input}:", solved[0])
        print(f"Part 2 {input}:", sum(solved[:3]))
        print()


run_puzzle()
