# Project 1 Python

## Run instructions

Use Python 3 to run the main script:

    python3 main.py

Optional flags:

- `-f <filename>` : specify the input filename
- `-g` : generate graphs

Examples:

    python3 main.py -f input/input.txt
    python3 main.py -f input/input.txt -g

## Testing instructions

Use Python unittests to run tests!

To run all tests at once:

    python3 -m unittest discover tests

To run each individual test:

    python3 -m unittest tests.test_basic
    python3 -m unittest tests.test_large
    python3 -m unittest tests.test_provided

## Performance Logging
To get the tables generated for the report run:

    python3 performance_logger.py

