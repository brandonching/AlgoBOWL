# brute force the best solution

import networkx as nx
import sys
import helper as helper
from itertools import combinations


def brute(input_file, output_file, nodes_to_remove=[]):
    # Build Graph
    full_graph = helper.build_graph(input_file)
    if nx.is_directed_acyclic_graph(full_graph):
        # if the graph is already a DAG, then return
        helper.write_output(output_file, [])
        return True

    # convert the nodes_to_remove to a list of integers
    nodes_to_remove = [int(node) for node in nodes_to_remove]

    # remove nodes from the graph if they are in the nodes_to_remove list
    full_graph.remove_nodes_from(nodes_to_remove)

    full_graph = helper.prune_graph(full_graph)

    # Brute force the best solution. Start with the full graph and remove one node at a time until the graph is a DAG. If no solution is found, then try removing two nodes at a time, and so on.

    for chose in range(1, full_graph.number_of_nodes()):
        print("Trying to remove", chose, "nodes")
        all_combinations = generate_combinations(
            full_graph.number_of_nodes(), chose)
        for combination in all_combinations:
            # make a copy of the graph
            graph = full_graph.copy()

            # map the nodes to the new ids
            node_id = sorted(graph.nodes)
            # remove the nodes in the combination
            remove_nodes = [node_id[i-1] for i in combination]
            graph.remove_nodes_from(remove_nodes)
            if nx.is_directed_acyclic_graph(graph):
                for i in remove_nodes:
                    # add the nodes to the nodes_to_remove list
                    nodes_to_remove.append(i)
                helper.write_output(output_file, nodes_to_remove)
                return True


def generate_combinations(num_range, chose):
    numbers = list(range(1, num_range+1))
    all_combinations = list(combinations(numbers, chose))
    return all_combinations


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = "test/algobowl-in/input_group797.in"
    output_file = "test-out/input_group797-brute.out"

    # Run the main function
    brute(input_file, output_file)
