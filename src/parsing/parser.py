"""Graph configuration parser and validation logic."""

from typing import Any, Dict, List, Sequence

from . import parsing_errors as errors


class GraphParser:
    """Parse graph configuration files and validate their contents."""

    def __init__(self, config: str) -> None:
        """Initialize the parser with the path to the configuration file.

        Args:
            config: Path to the configuration file.
        """
        self.config_file = config
        self.configs: Dict[str, Any] = {
            'nb_drones': None,
            'hubs': {},
        }
        self.parsing_safe = False
        self.hub_state = 1

    def load_file(self) -> None:
        """Load and parse the configuration file line by line."""
        hubs = ['start_hub', 'end_hub', 'hub']
        first_line = True
        try:
            with open(self.config_file, 'r') as config_file:
                for line in config_file:
                    if line.startswith('#') or line.isspace():
                        continue
                    if first_line:
                        self.configs['nb_drones'] = self.check_first_line(line)
                        first_line = False
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
        """Validate a connection line and add it to both hubs."""
        _, value = self.validate_line(line)
        value = value.strip()
        if '[' not in value or ']' not in value:
            raise errors.FormatError(line)

        dash_part = value[:value.index('[')].strip()
        meta_part = value[value.index('[') + 1:value.index(']')]

        if '-' not in dash_part:
            raise errors.FormatError(line)
        hub1, hub2 = dash_part.split('-')

        if hub1 not in self.configs['hubs'] or hub2 not in self.configs['hubs']:
            raise errors.ConnectionTypeError(line)

        if hub2 in self.configs['hubs'][hub1]['connection']:
            raise errors.DuplicateConnectionError(line)

        name, capacity = meta_part.split('=')
        if name != 'max_link_capacity' or not capacity.isdigit() or int(capacity) <= 0:
            raise errors.FormatError(line)

        self.configs['hubs'][hub1]['connection'].add(hub2)
        self.configs['hubs'][hub2]['connection'].add(hub1)

    def validate_hub(self, line: str) -> None:
        """Validate a hub line and store it in configs."""
        parts = self.validate_line(line)
        hub_type = parts[0].strip()
        self.test_zone(hub_type, line)

        for character in parts[1]:
            if character == ' ':
                name_ends = parts[1].index(character)
                break
        name = parts[1][:name_ends]
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

        self.configs['hubs'][name] = {
            'type': hub_type,
            'x': x,
            'y': y,
            'meta_data': md,
            'connection': set()
        }

    def test_metadata(self, metadata: List, line: str) -> dict:
        """Checks that metadata is valid."""
        if len(metadata) != 3:
            raise errors.MetaDataTypeError(line)
        for part in metadata:
            if '=' not in part:
                raise errors.MetaDataTypeError(line)

        seen = set()
        for part in metadata:
            key, value = part.split('=')
            if key in seen:
                raise errors.MetaDataTypeError(line)
            seen.add(key)
            if key == 'color':
                if not isinstance(value, str) or not value:
                    raise errors.MetaDataTypeError(line)
            elif key == 'max_drones':
                if not value.isdigit() or int(value) <= 0:
                    raise errors.MetaDataTypeError(line)
            elif key == 'zone':
                valid_zone_types = ('normal', 'blocked', 'restricted', 'priority')
                if value not in valid_zone_types:
                    raise errors.MetaDataTypeError(line)
            else:
                raise errors.MetaDataTypeError(line)
        return {part.split('=')[0]: part.split('=')[1] for part in metadata}

    def test_coords(self, x: str, y: str, line: str) -> None:
        """Checks that coords are valid integers and unique."""
        try:
            int(x)
            int(y)
        except ValueError:
            raise errors.CoordinatesTypeError(line)
        for hub in self.configs['hubs'].values():
            if hub['x'] == x and hub['y'] == y:
                raise errors.CoordinatesDuplicateError(line)

    def test_zone(self, zone: str, line: str) -> None:
        """Checks valid zone type and no duplicate start/end hubs."""
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

    def test_name(self, name1: str) -> None:
        """Test if a name is valid and unique."""
        # if not isinstance(name, str) or not name:
        #     raise errors.NameTypeError(name)
        name = name1.strip()
        if '-' in name or ' ' in name:
            raise errors.NameTypeError(name)
        if name in self.configs['hubs']:
            raise errors.NameDuplicateError(name)

    def check_first_line(self, line: str) -> int:
        """Validate the format of the first config line and return int."""
        to_test = line.split(':')
        if len(to_test) != 2:
            raise errors.FormatError(line)
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
        """Split a line into key and value and validate the format."""
        to_test = line.split(':')
        if len(to_test) != 2:
            raise errors.FormatError(line)
        valid_keys = ['start_hub', 'end_hub', 'hub', 'connection']
        if to_test[0].strip() not in valid_keys:
            raise errors.FormatError(line)
        return to_test

    @staticmethod
    def is_int(val: object) -> bool:
        """Return True if `val` is an int but not a bool."""
        return isinstance(val, int) and not isinstance(val, bool)