# This script generates the final output file for the project.

import networkx as nx
import helper as helper
import sys
import random


def main(output_file):
    # Create a blank graph
    G = nx.DiGraph()
    pos = nx.spring_layout(G)
    pos_index = 1

    # Add the cornerstone node to the graph (node 0)
    G.add_node(0)
    # set the position of the cornerstone node to (0,0)
    pos[0] = (0, 0)

    # For 1-10 add the node and edges from i to i+1
    for j in range(1, 101):
        for i in range(1, 11):
            node_id = i + (j-1)*10
            G.add_node(node_id)

            if i == 1 and j != 1:
                G.add_edge(node_id-10, node_id)
            elif i == 10:
                G.add_edge(node_id, node_id - 10)
                G.add_edge(node_id - 1, node_id)
            else:
                G.add_edge(node_id - 1, node_id)

        pos_index += 1
    # Draw the graph

    # for every node in the graph, if the current total degree is not 4, randomly add edges to from this node to any node where the last digit is greater than the current nodes last digit. Only add an edge if the total degree of the other node is less than 4. If no other node is found do nothing
    max_degree = 15
    for node in G:
        # skip the 0 node
        if node == 0 and G.out_degree(0) > max_degree/2:
            continue
        attempt = 0
        while G.in_degree(node) + G.out_degree(node) != max_degree:
            attempt += 1

            if attempt > 10:
                attempt = 0
                break
            # get the last digit of the current node
            last_digit = node % 10
            possible_nodes = []
            if last_digit == 0:
                # set possible nodes to all nodes with a last digit of 10 and the total node number is greater than the current node
                possible_nodes = [n for n in G if n % 10 == 0 and n < node]

            else:
                # get the nodes where the last digit is greater than the current node
                possible_nodes = [n for n in G if n % 10 > last_digit]

                if ((G.out_degree(0) + G.in_degree(0)) < max_degree):
                    possible_nodes.append(0)
            # remove the nodes where the total degree is equal to or greater than max_degree
            possible_nodes = [
                n for n in possible_nodes if G.in_degree(n) + G.out_degree(n) < max_degree]
            if len(possible_nodes) == 0:
                break

            # get a random node from the possible nodes
            random_node = possible_nodes[random.randint(
                0, len(possible_nodes)-1)]

            # check if there is already an edge between the current node and the random node
            if G.has_edge(node, random_node):
                continue
            else:
                # add an edge from the current node to the first possible node
                G.add_edge(
                    node, possible_nodes[random.randint(0, len(possible_nodes)-1)])

    # For every node if the current total degree is 2 or more less than the max, add annother node that is a child and parent of the current node
    for node in range(0, len(G.nodes)-1):
        if G.in_degree(node) + G.out_degree(node) < max_degree - 2:
            new_node = max(G.nodes) + 1
            G.add_node(new_node)
            G.add_edge(node, new_node)
            G.add_edge(new_node, node)

    # Create a bunch of fully connected graphs
    for i in range(0, 20):
        offset = max(G.nodes)
        # Create a fully connected graph with the next 16 nodes
        for i in range(1, 17):
            # Create a node
            G.add_node(offset+i)

            # Connect the node to all other nodes
            for j in range(1, 17):
                if i != j:
                    G.add_edge(i+offset, j+offset)

    # Create a bunch of fully connected graphs this time with only 7 nodes
    for i in range(0, 20):
        offset = max(G.nodes)
        # Create a fully connected graph with the next 16 nodes
        for i in range(1, 8):
            # Create a node
            G.add_node(offset+i)

            # Connect the node to all other nodes
            for j in range(1, 8):
                if i != j:
                    G.add_edge(i+offset, j+offset)

    # Create to sets of chains
    for i in range(0, 2):
        chain_length = 100
        # reset the offset
        offset = max(G.nodes) + 1
        # Create a chain of 100 nodes
        node_ids = []
        for i in range(0, chain_length):
            this_node_id = i + offset
            G.add_node(this_node_id)
            node_ids.append(this_node_id)

        # Add the edges to the chain
        for i in range(0, chain_length):
            this_node_id = node_ids[i]
            # start of chain
            if i == 0:
                G.add_edge(this_node_id, node_ids[1])
                G.add_edge(this_node_id, node_ids[2])
                G.add_edge(this_node_id, node_ids[3])

                G.add_edge(this_node_id, node_ids[chain_length-1])
                G.add_edge(this_node_id, node_ids[chain_length-2])
                G.add_edge(this_node_id, node_ids[chain_length-3])
            elif i == 1:
                G.add_edge(this_node_id, node_ids[2])
                G.add_edge(this_node_id, node_ids[3])
                G.add_edge(this_node_id, node_ids[4])

                G.add_edge(this_node_id, node_ids[0])
                G.add_edge(this_node_id, node_ids[chain_length-1])
                G.add_edge(this_node_id, node_ids[chain_length-2])
            elif i == 2:
                G.add_edge(this_node_id, node_ids[3])
                G.add_edge(this_node_id, node_ids[4])
                G.add_edge(this_node_id, node_ids[5])

                G.add_edge(this_node_id, node_ids[1])
                G.add_edge(this_node_id, node_ids[0])
                G.add_edge(this_node_id, node_ids[chain_length-1])
            elif i == 99:
                G.add_edge(this_node_id, node_ids[0])
                G.add_edge(this_node_id, node_ids[1])
                G.add_edge(this_node_id, node_ids[2])

                G.add_edge(this_node_id, node_ids[chain_length-2])
                G.add_edge(this_node_id, node_ids[chain_length-3])
                G.add_edge(this_node_id, node_ids[chain_length-4])
            elif i == 98:
                G.add_edge(this_node_id, node_ids[chain_length-1])
                G.add_edge(this_node_id, node_ids[0])
                G.add_edge(this_node_id, node_ids[1])

                G.add_edge(this_node_id, node_ids[chain_length-3])
                G.add_edge(this_node_id, node_ids[chain_length-4])
                G.add_edge(this_node_id, node_ids[chain_length-5])
            elif i == 97:
                G.add_edge(this_node_id, node_ids[chain_length-2])
                G.add_edge(this_node_id, node_ids[chain_length-1])
                G.add_edge(this_node_id, node_ids[0])

                G.add_edge(this_node_id, node_ids[chain_length-4])
                G.add_edge(this_node_id, node_ids[chain_length-5])
                G.add_edge(this_node_id, node_ids[chain_length-6])
            else:
                G.add_edge(this_node_id, node_ids[i+1])
                G.add_edge(this_node_id, node_ids[i+2])
                G.add_edge(this_node_id, node_ids[i+3])

                G.add_edge(this_node_id, node_ids[i-1])
                G.add_edge(this_node_id, node_ids[i-2])
                G.add_edge(this_node_id, node_ids[i-3])

    # reset the offset
    offset = max(G.nodes) + 1

    # Just randomize the rest of the nodes
    remaining_nodes = range(offset, 10000)

    # number of nodes and edges remaining
    remaining_nodes = 10000 - G.number_of_nodes()
    remaining_edges = 100000 - G.number_of_edges()
    print("Remaining nodes: " + str(remaining_nodes))
    print("Remaining edges: " + str(remaining_edges))

    average_degree = int(remaining_edges / remaining_nodes)
    print("Average degree: " + str(average_degree))
    for node in range(offset, 10000):
        G.add_node(node)
    for node in range(offset, 10000):
        # Connect a list of random numbers of size +-5 from the average degree
        random_list = random.sample(range(0, 10000), random.randint(
            average_degree-5, average_degree+5))
        for random_node in random_list:
            if (random_node != node):
                G.add_edge(node, random_node)

    # Add the last few edges at complete random
    while (G.number_of_edges() < 100000):
        node1 = random.randint(0, 10000)
        node2 = random.randint(0, 10000)
        while (node1 == node2):
            node2 = random.randint(0, 10000)
        G.add_edge(node1, node2)

    # Open the file for writing
    with open(output_file, "w") as file:
        # Write the number of nodes
        file.write(str(G.number_of_nodes()) + "\n")

        # Write the edges
        node_index = 1
        for node in sorted(G.nodes()):
            number_of_parents = len(list(G.predecessors(node)))
            list_of_parents = list(G.predecessors(node))

            # Write the node number
            # TODO: USEFUL TO DEBUG DO NOT USE IN FINAL VERSION
            # file.write(str(node + 1) + " ")

            # Write the number of parents
            file.write(str(number_of_parents) + " ")
            # Write the list of parents
            for parent in list_of_parents:
                if (parent + 1) != node_index:
                    file.write(str(parent + 1) + " ")
                else:
                    file.write(str(parent) + " ")
                    print(
                        "ERROR: Parent is the same as the child for node:" + str(node_index))

            # End the line
            file.write("\n")
            node_index += 1

    print("Output file generated at " + output_file)
    print("Number of nodes: " + str(G.number_of_nodes())
          + " Number of edges: " + str(G.number_of_edges()))


if __name__ == "__main__":
    output_file = "test/input/00-final.in"

    # Run the main function
    # output file is the location and name of the file this script will generate (project input)
    main(output_file)
