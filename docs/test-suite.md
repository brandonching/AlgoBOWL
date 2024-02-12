# Test Suite

The test suite is located in the `tests` directory. It contains a set of input files (`.in`) and expected output (`.out.valid`) files.

To run the test suite, use the following commands:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

The script will run each program on every input file and compare the output to the expected output. If the output matches the expected output, the test passes. Otherwise, the test fails. Each run also has a timeout of 5 seconds.

Following completion of all test, a summary table will be printed to the console.

## run_tests.sh

The only changes that should be made to the `run_tests.sh` script are the paths to the programs. The script is designed to be run from the root directory of the repository.

Each program should accept two arguments:

1. The input file path
2. The output file path

The script will automatically fill in the input/output file paths for each test.

### Build Configuration

If the implementation requires the program to be built before running the test suite, the build commands should be added to the `run_tests.sh` script.

## GitHub Actions

The repository is configured to run the test suite on every push to the `main` branch. The results of the test suite will be displayed in the "Actions" tab of the repository.
