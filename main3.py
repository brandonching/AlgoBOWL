import networkx as nx
import helper as helper
import sys


def main(input_file, output_file):
    # Build Graph
    G = helper.build_graph(input_file)
    if nx.is_directed_acyclic_graph(G):
        return True
    G = helper.prune_graph(G)
    num_nodes = G.number_of_nodes()

    # default to remove all nodes
    nodes_to_remove = set()
    for node in G:
        nodes_to_remove.add(node)

    helper.write_output(output_file, nodes_to_remove)

    # attempt to brute force the solution by removing nodes and checking if the graph is still a DAG
    solutions = {}
    solutions[num_nodes] = nodes_to_remove
    best_solution_length = num_nodes
    block_size = 1000
    # Process a max of 1000 nodes at a time

    for node_block in range(1, num_nodes + 1, block_size):

        block_range = range(node_block, min(
            node_block + block_size, num_nodes + 1))

        for node in block_range:
            # remove the node from the graph
            G.remove_node(node)
            # check if the graph is still a DAG
            if nx.is_directed_acyclic_graph(G):
                # if it is, add the node to the solution
                if len(G.nodes) not in solutions:
                    solutions[len(G.nodes)] = set()
                solutions[len(G.nodes)].add(node)
                if len(G.nodes) < best_solution_length and helper.check_validity(G, G.nodes):
                    best_solution_length = len(G.nodes)
                    helper.write_output(output_file, G.nodes)
            else:
                # if it is not, add the node back to the graph
                G.add_node(node)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    main(input_file, output_file)

    # Validate the output
    if helper.validate_output(input_file, output_file):
        print('Output is valid')
    else:
        print('Output is invalid')
