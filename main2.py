# Simple blank script to test the auto test script is working

import sys


def main():
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # open the input file
    with open(input_file, 'r') as file:
        # read the input file
        input_data = file.read()

    # copy the input file to the output file
    with open(output_file, 'w') as file:
        file.write(input_data)


if __name__ == "__main__":
    main()
