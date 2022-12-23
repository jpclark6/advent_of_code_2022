import os
import re
from collections import defaultdict
from copy import deepcopy


filename = "input.txt"
filename = "example.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()


class Recipe:
    def __init__(self, **kwargs):
        self.blueprint = kwargs['blueprint']
        self.ore_robot_ore = kwargs['ore_robot_ore']
        self.clay_robot_ore = kwargs['clay_robot_ore']
        self.obsidian_robot_ore = kwargs['obsidian_robot_ore']
        self.obsidian_robot_clay = kwargs['obsidian_robot_clay']
        self.geode_robot_ore = kwargs['geode_robot_ore']
        self.geode_robot_obsidian = kwargs['geode_robot_obsidian']


p = re.compile('\d+')
recipes = []
for line in input:
    numbers = p.findall(line)
    recipes.append(Recipe(
        **dict(
            blueprint = int(numbers[0]),
            ore_robot_ore = int(numbers[1]),
            clay_robot_ore = int(numbers[2]),
            obsidian_robot_ore = int(numbers[3]),
            obsidian_robot_clay = int(numbers[4]),
            geode_robot_ore = int(numbers[5]),
            geode_robot_obsidian = int(numbers[6]),
        )
    ))



def find_max_geodes(robots, inventory, minutes, new_robots, recipe):
    states = [{
        'robots': robots,
        'inventory': inventory,
        'minutes': minutes,
        'new_robots': new_robots,
    }]
    totals = []
    seenbefore = set()
    while states:
        state = states.pop()
        if str(state) in seenbefore:
            continue
        else:
            seenbefore.add(str(state))


        # Add new robots and subtract inventory
        while state['new_robots']:
            robot = state['new_robots'].pop()
            state['robots'][robot] += qty
            if robot == 'ore':
                state['inventory']['ore'] -= recipe.ore_robot_ore
                state['robots']['ore'] += 1
            elif robot == 'clay':
                state['inventory']['ore'] -= recipe.clay_robot_ore
                state['robots']['clay'] += 1
            elif robot == 'obsidian':
                state['inventory']['ore'] -= recipe.obsidian_robot_ore
                state['inventory']['clay'] -= recipe.obsidian_robot_clay
                state['robots']['obsidian'] += 1
            elif robot == 'geode':
                state['inventory']['ore'] -= recipe.geode_robot_ore
                state['inventory']['obsidian'] -= recipe.geode_robot_obsidian
                state['robots']['geode'] += 1


        if state['inventory']['ore'] >= recipe.ore_robot_ore:
            new_state = deepcopy(state)
            new_state['new_robots'].append('ore')
            new_state['inventory']['ore'] -= recipe.ore_robot_ore
            states.append(new_state)
        if state['inventory']['ore'] >= recipe.clay_robot_ore:
            new_state = deepcopy(state)
            new_state['new_robots'].append('clay')
            new_state['inventory']['ore'] -= recipe.clay_robot_ore
            states.append(new_state)
        if state['inventory']['ore'] >= recipe.ore_robot_ore + recipe.clay_robot_ore:
            new_state = deepcopy(state)
            new_state['new_robots'].append('ore')
            new_state['new_robots'].append('clay')
            new_state['inventory']['ore'] -= recipe.ore_robot_ore + recipe.clay_robot_ore
            states.append(new_state)
        if state['inventory']['ore'] >= recipe.obsidian_robot_ore and state['inventory']['clay'] >= recipe.obsidian_robot_clay:
            new_state = deepcopy(state)
            new_state['new_robots'].append('obsidian')
            new_state['inventory']['ore'] -= recipe.obsidian_robot_ore
            new_state['inventory']['clay'] -= recipe.obsidian_robot_clay
            states.append(new_state)
        if state['inventory']['ore'] >= recipe.geode_robot_ore and state['inventory']['obsidian'] >= recipe.geode_robot_obsidian:
            new_state = deepcopy(state)
            new_state['new_robots'].append('geode')
            new_state['inventory']['ore'] -= recipe.geode_robot_ore
            new_state['inventory']['obsidian'] -= recipe.geode_robot_obsidian
            states.append(new_state)

#   Each ore robot costs 4 ore.
#   Each clay robot costs 2 ore.
#   Each obsidian robot costs 3 ore and 14 clay.
#   Each geode robot costs 2 ore and 7 obsidian.

        # Add new inventory for things mined during minute
        for robot, qty in state['robots'].items():
            state['inventory'][robot] += qty

        # Subtract time
        state['minutes'] -= 1

        # Don't add new state if time is 0
        if state['minutes'] == 0:
            totals.append(state['inventory']['geode'])
        else:
            states.append(state)

        print(len(states), len(totals), state['inventory'])
    return max(totals)


def setup_and_run_max_geodes(recipe, minutes):
    robots = {
        'ore': 1,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
    }
    inventory = {
        'ore': 0,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
    }
    new_robots = []
    return find_max_geodes(robots, inventory, minutes, new_robots, recipe)


MINUTES = 24
values = 0
for recipe in recipes:
    max_geodes = setup_and_run_max_geodes(recipe, MINUTES)
    values += max_geodes * recipe.blueprint
print("Part 1:", values)