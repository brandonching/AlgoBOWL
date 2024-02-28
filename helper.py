import networkx as nx
import sys
import matplotlib as mpl


def check_validity(graph, nodes_to_remove):

    # Remove the nodes from the graph
    G = graph.copy()
    G.remove_nodes_from(nodes_to_remove)

    # Check if the graph is a directed acyclic graph (valid solution)
    return nx.is_directed_acyclic_graph(G)


def build_graph(input_file):
    '''
    Build a directed graph from the input file
    @input_file: the input file
    @returns: a directed graph
    '''
    # open the input file
    with open(input_file, 'r') as file:
        # read the input file
        input_data = file.read()

    # Get the number of nodes from the first line of the input file
    num_nodes = int(input_data.split('\n')[0])

    # Create a graph and add the nodes
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_nodes + 1))

    # Add the edges from the input file
    parent_node = 1
    for line in input_data.split('\n')[1:]:
        # Split the line into a list of numbers
        nodes = list(map(int, line.split()))

        # if there is no parent, delete the node
        if len(nodes) == 1:
            G.remove_node(parent_node)
            parent_node += 1
            continue

        # Add the edges to the graph
        for child in nodes[1:]:
            G.add_edge(child, parent_node)

        parent_node += 1

    return G


def get_nodes_to_remove_from_output(output_file):
    '''
    Get the list of nodes to remove from the output file
    @output_file: the output file
    @returns: a list of nodes to remove
    '''
    # open the output file
    with open(output_file, 'r') as file:
        # read the output file
        output_data = file.read()

    # List of nodes to remove is the second line of the output file
    nodes_to_remove = list(map(int, output_data.split('\n')[1].split()))

    return nodes_to_remove


def prune_graph(graph):
    '''
    Prune the graph of any nodes with no parents
    @graph: the graph to prune
    @returns: the pruned graph
    '''
    # Get the nodes with no parents
    nodes_to_remove = [
        node for node in graph.nodes if graph.in_degree(node) == 0]

    while len(nodes_to_remove) > 0:
        # Remove the nodes from the graph
        graph.remove_nodes_from(nodes_to_remove)

        # Get the nodes with no parents
        nodes_to_remove = [
            node for node in graph.nodes if graph.in_degree(node) == 0]

    # add nodes with no children to the list of nodes to remove
    nodes_to_remove += [
        node for node in graph.nodes if graph.out_degree(node) == 0]

    while len(nodes_to_remove) > 0:
        # Remove the nodes from the graph
        graph.remove_nodes_from(nodes_to_remove)

        # Get the nodes with no parents
        nodes_to_remove = [
            node for node in graph.nodes if graph.out_degree(node) == 0]

    return graph


def report_graph_stats(graph):
    '''
    Report the statistics of the graph
    @graph: the graph
    '''
    print('Number of nodes: ' + str(graph.number_of_nodes()))
    print('Number of edges: ' + str(graph.number_of_edges()))
    print('Is directed acyclic graph: ' +
          str(nx.is_directed_acyclic_graph(graph)))


def write_output(output_file, solution):
    '''
    Write the output file
    '''
    # sort the solution
    solution = sorted(solution)

    # open the output file
    with open(output_file, 'w') as file:
        # write the number of nodes to remove
        file.write(str(len(solution)) + '\n')
        # write the nodes to remove
        file.write(' '.join(map(str, solution)))


def validate_output(input_file, output_file):
    '''
    Validate the output file
    '''
    # Build the graph from the input file
    G = build_graph(input_file)

    # Get the nodes to remove from the output file
    nodes_to_remove = get_nodes_to_remove_from_output(output_file)

    # Check if the solution is valid
    return check_validity(G, nodes_to_remove)


