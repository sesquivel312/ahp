def traverse_tree(start_node, children_attribute='children', visited_nodes=[], leaf_nodes=[]):
    """
    traverse a tree of objects returning a list of all nodes and a list of only leaf nodes
         
    Args:
        children_attribute(string): name of object attribute containing the list of child objects 
        start_node(object): object with a compatible 'children' attribute that is a list of objects of the same type
        visited_nodes(list): list to be filled with all nodes in the tree
        leaf_nodes(list): list to be filled with only leaf objects in the tree 

    Returns(tuple): 2-tuple of lists - (visited_nodes, leaf_nodes)

    """

    visited_nodes.append(start_node)

    if start_node.children:
        for child in start_node.children:
            traverse_tree(child, visited_nodes=visited_nodes, leaf_nodes=leaf_nodes)
    else:
        leaf_nodes.append(start_node)

    return visited_nodes, leaf_nodes