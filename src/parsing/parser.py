"""Graph configuration parser and validation logic."""

from typing import Dict, List, Sequence

from . import parsing_errors as errors


class GraphParser:
    """Parse graph configuration files and validate their contents."""

    def __init__(self, config: str) -> None:
        """Initialize the parser with the path to the configuration file.

        Args:
            config: Path to the configuration file.
        """
        self.config_file = config
        self.configs: Dict[str, object] = {}
        self.parsing_safe = False
        self.hub_state = 1

    def load_file(self) -> None:
        """Load and parse the configuration file line by line."""
        state = 1
        try:
            with open(self.config_file, 'r') as config_file:
                for line in config_file:
                    if line.startswith('#'):
                        continue
                    if state == 1:
                        self.configs['nb_drones'] = self.check_first_line(line)
                        self.configs['hubs'] = {}
                        state = 2
                    elif state == 2:
                        # Placeholder for hub parsing
                        continue
                    elif state == 3:
                        continue
            self.parsing_safe = True
        except Exception as exc:  # pragma: no cover
            print('[Parsing]: Error!')
            print(exc)

    def validate_hub(self, line: str) -> Dict[str, object]:
        """Validate a hub definition line and return parsed parts.

        Raises errors.HubFormat if the line is not a valid hub definition.
        """
        parts = self.validate_line(line)
        possible_hubs: Sequence[str] = (
            'start_hub',
            'hub',
            'end_hub',
        )
        key = parts[0].strip()
        if key not in possible_hubs:
            raise errors.HubFormat(line)
        return {}

    def check_first_line(self, line: str) -> int:
        """Validate the format of the first config line and return int."""
        self.validate_line(line)
        to_test = line.split(':')
        if to_test[0].strip() != 'nb_drones':
            raise errors.DroneNumberError()
        val_str = to_test[1].strip()
        try:
            val = int(val_str)
        except ValueError:
            raise errors.DroneNumberError()
        return val

    def validate_line(self, line: str) -> List[str]:
        """Split a line into key and value and validate the format."""
        to_test = line.split(':')
        if len(to_test) != 2:
            raise errors.FormatError(line)
        return to_test

    @staticmethod
    def is_int(val: object) -> bool:
        """Return True if `val` is an int but not a bool."""
        return isinstance(val, int) and not isinstance(val, bool)
