import os
from collections import OrderedDict


filename = "example.txt"  # 10605
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    data = f.read()
raw_monkeys = data.split('\n\n')


'''
Starting items = worry level
Run through operation
Divide by 3 by rounding down
Run test and pass to new monkey
'''

class Monkey:
    def __init__(self, info):
        self.name = info.split('Monkey ')[1].split(':\n')[0]
        self.items = [int(x) for x in info.split('items: ')[1].split('\n')[0].split(', ')]
        self.operation = info.split('new = ')[1].split('\n')[0]
        self.divisible_by = int(info.split('divisible by ')[1].split('\n')[0])
        self.throw_to = {
            True: info.split('monkey ')[1].split('\n')[0],
            False: info.split('monkey ')[2].split('\n')[0],
        }
        self.inspections = 0

    def run_op(self, old):
        return eval(self.operation)

    def check_divisible(self, item):
        return item % self.divisible_by == 0

    def next_monkey(self, item):
        return self.throw_to[self.check_divisible(item)]

    def get_item(self):
        self.inspections += 1
        return self.items.pop(0)


monkeys = OrderedDict()
for raw_monkey in raw_monkeys:
    monkey = Monkey(raw_monkey)
    monkeys[monkey.name] = monkey


def print_worry_items(monkeys):
    for monkey in monkeys.values():
        print(monkey.name, monkey.items)


def run_round_part_1(monkeys):
    for monkey in monkeys.values():
        while monkey.items:
            item = monkey.get_item()
            new_num = monkey.run_op(item) // 3
            next_monkey = monkey.next_monkey(new_num)
            monkeys[next_monkey].items.append(new_num)



ROUNDS = 20
for round in range(ROUNDS):
    run_round_part_1(monkeys)

inspections = []
for monkey in monkeys.values():
    inspections.append(monkey.inspections)
inspections = sorted(inspections, reverse=True)

part_1 = inspections[0] * inspections[1]
print("Part 1:", part_1)


##### Part 2 #####

monkeys = OrderedDict()
for raw_monkey in raw_monkeys:
    monkey = Monkey(raw_monkey)
    monkeys[monkey.name] = monkey


# magic sauce - find common factor to divide by it later
# to keep numbers halfway small
divider = 1
for monkey in monkeys.values():
    divider *= monkey.divisible_by


def run_round_part_2(monkeys):
    for monkey in monkeys.values():
        while monkey.items:
            item = monkey.get_item()
            new_num = monkey.run_op(item)
            remainder = new_num % divider
            next_monkey = monkey.next_monkey(remainder)
            monkeys[next_monkey].items.append(remainder)


ROUNDS = 10000
for round in range(ROUNDS):
    run_round_part_2(monkeys)

inspections = []
for monkey in monkeys.values():
    inspections.append(monkey.inspections)
inspections = sorted(inspections, reverse=True)

part_2 = inspections[0] * inspections[1]
print("Part 2:", part_2)
