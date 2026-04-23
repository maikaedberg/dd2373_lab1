import argparse
from regex import match_substrings

def process_file(input_path, graph=False):
    print("processing file:", input_path)
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    if len(lines) < 3:
        raise ValueError("Input file must have at least 3 lines: alphabet, regex, and one test string.")

    alphabet = [s for s in lines[0] if s != '\n']
    regexstr_input = lines[1].strip()
    test_strings = [line.strip() for line in lines[2:] if line.strip()]

    regex_match_result = match_substrings(regexstr_input, alphabet, test_strings, graph)
    for s, match in regex_match_result.items():
        if match:
            print(s)

def main():
    parser = argparse.ArgumentParser()
    # -f or --file for input file
    parser.add_argument("-f", required=True, metavar="filename.txt",
                        help="Input file: line 1 = alphabet, line 2 = regex, line 3+ = strings to test")
    # -g added if we want to generate graph for the NFA / DFA, default is False
    parser.add_argument("-g", action="store_true", help="Generate graph for the NFA / DFA")

    process_file(parser.parse_args().f, parser.parse_args().g)
if __name__ == "__main__":
    main()