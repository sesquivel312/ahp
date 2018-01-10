def traverse_tree(start_node, visited_nodes=[], leaf_nodes=[], children_attribute='children'):
    """
    traverse a tree of objects returning a list of all nodes and a list of only leaf nodes
         
    Args:
        children_attribute(string): name of object attribute containing the list of child objects 
        start_node(object): object with a compatible 'children' attribute that is a list of objects of the same type
        visited_nodes(list): list to be filled with all nodes in the tree
        leaf_nodes(list): list to be filled with only leaf objects in the tree 

    Returns(tuple): 2-tuple of lists - (visited_nodes, leaf_nodes)

    """

    children = getattr(start_node, children_attribute)
    visited_nodes.append(start_node)

    if children:
        for child in children:
            traverse_tree(child, visited_nodes, leaf_nodes, children_attribute)
    else:
        leaf_nodes.append(start_node)

    return visited_nodes, leaf_nodes