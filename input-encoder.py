# pretty basic function, it takes the an input file and sorts it/renumbers nodes
# this makes it hard to visualize any trends in the input file, but preserves the
# structure of the graph

import sys
import os
import random


def main(input_file):
    number_of_nodes = -1
    parent_array = []
    # Open the file
    with open(input_file, 'r') as f:
        # Read the first line to get the number of nodes
        number_of_nodes = int(f.readline())

        # Read the rest of the lines to get the parent array
        # ignore the first number in the line
        for line in f:
            parents = line.split()
            this_node_parent = []
            for parent in parents:
                this_node_parent.append(int(parent))
            # remove the first number in the line
            this_node_parent.pop(0)
            parent_array.append(this_node_parent)

    size_map = {}
    # key is the number of parents, and the value is a list of node ids
    for i in range(0, number_of_nodes):
        parent_count = len(parent_array[i])
        if parent_count in size_map:
            size_map[parent_count].append(i)
        else:
            size_map[parent_count] = [i]

    map_keys = sorted(list(size_map.keys()))

    new_id = [0]*10000

    next_id = 1
    for key in map_keys:
        nodes_in_size = sorted(size_map[key])
        for node in nodes_in_size:
            new_id[node] = next_id
            next_id += 1

    # write the new input file
    with open(input_file.replace(".in", "") + "-encoded.in", 'w') as f:
        f.write(str(number_of_nodes) + "\n")
        for key in map_keys:
            nodes_in_size = sorted(size_map[key])
            for node in nodes_in_size:
                f.write(str(len(parent_array[node])) + " ")
                for parent in parent_array[node]:
                    f.write(str(new_id[parent-1]) + " ")
                f.write("\n")



if __name__ == "__main__":
    input_file = "test/input/00-0-final.in"
    main(input_file)
