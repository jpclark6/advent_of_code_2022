import os


filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    pinput = f.read().splitlines()

monkeys = [x.split(': ') for x in pinput]

answers = {}
arith_monkeys = []
for monkey in monkeys:
    try:
        globals()[monkey[0]] = int(monkey[1])
    except ValueError:
        arith_monkeys.append(monkey)

i = 0
while 'root' not in globals():
    i += 1
    print(i)
    for monkey in arith_monkeys:
        try:
            ans = eval(monkey[1])
            globals()[monkey[0]] = ans
        except NameError:
            continue

print("Part 1:", globals()['root'])


## Part 2 ##

'''
Super hacky. Went with a pseudo binary search type method but
instead of programmatically doing it I just hacked it and did
it by hand. Start with some random guess and then below under
'if globals()['root']:' first do something like *= 2 until you
see which direction things are moving. Play around until you start
crossing over the '0' between the needed number and your number,
then make it a += operation starting around 10000, then right before
it crosses over change the 'guess' to the new guess and change
the addition to += 1000, then 100, then 10, then 1. Took < 5 min
to find the answer so I think I came out ahead. Hacky day. Still got the answer.
'''

monkeys = [x.split(': ') for x in pinput]
for monkey in monkeys:
    if monkey[0] == 'root':
        things = monkey[1].split(' + ')
        changable = things[0]
        static = things[1]
        monkey[1] = 'globals()[changable] > globals()[static]'
    if monkey[0] == 'humn':
        monkey[1] = 100

guess = 3378273370673
last_diff = 0
while True:
    for monkey in monkeys:
        try:
            del globals()[monkey[0]]
        except KeyError:
            pass
        if monkey[0] == 'humn':
            num = guess
            monkey[1] = int(num)
    arith_monkeys = []
    for monkey in monkeys:
        try:
            globals()[monkey[0]] = int(monkey[1])
        except ValueError:
            arith_monkeys.append(monkey)
    while 'root' not in globals():
        for monkey in arith_monkeys:
            try:
                # if monkey[0] == 'root':
                #     import pdb; pdb.set_trace()
                ans = eval(monkey[1])
                globals()[monkey[0]] = ans
            except (NameError, KeyError):
                continue
    print('Root', globals()['root'], 'guess', guess)
    print(globals()[changable], globals()[static], globals()[changable] - globals()[static], last_diff - (globals()[changable] - globals()[static]))
    if globals()[changable] == globals()[static]:
        print("Part 2:", guess)
        break
    if globals()['root']:
        guess = int(guess + 1)
    else:
        guess = guess // 1.05
    last_diff = globals()[changable] - globals()[static]