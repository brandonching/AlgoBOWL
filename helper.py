import networkx as nx
import sys


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

    # add nodes with no children to the list of nodes to remove

    # Remove the nodes from the graph
    graph.remove_nodes_from(nodes_to_remove)

    # recursively prune the graph until no more nodes with no parents are found
    if len(nodes_to_remove) > 0:
        return prune_graph(graph)
    else:
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

    # Create a map to count the number of children for each node
    children_count = {}
    parents_count = {}
    for node in graph:
        children_count[node] = len(list(graph.successors(node)))
        parents_count[node] = len(list(graph.predecessors(node)))

    # Print the number of children for each node
    print('Children count:')
    for child_size in set(children_count.values()):
        print(str(child_size),
              str(list(children_count.values()).count(child_size)))

    # Print the number of parents for each node
    print('Parents count:')
    for parent_size in set(parents_count.values()):
        print(str(parent_size),
              str(list(parents_count.values()).count(parent_size)))


def write_output(output_file, solution):
    '''
    Write the output file
    '''
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


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Build the graph from the input file
    G = build_graph(input_file)

    # Get the nodes to remove from the output file
    nodes_to_remove = get_nodes_to_remove_from_output(output_file)

    # Check if the solution is valid
    print(check_validity(G, nodes_to_remove))
