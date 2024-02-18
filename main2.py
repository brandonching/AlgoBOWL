import sys
import networkx as nx
import helper as helper

import multiprocessing
import logging


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

    print('Number of nodes: ' + str(num_nodes))
    solutions = {}
    solutions[num_nodes] = nodes_to_remove
    best_solution_length = num_nodes
    block_size = 1000
    # Process a max of 1000 nodes at a time
    for node_block in range(1, num_nodes + 1, block_size):

        block_range = range(node_block, min(
            node_block + block_size, num_nodes + 1))
        print(block_range, best_solution_length)

        # create a pool of workers
        pool = multiprocessing.Pool()

        # map the search_graph function to the pool of workers
        results = pool.starmap(search_graph, zip(
            block_range, [G] * len(block_range)))
        # close the pool
        pool.close()
        pool.join()

        # add the results to the solutions map, the key is the length of the set of nodes to remove and the value is the set of nodes to remove

        for index in range(len(results)):
            if results[index] is not None:
                length = len(results[index])
                if length not in solutions:
                    solutions[length] = set()
                solutions[length].add(index + 1)

                if length < best_solution_length and helper.check_validity(G, results[index]):
                    best_solution_length = length
                    helper.write_output(output_file, results[index])


def search_graph(start_node, graph, output_file=None):
    if start_node % 1000 == 0:
        print('Progress: ' + str(start_node) +
              '/' + str(graph.number_of_nodes()))

    # if the start node is not in the graph, then return
    if start_node not in graph:
        return

    # initialize a set of unique values to store the nodes to remove
    this_nodes_to_remove = set()
    visited = set()
    stack = [start_node]
    while stack:
        # remove this node from the stack and marked as visited
        node = stack.pop()
        visited.add(node)
        # for each of the node's children, check if it is already visited. If it is, then a cycle is found and the node is added to the list of nodes to remove. If it is not, then add it to the stack
        for child in graph[node]:
            if child in visited:
                this_nodes_to_remove.add(node)
            else:
                stack.append(child)

    return this_nodes_to_remove


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
