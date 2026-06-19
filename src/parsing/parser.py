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
        self.configs: Dict = {
            'nb_drones': 0,
            'hubs': {},
            'connections': {}
        }
        self.parsing_safe = False
        self.hub_state = 1

    def load_file(self) -> None:
        """Load and parse the configuration file line by line."""
        hubs = ['start_hub', 'end_hub', 'hub']
        first = True
        try:
            with open(self.config_file, 'r') as config_file:
                for line in config_file:
                    if line.startswith('#'):
                        continue
                    if line.isspace():
                        continue
                    if first:
                        self.configs['nb_drones'] = self.check_first_line(line)
                        first = False
                        continue
                    key, _ = self.validate_line(line)
                    if key in hubs:
                        self.validate_hub(line)
                    elif key == 'connection':
                        self.validate_connection(line)
            self.parsing_safe = True
        except Exception as exc:
            print('[Parsing]: Error!')
            print(exc)

    def validate_connection(self, line: str) -> None:
        """Perfect doc string."""
        key, value = self.validate_line(line)
        test = value.strip().split(' ')
        if len(test) != 2:
            raise errors.FormatError(line)
        hub1, hub2 = test[0].split('-')
        metadata = test[1].strip(']', '[')
        test2 = metadata.split('=')
        if test2.len() != 2:
            raise errors.FormatError(line)
        if hub1 not in self.configs['hubs'] or hub2 not in self.configs['hubs']:
            raise errors.ConnectionTypeError(line)
        if test2 != 'max_link_capacity':
            raise errors.FormatError(line)
        

    def validate_hub(self, line: str):
        """Perfect doc string."""
        parts = self.validate_line(line)
        # sequence allows for read only so that mypy doesnt scream
        hub_type = parts[0].strip()
        self.test_zone(hub_type, line)
        for character in parts[1]:
            if character == ' ':
                name_ends = parts[1].index(character)
        name = parts[1][: name_ends]
        self.test_name(name)

        rest = parts[1][name_ends + 1:]
        if '[' not in rest or ']' not in rest:
            raise errors.MetaDataTypeError(line)
        start = rest.index('[')
        close = rest.index(']')
        if start > close:
            raise errors.MetaDataTypeError(line)
        coords, metadata = rest[:start], rest[start + 1:close]

        x, y = coords.split()
        self.test_coords(x, y, line)

        metadata_parts = metadata.split()
        md = self.test_metadata(metadata_parts, line)
        # return dict of {hub_type, name, x, ,y, metadata_dict}
        # idk how figure out how to return it tmrw w parsing is done :)
        self.configs['hubs'][name] = {
            'type': hub_type,
            'x': x, 'y': y,
            'meta_data': md,
            'connection': {None}}

    def test_metadata(self, metadata: List, line: str) -> dict:
        """Checks that metadata is valid."""
        if len(metadata) != 3:
            raise errors.MetaDataTypeError(line)
        for part in metadata:
            if '=' not in part:
                raise errors.MetaDataTypeError(line)
        # check if metadata is valid (color, max_drones, zone)
        # make sure it apears only once
        # validate values
        seen = set()
        for part in metadata:
            key, value = part.split('=')
            if key in seen:
                raise errors.MetaDataTypeError(line)
            seen.add(key)
            if key == 'color':
                if not isinstance(value, str):
                    raise errors.MetaDataTypeError(line)
            elif key == 'max_drones':
                if not self.is_int(value):
                    raise errors.MetaDataTypeError(line)
            elif key == 'zone':
                self.test_zone(value, line)
            else:
                raise errors.MetaDataTypeError(line)
        return {part.split('=')[0]: part.split('=')[1] for part in metadata}

    def test_coords(self, x: str, y: str, line: str) -> None:
        """Checks that coords are unique and valid."""
        try:
            int(x)
            int(y)
        except ValueError:
            raise errors.CoordinatesTypeError(line)
        for hub in self.configs['hubs'].values():
            if hub['x'] == x and hub['y'] == y:
                raise errors.CoordinatesDuplicateError(line)

    def test_zone(self, zone: str, line: str) -> None:
        """Checks valid zone type."""
        possible_hubs: Sequence[str] = ('start_hub', 'hub', 'end_hub',)
        if zone not in possible_hubs:
            raise errors.HubFormat(line)
        if zone != 'hub':
            existing_types = [
                hub['type'] for hub in self.configs['hubs'].values()
                if isinstance(hub, dict) and 'type' in hub
            ]
            if zone in existing_types:
                raise errors.DuplicateZone(line)

    def test_name(self, name: str) -> None:
        """Test if a name is valid."""
        if not isinstance(name, str) or not name:
            raise errors.NameTypeError(NameError)
        # i dont know if this really checks all names or not :(
        # we will check if it fails we come back here lol
        if name in self.configs['hubs']:
            raise errors.NameDuplicateError(name)
        if '-' in name or ' ' in name:
            raise errors.NameTypeError(name)

    def check_first_line(self, line: str) -> int:
        """Validate the format of the first config line and return int."""
        self.validate_line(line)
        to_test = line.split(':')
        if to_test[0].strip() != 'nb_drones':
            raise errors.DroneNumberError(line)
        val_str = to_test[1].strip()
        try:
            val = int(val_str)
            if val <= 0:
                raise errors.DroneNumberError(line)
        except ValueError:
            raise errors.DroneNumberError(line)
        return val

    def validate_line(self, line: str) -> List[str]:
        """Split a line into zone and value and validate the format."""
        to_test = line.split(':')
        if len(to_test) != 2:
            raise errors.FormatError(line)
        valid_keys = ['start_hub', 'end_hub', 'hub', 'connection']
        if to_test[0] not in valid_keys:
            raise errors.FormatError(line)
        return to_test

    @staticmethod
    def is_int(val: object) -> bool:
        """Return True if `val` is an int but not a bool."""
        return isinstance(val, int) and not isinstance(val, bool)
