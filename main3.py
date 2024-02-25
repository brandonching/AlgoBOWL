import networkx as nx
import helper as helper
import sys


def main(input_file, output_file):
    # Build Graph
    G = helper.build_graph(input_file)
    if nx.is_directed_acyclic_graph(G):
        # if the graph is already a DAG, then return
        helper.write_output(output_file, [])
        return True
    G = helper.prune_graph(G)
    num_nodes = G.number_of_nodes()

    # default to remove all nodes
    nodes_to_remove = set()
    for node in G:
        nodes_to_remove.add(node)

    helper.write_output(output_file, nodes_to_remove)

    # reset nodes to remove
    nodes_to_remove = set()

    while not nx.is_directed_acyclic_graph(G):
        # Find a cycle
        cycle = nx.find_cycle(G)

        # get a list of all the nodes in the cycle
        cycle_nodes = set()
        for edge in cycle:
            cycle_nodes.add(edge[0])
            cycle_nodes.add(edge[1])

        # remove the node with the highest out degree + in degree
        max_node = None
        max_degree = -1
        for node in cycle_nodes:
            degree = G.in_degree(node) + G.out_degree(node)
            if degree > max_degree:
                max_node = node
                max_degree = degree

        # remove the node from the graph
        G.remove_node(max_node)
        nodes_to_remove.add(max_node)

    # Write the output
    helper.write_output(output_file, nodes_to_remove)


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
