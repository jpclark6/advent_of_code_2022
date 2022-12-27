import os
import re
from itertools import combinations, chain
from copy import copy
from pprint import pprint as pp


filename = "example.txt"
filename = "input.txt"  # 1480 3168
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()


class Recipe:
    def __init__(self, **kwargs):
        self.blueprint = kwargs['blueprint']
        self.ore_r_ore = kwargs['ore_r_ore']
        self.clay_r_ore = kwargs['clay_r_ore']
        self.obsidian_r_ore = kwargs['obsidian_r_ore']
        self.obsidian_r_clay = kwargs['obsidian_r_clay']
        self.geode_r_ore = kwargs['geode_r_ore']
        self.geode_r_obsidian = kwargs['geode_r_obsidian']


p = re.compile('\d+')
recipes = []
for line in input:
    numbers = p.findall(line)
    recipes.append(Recipe(
        **dict(
            blueprint = int(numbers[0]),
            ore_r_ore = int(numbers[1]),
            clay_r_ore = int(numbers[2]),
            obsidian_r_ore = int(numbers[3]),
            obsidian_r_clay = int(numbers[4]),
            geode_r_ore = int(numbers[5]),
            geode_r_obsidian = int(numbers[6]),
        )
    ))


def hash_state(state):
    return (
        f'{state["r_ore"]},{state["ore"]}'
        f'{state["r_clay"]},{state["clay"]}'
        f'{state["r_obsidian"]},{state["obsidian"]}'
        f'{state["r_geode"]},{state["geode"]}'
    )


def has_supplies(rs, state, recipe):
    required = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
    for r in rs:
        if r == 'r_ore':
            required['ore'] += recipe.ore_r_ore
        elif r == 'r_clay':
            required['ore'] += recipe.clay_r_ore
        elif r == 'r_obsidian':
            required['ore'] += recipe.obsidian_r_ore
            required['clay'] += recipe.obsidian_r_clay
        elif r == 'r_geode':
            required['ore'] += recipe.geode_r_ore
            required['obsidian'] += recipe.geode_r_obsidian
    if (
        required['ore'] <= state['ore']
        and required['clay'] <= state['clay']
        and required['obsidian'] <= state['obsidian']
    ):
        return True
    return False


def prune_states(states):
    ORE = 1
    CLAY = 10
    OBSIDIAN = 150
    GEODE = 10000
    ORE_R = 1
    CLAY_R = 10
    OBSIDIAN_R = 250
    GEODE_R = 10000

    new_states = sorted(
        states,
        key= lambda x: (
            x['ore'] * ORE
            + x['clay'] * CLAY
            + x['obsidian'] * OBSIDIAN
            + x['geode'] * GEODE
            + x['r_ore'] * ORE_R
            + x['r_clay'] * CLAY_R
            + x['r_obsidian'] * OBSIDIAN_R
            + x['r_geode'] * GEODE_R
        ),
        reverse=True)
    states = new_states[:1000]
    return states


def find_max_geodes(recipe, minutes):
    visited = set()
    states = [{
        'r_ore': 1, 'ore': 0,
        'r_clay': 0, 'clay': 0,
        'r_obsidian': 0, 'obsidian': 0,
        'r_geode': 0, 'geode': 0,
    }]
    while minutes > 0:
        next_states = []
        while states:
            state = states.pop()
            visited.add(hash_state(state))
            for rs in [(), ('r_ore',), ('r_clay',), ('r_obsidian',), ('r_geode',)]:
                if has_supplies(rs, state, recipe):
                    to_build = rs
                else:
                    continue
                _state = copy(state)
                _state['ore'] += _state['r_ore']
                _state['clay'] += _state['r_clay']
                _state['obsidian'] += _state['r_obsidian']
                _state['geode'] += _state['r_geode']
                for r in to_build:
                    _state[r] += 1
                    if r == 'r_ore':
                        _state['ore'] -= recipe.ore_r_ore
                    elif r == 'r_clay':
                        _state['ore'] -= recipe.clay_r_ore
                    elif r == 'r_obsidian':
                        _state['ore'] -= recipe.obsidian_r_ore
                        _state['clay'] -= recipe.obsidian_r_clay
                    elif r == 'r_geode':
                        _state['ore'] -= recipe.geode_r_ore
                        _state['obsidian'] -= recipe.geode_r_obsidian
                if hash_state(_state) not in visited:
                    next_states.append(_state)
        minutes -= 1
        states = next_states
        states = prune_states(states)

    max_geode = max(states, key=lambda x: x['geode'])['geode']
    return max_geode


MINUTES = 24
values = 0
for recipe in recipes:
    max_geodes = find_max_geodes(recipe, MINUTES)
    values += max_geodes * recipe.blueprint
print("Part 1:", values)


MINUTES = 32
values = 1
for recipe in recipes[:3]:
    max_geodes = find_max_geodes(recipe, MINUTES)
    values *= max_geodes
print("Part 2:", values)  # 1465 too low
