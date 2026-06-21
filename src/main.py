"""Application entry point and runtime orchestration."""

import sys

from parsing import GraphParser


def check_input_arguments():
    """Check if the required input arguments are provided.

    This function ensures that the user has provided the necessary command-line
    arguments for the application to run. If not, it prints a usage message and
    exits the program.
    """
    if len(sys.argv) != 2:
        print('Usage: python main.py <configuration_file>')
        sys.exit(1)


def main():
    """Entry point for the application.

    This function is currently a placeholder for the main program logic.
    """
    check_input_arguments()
    config_file = sys.argv[1]
    parser = GraphParser(config_file)
    parser.load_file()
    if parser.parsing_safe:
        print('Parsing successful.')
    else:
        print('Parsing failed.')


if __name__ == '__main__':
    main()
