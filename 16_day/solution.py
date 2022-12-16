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


nodes = Nodes()

p = re.compile('Valve (.*) has flow rate=(.*); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)')
for line in input:
    id, flow_rate, connections = p.findall(line)[0]
    node = Node(id, flow_rate, connections)
    nodes.add_node(node)
nodes.update_node_connections()


class Path:
    def __init__(self, path=None, minutes=30):
        self.path = path or [] # {'node': node, 'action': action}
        self.minutes = minutes

    @property
    def total(self):
        total = 0
        minutes = self.minutes
        for node in self.path:
            if node['action'] == 'open':
                total += minutes * node['node'].flow_rate
                minutes -= 2
            else:
                minutes -= 1
        return total


## Part 1
START = 'AA'
node = nodes.get(START)
final_path = Path()

while True:
    for conn1 in node.connections:
        for conn2 in conn1.connections:
            
