# decode an output file from the encoder

import os
import sys


def main(output_file, id_map_file):
    # Open the id map file
    id_map = []
    with open(id_map_file, 'r') as f:
        for line in f:
            # save the second number in the line
            id_map.append(int(line.split()[1]))

    encoded_output = []
    # Open the output file
    with open(output_file, 'r') as f:
        # skip the first line
        f.readline()

        # the next line is the list of encoded nodes separated by spaces
        encoded_output = list(map(int, f.readline().split()))

    # decode the output
    decoded_output = []
    for node in encoded_output:
        decoded_output.append(id_map[node-1])

    # write the decoded output to a file
    with open(output_file.replace(".out", "") + "-decoded.out", 'w') as f:
        # the first line is the number of nodes
        f.write(str(len(decoded_output)) + "\n")

        # the next line is the list of decoded nodes separated by spaces
        for node in decoded_output:
            f.write(str(node) + " ")
        f.write("\n")


if __name__ == "__main__":
    # get the input file from the arguments
    output_file = sys.argv[1]
    id_map_file = sys.argv[2]

    # Run the main function
    main(output_file, id_map_file)
