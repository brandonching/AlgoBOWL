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
