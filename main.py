import sys
import networkx as nx
import helper as helper


def main(input_file, output_file):
    # Build Graph
    G = helper.build_graph(input_file)

    ##############################
    # Check graph and remove nodes
    ##############################

    # test if graph is already a directed acyclic graph
    if nx.is_directed_acyclic_graph(G):
        # if the graph is already a DAG, then return
        helper.write_output(output_file, [])
        return True

    # prune the graph by removing nodes with no parents
    G = helper.prune_graph(G)
    num_nodes = G.number_of_nodes()

    # conduct a traversal on the graph to find the best nodes to remove
    nodes_to_remove = set()
    # default nodes to remove is all nodes
    for node in G:
        nodes_to_remove.add(node)
    for start_node in range(1, num_nodes + 1):
        # Print out progress every 1000 nodes
        if start_node % 1000 == 0:
            print('Progress: ' + str(start_node) + '/' + str(num_nodes))

        # Check if the start node is still in the graph
        if start_node not in G:
            continue
        # initialize a set of unique values to store the nodes to remove
        this_nodes_to_remove = set()
        visited = set()
        stack = [start_node]
        while stack:
            # remove this node from the stack and marked as visited
            node = stack.pop()
            visited.add(node)

            # for each of the node's children, check if it is already visited. If it is, then a cycle is found and the node is added to the list of nodes to remove. If it is not, then add it to the stack
            for child in G[node]:
                if child in visited:
                    this_nodes_to_remove.add(child)
                else:
                    stack.append(child)

        # if this solution is better than the previous best solution, then update the best solution
        if len(this_nodes_to_remove) < len(nodes_to_remove):
            nodes_to_remove = this_nodes_to_remove
            if helper.check_validity(G, nodes_to_remove):
                helper.write_output(output_file, nodes_to_remove)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    main(input_file, output_file)
