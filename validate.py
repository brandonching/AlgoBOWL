import helper as helper
import sys
import os


def main(input_folder, output_folder):

    # Get a list of all the input files
    output_files = get_file_names(output_folder)

    for output_file in output_files:
        # Get the corresponding output file
        output_file_path = os.path.join(output_folder, output_file)
        input_file = output_file.replace('out', 'in')
        input_file_path = os.path.join(input_folder, input_file)
        validate(input_file_path, output_file_path)


def validate(input_file, output_file):
    if (helper.validate_output(input_file, output_file)):
        # rename the file to add the .valid extension
        os.rename(output_file, output_file + '.valid')
        print('Output', output_file, ' is valid for', input_file)
        return True
    else:
        # rename the file to add the .invalid extension
        os.rename(output_file, output_file + '.invalid')
        print('Output', output_file, ' is not valid for', input_file)
        return False


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
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Run the main function
    main(input_file, output_file)
