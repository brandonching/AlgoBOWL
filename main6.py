import networkx as nx
import helper as helper
import sys


def main(input_file, output_file):
    # Build Graph
    full_graph = helper.build_graph(input_file)
    if nx.is_directed_acyclic_graph(full_graph):
        # if the graph is already a DAG, then return
        helper.write_output(output_file, [])
        return True
    G = helper.prune_graph(full_graph)

    # default to remove all nodes
    nodes_to_remove = set()
    for node in G:
        nodes_to_remove.add(node)

    if helper.check_validity(full_graph, nodes_to_remove):
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

        # remove the node with the highest degree from the cycle
        min_node = None
        min_degree = 100000
        for node in cycle_nodes:
            degree = G.in_degree(node) + G.out_degree(node)
            if degree < min_degree:
                min_node = node
                min_degree = degree

        # remove the node from the graph
        G.remove_node(min_node)
        nodes_to_remove.add(min_node)
        G = helper.prune_graph(G)

    # Write the output
    if helper.check_validity(full_graph, nodes_to_remove):
        helper.write_output(output_file, nodes_to_remove)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    main(input_file, output_file)
