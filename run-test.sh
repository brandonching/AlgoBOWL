#!/bin/bash
# This script runs the test suite for the project. It runs the build commands (if any) and then runs the programs on the test cases.
# It then checks the output of the programs against the expected output and prints the results.


# list of build commands to run (if any)
# build_commands=("make")  # TODO: Add the build commands here

# for command in "${build_commands[@]}" 
# do
#     echo "Running build command: $command"
#     $command
# done


# Programs to run 
programs=("python3 main.py") # TODO: Add the programs to run here

# List of test files
test_files=$(ls test/input)

# Timeout duration in seconds (maximum time a program is allowed to run per test case)
timeout_duration=10

# Output folder
output_folder="test-out"

# Initialize the arrays to store the statistics
program_pass_count=()
program_total_count=()
program_timeout_count=()
program_time=()


# Get the OS type for OS specific commands
os_type=$(uname)

# Test each program
for program in "${programs[@]}"
do
    echo "---------------------------------"
    echo "Running program: $program"

    # get the start time and initialize the iteration variables
    start_time=$(date +"%s")
    pass_count=0
    total_count=0

    # clean the conetents of the output folder
    rm -rf $output_folder
    mkdir $output_folder

    # For each test file, run the program and check the output
    for file in $test_files
    do
        test_start_time=$(date +"%s")
        # change the output file name from .in to .out
        output_file=$(echo $file | sed 's/.in/.out/')

        # print the test being run
        echo "Running test $file"
            total_count=$((total_count+1))

        # Run the program
        if [ $os_type = "Linux" ]; then
            # Linux
            timeout $timeout_duration $program test/input/$file $output_folder/$output_file
        else
            # Mac
            gtimeout $timeout_duration $program test/input/$file $output_folder/$output_file
        fi

        exit_status=$?

         # Check if program timed out
        if [ $exit_status -eq 124 ]; then
            echo "     [TIMEOUT] The script took longer than $timeout_duration seconds."
            program_timeout_count=$((program_timeout_count+1))
            continue
        fi

        # Check the output (do not print to the console, just check if the output is correct or not)
        diff -q test/output/$output_file.valid $output_folder/$output_file > /dev/null

        # Print the result Pass/Fail
        if [ $? -eq 0 ]
        then
            echo "     [PASS]"
            pass_count=$((pass_count+1))
        else
            echo "     [FAIL]"

            # Print the diff to a file
            diff test/output/$output_file.valid $output_folder/$output_file > test-diff/$output_file.diff
        fi

        test_end_time=$(date +"%s")
        test_duration=$((test_end_time - test_start_time))
        echo "     Test completed in $test_duration seconds"
    done
    
    # get the end time and save the results
    end_time=$(date +"%s")
    program_pass_count+=($pass_count)
    program_total_count+=($total_count)
    program_time+=($((end_time - start_time)))
    echo "Passed $pass_count out of $total_count tests in $((end_time - start_time)) seconds" 

done

echo "----------------------------------------------------------------------------------"
echo "|                               Test Suite Summary                               |"
echo "----------------------------------------------------------------------------------"
printf "| %-20s | %6s | %6s | %8s | %14s | %7s |\n" "Program" "Passed" "Total" "Percentage" "Duration (sec)" "Timeout"
echo "----------------------------------------------------------------------------------"

for program in "${programs[@]}"
do
    index=$(printf "%s\n" "${programs[@]}" | grep -n -m 1 "$program" | cut -d: -f1)
    pass=${program_pass_count[$index-1]}
    total=${program_total_count[$index-1]}
    duration=${program_time[$index-1]}
    timeout=${program_timeout_count[$index-1]}
    # Program | Passed | Total | Percentage | Duration | Timeout
    printf "| %-20s | %6d | %6d | %9.2f%% | %14.2f | %7d |\n" "${program:0:20}" $pass $total $(echo "scale=2; $pass / $total * 100" | bc) $duration $timeout
done

echo "----------------------------------------------------------------------------------"