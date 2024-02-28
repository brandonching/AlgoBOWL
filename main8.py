import networkx as nx
import helper as helper
import sys
import brute as brute
import time


def main(input_file, output_file):
    # Build Graph
    full_graph = helper.build_graph(input_file)
    if nx.is_directed_acyclic_graph(full_graph):
        # if the graph is already a DAG, then return
        helper.write_output(output_file, [])
        return True
    G = full_graph.copy()
    G = helper.prune_graph(G)
    # default to remove all nodes
    nodes_to_remove = set()

    for node in G:
        nodes_to_remove.add(node)
    if helper.check_validity(full_graph, nodes_to_remove):
        helper.write_output(output_file, nodes_to_remove)

    # reset nodes to remove
    nodes_to_remove = set()

    # create a queue of the SCCs to process
    scc_queue = list(nx.strongly_connected_components(G))
    scc_queue = [scc for scc in scc_queue if len(scc) > 1]

    while len(scc_queue) > 0:
        # get the first scc
        scc = scc_queue.pop(0)

        if scc == 0:
            continue

        # get the subgraph of the scc
        scc_graph = G.subgraph(scc)

        # break the cycles in the graph
        (new_sccs, nodes_removed) = break_scc_cycles(scc_graph)

        # add the new sccs to the queue
        for sub_scc in new_sccs:
            if len(sub_scc) > 1:
                scc_queue.append(sub_scc)

        # add the nodes removed to the nodes to remove
        nodes_to_remove = nodes_to_remove.union(nodes_removed)
        print("Nodes removed: ", nodes_removed)

    # Write the output file
    if helper.check_validity(full_graph, nodes_to_remove):
        helper.write_output(output_file, nodes_to_remove)
    else:
        print("Invalid solution")


def break_scc_cycles(scc_graph):
    '''
    Break the cycles in the graph
    @scc_graph: the graph with the SCCs
    @returns: the graph with the cycles broken
    '''

    scc_graph = scc_graph.copy()
    nodes_removed = set()
    (scc_graph, nodes_removed) = helper.simplify_graph(scc_graph)
    new_sccs = list(nx.strongly_connected_components(scc_graph))
    # only return new_sccs with more than 1 node in them
    new_sccs = [scc for scc in new_sccs if len(scc) > 1]

    # get and array of all the SCCs
    number_of_sccs = 1
    while number_of_sccs == 1:
        print("Nodes removed: ", len(nodes_removed))
        (scc_graph, this_nodes_removed) = helper.simplify_graph(scc_graph)
        nodes_removed = nodes_removed.union(this_nodes_removed)
        # if the graph is already a DAG, then return
        if nx.is_directed_acyclic_graph(scc_graph):
            return (new_sccs, nodes_removed)
        if scc_graph.number_of_edges() == 0:
            return (new_sccs, nodes_removed)
        # find a cycle
        cycle = nx.find_cycle(scc_graph)

        # get the list of all the nodes in the cycle
        cycle_nodes = set()
        for edge in cycle:
            cycle_nodes.add(edge[0])

        # remove the node with the highest degree from the cycle
        max_node = None
        max_degree = -1
        for node in cycle_nodes:
            degree = scc_graph.in_degree(node) + scc_graph.out_degree(node)
            if degree > max_degree:
                max_node = node
                max_degree = degree

        # remove the node from the graph
        scc_graph.remove_node(max_node)
        nodes_removed.add(max_node)

        # Check if there are any more SCCs
        new_sccs = list(nx.strongly_connected_components(scc_graph))
        new_sccs = [scc for scc in new_sccs if len(scc) > 1]

        # get and array of all the SCCs
        number_of_sccs = len(new_sccs)

    new_sccs = list(nx.strongly_connected_components(scc_graph))

    # only return new_sccs with more than 1 node in them
    new_sccs = [scc for scc in new_sccs if len(scc) > 1]

    return (new_sccs, nodes_removed)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    main(input_file, output_file)
