import sys
import networkx as nx
import tools.helper as helper


def main(input_file, output_file):
    # Build Graph
    G = helper.build_graph(input_file)
    num_nodes = G.number_of_nodes()

    ##############################
    # Check graph and remove nodes
    ##############################

    # test if graph is already a directed acyclic graph
    if nx.is_directed_acyclic_graph(G):
        return True

    # conduct a traversal on the graph to find the best nodes to remove
    nodes_to_remove = []
    for start_node in range(1, num_nodes + 1):
        this_nodes_to_remove = []
        visited = set()
        stack = [start_node]
        while stack:
            node = stack.pop()
            if node in visited:
                # cycle found
                this_nodes_to_remove.append(node)
                break
            visited.add(node)
            stack.extend(G.successors(node))

        # append this solution to the list of solutions
        nodes_to_remove.append(this_nodes_to_remove)

    ##############################
    # Find the best solution
    ##############################

    # sort the list of solutions by length
    nodes_to_remove.sort(key=len)
    # default solution to remove all nodes
    solution = list(range(1, num_nodes + 1))
    for nodes in nodes_to_remove:
        if helper.check_validity(G, nodes):
            solution = nodes

    ##############################
    # Write output file
    ##############################

    # open the output file
    with open(output_file, 'w') as file:
        # write the number of nodes to remove
        file.write(str(len(solution)) + '\n')
        # write the nodes to remove
        file.write(' '.join(map(str, solution)))


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function 1e5 times
    main(input_file, output_file)
