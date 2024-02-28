import os
import sys


def sort_output(output_folder):
    # Get a list of all the output files
    output_files = get_file_names(output_folder)

    for output_file in output_files:
        # Get the number of nodes from the first line
        output_file_path = os.path.join(output_folder, output_file)

        # get the nodes from the second line which are space separated
        with open(output_file_path, 'r') as file:
            # get the number of nodes
            num_nodes = int(file.readline().strip())

            # get the nodes
            nodes = file.readline().strip().split(' ')

        # sort the nodes
        nodes.sort()

        # write the sorted nodes back to the file
        with open(output_file_path, 'w') as file:
            # write the number of nodes
            file.write(str(len(nodes)) + '\n')

            # write the sorted nodes separated by a space
            file.write(' '.join(nodes))


def get_file_names(directory_path):
    try:
        # Get the list of file names in the specified directory
        file_names = [f for f in os.listdir(directory_path) if os.path.isfile(
            os.path.join(directory_path, f))]
        return file_names
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return []


if __name__ == "__main__":
    # get the input file from the arguments
    output_folder = "test-out"

    # Run the main function
    sort_output(output_folder)
