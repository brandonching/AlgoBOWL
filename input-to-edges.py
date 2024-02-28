# Takes an inout file and exports an edges file

import helper as helper
import sys
import os


def main(input_file, edges_file):
    # Build Graph
    full_graph = helper.build_graph(input_file)

    all_edges = sorted(full_graph.edges())

    # convert each edge to a string "a b" and join them with a newline
    edges = "\n".join([" ".join(map(str, edge)) for edge in all_edges])

    # Create the edges file
    with open(edges_file, "w") as file:
        file.write(edges)


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    edges_file = sys.argv[2]

    main(input_file, edges_file)
