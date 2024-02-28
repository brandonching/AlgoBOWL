

import helper as helper
import sys
import networkx as nx


def main(edges_file, input_file, output_file):
    # Read the edges from the file
    # open the output file
    with open(edges_file, 'r') as file:
        edges = file.read().split("\n")

    node_frequency = {}
    for edge in edges:
        # split the edge into two nodes
        edge = edge.split(" ")

        # add the nodes to the frequency dictionary
        for node in edge:
            if node in node_frequency:
                node_frequency[node] += 1
            else:
                node_frequency[node] = 1

    # Sort the nodes by frequency highest to lowest
    sorted_nodes = sorted(node_frequency, key=node_frequency.get, reverse=True)

    # remove any nodes that are not numbers
    sorted_nodes = [node for node in sorted_nodes if node.isdigit()]

    total_degree = []
    frequency_weight = []

    # Build Graph
    full_graph = helper.build_graph(input_file)

    for node in sorted_nodes:
        total_degree.append(full_graph.in_degree(
            int(node)) + full_graph.out_degree(int(node)))
        frequency_weight.append(node_frequency[node]/total_degree[-1])

    # resort the nodes by frequency/degree
    sorted_nodes = [x for _, x in sorted(
        zip(frequency_weight, sorted_nodes), reverse=True)]

    node_index = 0
    for node in sorted_nodes:
        print("Removing node: ", node,
              " with frequency/total_degree: ", node_frequency[node] / total_degree[node_index])
        # convert the node to an integer
        node = int(node)
        # remove the node from the graph
        full_graph.remove_node(node)
        node_index += 1

        # Check if the graph is a directed acyclic graph (valid solution)
        if nx.is_directed_acyclic_graph(full_graph):
            # Write the output
            helper.write_output(output_file, sorted_nodes[:node_index])
            return


if __name__ == "__main__":
    # get the input file from the arguments
    edges_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    main(edges_file, input_file, output_file)
