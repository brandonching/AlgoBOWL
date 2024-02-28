import networkx as nx
import helper as helper
import sys
import random


def main(input_file, output_file, target):
    # read the output file
    with open(input_file, 'r') as file:
        # number of nodes to remove from first line
        best_num_nodes = int(file.readline())
        # list of nodes to remove is on the second line separated by spaces
        best_nodes_to_remove = list(map(int, file.readline().split()))

    # convert best_nodes_to_remove to a array of ints
    best_nodes_to_remove = [int(node) for node in best_nodes_to_remove]

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

    shuffle_nodes = best_nodes_to_remove
    random.shuffle(shuffle_nodes)

    # randomly add 50% of the best nodes to remove
    for node in shuffle_nodes[0:int(len(shuffle_nodes)/2)]:
        nodes_to_remove.add(node)
        G.remove_node(node)

    # reprune the graph
    G = helper.prune_graph(G)

    while not nx.is_directed_acyclic_graph(G):
        if len(nodes_to_remove) > target:
            return
        # Find a cycle
        cycle = nx.find_cycle(G)

        # get a list of all the nodes in the cycle
        cycle_nodes = set()
        for edge in cycle:
            cycle_nodes.add(edge[0])

        # remove the node with the highest degree from the cycle
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
        G = helper.prune_graph(G)

    # Write the output
    if helper.check_validity(full_graph, nodes_to_remove):
        helper.write_output(output_file, nodes_to_remove)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    target = int(sys.argv[3])

    # Run the main function
    while True:
        main(input_file, output_file, target)
