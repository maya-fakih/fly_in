"""Graph configuration parser and validation logic."""

from typing import Dict

from parsing_errors import DroneNumberError, FormatError


class GraphParser():
    """Parse graph configuration files and validate their contents."""

    def __init__(self, config: str):
        """Initialize the parser with the path to the configuration file."""
        self.config_file = config
        self.configs = Dict

    def load_file(self):
        """Load and parse the configuration file line by line."""
        first_line = True
        try:
            with open(self.config_file, 'r') as config_file:

                for line in config_file:
                    if line.startswith('#'):
                        continue
                    if first_line:
                        # nb_drone = self.check_first_line(line)
                        first_line = False

        except Exception as e:
            print('[Parsing]: Error!')
            print(e)

    def check_first_line(self, line) -> int:
        """Validate the format of the first configuration line."""
        try:
            self.validate_line(line)
            to_test = line.split(':')
            if to_test[0] != 'nb_drones':
                raise DroneNumberError
            val = to_test[1]
            if isinstance(val, (int)) and not isinstance(val, bool):
                return (int(val))
            else:
                raise DroneNumberError
        except Exception as e:
            raise (e)

    def validate_line(self, line):
        to_test = line.split(':')
        if to_test.len() != 2:
            raise FormatError(line)
