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
        self.connections = connections.split(', ')

    def __repr__(self) -> str:
        return f'< {self.id} - {self.flow_rate} - {",".join([x.id for x in self.connections])}'


non_zero_flows = dict()
nodes = set()
distances = defaultdict(lambda: 99999)

p = re.compile('Valve (.*) has flow rate=(.*); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)')
for line in input:
    id, flow_rate, connections = p.findall(line)[0]
    if flow_rate != '0':
        non_zero_flows[id] = int(flow_rate)
    nodes.add(id)
    for conn in connections.split(', '):
        distances[id, conn] = 1

for k, i, j in product(nodes, repeat=3):  # floyd-warshall
    distances[i,j] = min(distances[i,j], distances[i,k] + distances[k,j])

@cache
def search(time, non_zero_flows_set=frozenset(non_zero_flows), current_node='AA'):
    answers = []
    for id in non_zero_flows_set:
        if distances[current_node, id] > time:
            continue
        ans = (
            non_zero_flows[id] * (time - distances[current_node, id] - 1)
            + search(time-distances[current_node, id] - 1, non_zero_flows_set - {id}, id))
        answers.append(ans)
    return max(answers, default=0)

print(search(30))

@cache
def search_p2(time, non_zero_flows_set=frozenset(non_zero_flows), current_node='AA', top_level=False):
    answers = []
    for id in non_zero_flows_set:
        if distances[current_node, id] > time:
            continue
        ans = (
            non_zero_flows[id] * (time - distances[current_node, id] - 1)
            + search_p2(time-distances[current_node, id] - 1, non_zero_flows_set - {id}, id, top_level=True))
        answers.append(ans)
    if top_level:
        answers.append(search(26, non_zero_flows_set=non_zero_flows_set))
    return max(answers, default=0)

print(search_p2(26, top_level=True))
