from src.tree import Tree

a = Tree(1)

b = a.add_node(2)
c = a.add_node(3)

b.add_node(4)
b.add_node(5)
b.add_node(6)

c.add_node(7)
a.print()
