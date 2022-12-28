from collections import defaultdict
from itertools import product
from functools import cache
import os
import re

filename = "example.txt"
filename = "input.txt"
directory, _ = os.path.split(__file__)
filepath = directory + "/" + filename

with open(filepath, "r") as f:
    input = f.read().splitlines()


class Nodes:
    def __init__(self):
        self._nodes = {}
        self.paths = []

    def add_node(self, node):
        self._nodes[node.id] = node

    def update_node_connections(self):
        for node in self._nodes.values():
            ids = node.connections
            node.connections = []
            for id in ids:
                node.connections.append(self._nodes[id])

    @property
    def nodes(self):
        return [*self._nodes.values()]

    def get(self, id):
        return self.nodes[id]


class Node:
    def __init__(self, id, flow_rate, connections):
        self.id = id
        self.flow_rate = int(flow_rate)
        self.connections = connections.split(", ")

    def __repr__(self) -> str:
        return f'< {self.id} - {self.flow_rate} - {",".join([x.id for x in self.connections])}'


non_zero_flows = dict()
nodes = set()
distances = defaultdict(lambda: 99999)

p = re.compile(
    "Valve (.*) has flow rate=(.*); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)"
)
for line in input:
    id, flow_rate, connections = p.findall(line)[0]
    if flow_rate != "0":
        non_zero_flows[id] = int(flow_rate)
    nodes.add(id)
    for conn in connections.split(", "):
        distances[id, conn] = 1
non_zero_nodes = set(non_zero_flows)

for k, i, j in product(nodes, repeat=3):  # floyd-warshall
    distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])


@cache
def search(time, non_zero_nodes, location="AA", split_for_elephant=False):
    totals = []
    for node in non_zero_nodes:
        distance = distances[location, node]
        if time < distance:
            continue
        total = (time - distance - 1) * non_zero_flows[node]
        next_locations = non_zero_nodes - {node}
        total += search(
            (time - distance - 1),
            frozenset(next_locations),
            location=node,
            split_for_elephant=split_for_elephant,
        )
        totals.append(total)
    if split_for_elephant:
        totals.append(search(26, non_zero_nodes))
    return max(totals, default=0)


print("Part 1:", search(30, frozenset(non_zero_nodes), "AA"))
print("Part 2:", search(26, frozenset(non_zero_nodes), "AA", split_for_elephant=True))