def simplify_graph(graph):
    '''
    This function simplifies the graph by condensing linear paths of nodes
    '''
    # prune the graph to remove nodes with no parents and no children

    graph = graph.copy()
    start = len(graph.nodes)
    nodes_removed = set()

    # prune the graph to remove nodes with no parents and no children
    graph = prune_graph(graph)

    # get a list of nodes where in_degree = 1 and out_degree = 1
    linear_nodes = [node for node in graph.nodes if graph.in_degree(
        node) == 1 and graph.out_degree(node) == 1]

    # get a subgraph of the linear nodes
    linear_subgraph = graph.subgraph(linear_nodes).copy()

    # test if the linear subgraph is a cycle
    while not nx.is_directed_acyclic_graph(linear_subgraph):
        cycle = nx.find_cycle(linear_subgraph)
        linear_subgraph.remove_node(cycle[0][0])
        graph.remove_node(cycle[0][0])
        nodes_removed.add(cycle[0][0])
        linear_nodes.remove(cycle[0][0])

    # For each linear node, remove the node and connect the parent to the child
    while len(linear_nodes) > 0:
        node = linear_nodes[0]
        # test if the graph needs to be pruned
        if graph.in_degree(node) == 0 or graph.out_degree(node) == 0:
            graph = prune_graph(graph)
            linear_nodes = [node for node in graph.nodes if graph.in_degree(
                node) == 1 and graph.out_degree(node) == 1]
            continue
        # skip if self loop
        if list(graph.predecessors(node))[0] == node and list(graph.successors(node))[0] == node:
            continue
        parent = list(graph.predecessors(node))[0]
        child = list(graph.successors(node))[0]
        graph.add_edge(parent, child)
        graph.remove_node(node)

        # get a list of nodes where in_degree = 1 and out_degree = 1
        linear_nodes = [node for node in graph.nodes if graph.in_degree(
            node) == 1 and graph.out_degree(node) == 1]

    # list of nodes with in_degree = 1
    in_degree_one_nodes = [
        node for node in graph.nodes if graph.in_degree(node) == 1]

    while len(in_degree_one_nodes) > 0:
        # get the first node in the list
        node = in_degree_one_nodes[0]
        # test if the graph needs to be pruned
        if graph.in_degree(node) == 0 or graph.out_degree(node) == 0:
            graph = prune_graph(graph)
            in_degree_one_nodes = [
                node for node in graph.nodes if graph.in_degree(node) == 1]
            continue

        # connect the parent to all the children
        parent = list(graph.predecessors(node))[0]
        children = list(graph.successors(node))
        for child in children:
            graph.add_edge(parent, child)
        graph.remove_node(node)

        in_degree_one_nodes = [
            node for node in graph.nodes if graph.in_degree(node) == 1]

    # list of nodes with out_degree = 1
    out_degree_one_nodes = [
        node for node in graph.nodes if graph.out_degree(node) == 1]
    while len(out_degree_one_nodes) > 0:
        # get the first node in the list
        node = out_degree_one_nodes[0]
        # test if the graph needs to be pruned
        if graph.in_degree(node) == 0 or graph.out_degree(node) == 0:
            graph = prune_graph(graph)
            out_degree_one_nodes = [
                node for node in graph.nodes if graph.out_degree(node) == 1]
            continue
        # connect the child to all the parents
        child = list(graph.successors(node))[0]
        parents = list(graph.predecessors(node))
        for parent in parents:
            graph.add_edge(parent, child)
        graph.remove_node(node)
        out_degree_one_nodes = [
            node for node in graph.nodes if graph.out_degree(node) == 1]

    # remove the list of nodes with self loops
    self_loop_nodes = list(nx.nodes_with_selfloops(graph))
    for node in self_loop_nodes:
        graph.remove_node(node)
        nodes_removed.add(node)

    print("Size simplified graph: ", start-len(graph.nodes))

    # Return the simplified graph
    return (graph, nodes_removed)


def draw_graph(graph, center_node=None):
    '''
    Draw the graph
    '''
    # Create a shell layout
    pos = nx.shell_layout(graph)

    # Set the center node
    if center_node:
        pos[center_node] = [0, 0]

    # Draw the graph
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1,
            font_size=10, font_color='black', font_weight='bold', alpha=0.9, arrowsize=20)

    # Show the graph
    mpl.pyplot.show()


def get_subgraph(graph, node, depth):
    '''
    Get the subgraph of the nodes
    '''
    nodes_in_subgraph = set()
    nodes_to_process = [(node, depth)]
    while len(nodes_to_process) > 0:
        (node, depth) = nodes_to_process.pop(0)
        nodes_in_subgraph.add(node)

        # get the children of the node
        children = list(graph.successors(node))
        for child in children:
            if child not in nodes_in_subgraph and depth > 0:
                nodes_to_process.append((child, depth - 1))

        # get the parents of the node
        parents = list(graph.predecessors(node))
        for parent in parents:
            if parent not in nodes_in_subgraph and depth > 0:
                nodes_to_process.append((parent, depth - 1))

    return graph.subgraph(nodes_in_subgraph)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Build the graph from the input file
    G = build_graph(input_file)

    draw_graph(get_subgraph(G, 2340, 3), 2340)
