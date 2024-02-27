# Basic script to call the algobowl CLI to submit all the solutions
output_folder="test/algobowl-out"

for file in $(ls $output_folder); do
    echo "Submitting $file"
    # run the algoboal executable
    # algobowl group output upload <path-to-solution>
    ./algobowl group output upload $output_folder/$file
done