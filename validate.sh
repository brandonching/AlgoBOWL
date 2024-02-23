#!/bin/bash

# List of test files
test_files=$(ls test/input)

for file in $test_files
do
    # change the output file name from .in to .out
    output_file=$(echo $file | sed 's/.in/.out/')

    # Run the program
    timeout 300 python3 validate.py test/input/$file test-out/$output_file

    exit_status=$?
    if [ $exit_status -eq 124 ]; then
        echo "Program timed out"
    fi
done