# This script generates the final output file for the project.

import networkx as nx
import helper as helper
import sys
import matplotlib.pyplot as plt


def main(output_file):
    # Create a blank graph
    G = nx.DiGraph()

    # Add the cornerstone node to the graph (node 0)
    G.add_node(0)

    # For 1-10 add the node and edges from i to i+1
    for i in range(1, 11):
        G.add_node(i)
        if i != 10:
            G.add_edge(i - 1, i)
        else:
            G.add_edge(i, 0)

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1500,
            node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
    plt.show()


if __name__ == "__main__":
    output_file = "test/input/00-final.in"

    # Run the main function
    main(output_file)
