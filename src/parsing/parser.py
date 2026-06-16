"""Graph configuration parser and validation logic."""

from typing import Dict, List

from parsing_errors import DroneNumberError, FormatError


class GraphParser():
    """Parse graph configuration files and validate their contents."""

    def __init__(self, config: str):
        """Initialize the parser with the path to the configuration file."""
        self.config_file = config
        self.configs = {}
        self.parsing_safe = False
        self.hub_state = 1

    def load_file(self):
        """Load and parse the configuration file line by line."""
        state = 1
        try:
            with open(self.config_file, 'r') as config_file:

                for line in config_file:
                    if line.startswith('#'):
                        continue
                    if state == 1:
                        self.configs["nb_drones"] = self.check_first_line
                        self.configs["hubs"] = {}
                        state = 2
                    elif state == 2:
                        pass
                    elif state == 3:
                        pass
            self.parsing_safe = True
        except Exception as e:
            print('[Parsing]: Error!')
            print(e)

    def validate_hub(self, line) -> Dict:
        parts = self.validate_line(line)
        # here i should parse lines, validate hubs, w then check the self.configs[hubs] for dups




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

    def validate_line(self, line) -> List:
        to_test = line.split(':')
        if to_test.len() != 2:
            raise FormatError(line)
        return to_test

    def is_int(val: int) -> bool:
        if isinstance(val, (int)) and not isinstance(val, bool):
            return (int(val))