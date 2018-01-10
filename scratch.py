class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_children(self, nodes):
        """
        add child nodes to the list of children

        Args:
            nodes(list): List of Node objects

        Returns(None):

        """

        self.children.extend(nodes)
        for node in nodes:
            node.parent = self


def traverse(start_node, visited_nodes=[], leaf_nodes=[]):
    visited_nodes.append(start_node)

    if start_node.children:
        for child in start_node.children:
            traverse(child, visited_nodes, leaf_nodes)
    else:
        leaf_nodes.append(start_node)

    return visited_nodes, leaf_nodes


n0 = Node('root-0')
n01 = Node('child-01')
n011 = Node('gchild-011')
n012 = Node('gchild-012')
n02 = Node('child-02')
n021 = Node('gchild-021')
n03 = Node('child-03')

n0.add_children([n01, n02, n03])
n01.add_children([n011, n012])
n02.add_children([n021])

visited, leaves = traverse(n0)
print('tree')
for i in visited:
    print i.name
print('\nleaves')
for i in leaves:
    print i.name
