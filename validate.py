import helper as helper
import sys


def main(input_file, output_file):

    if (helper.validate_output(input_file, output_file)):
        print('Output', input_file, ' is valid')
    else:
        print("Input:", input_file, "is invalid")


if __name__ == "__main__":
    # get the input file from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    main(input_file, output_file)
