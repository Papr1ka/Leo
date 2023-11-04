import weakref
from typing import Any, List


class Tree:
    nodes: List
    data: Any

    def __init__(self, data, parent=None):
        self.nodes = []
        self.data = data
        self.parent = parent

    def add_node(self, data):
        tree = Tree(data, parent=weakref.ref(self))
        self.nodes.append(
            tree
        )
        return tree

    def print(self, offset=0):
        for i in range(offset):
            print("    ", end="")
        print(self.data)

        for node in self.nodes:
            node.print(offset + 1)
