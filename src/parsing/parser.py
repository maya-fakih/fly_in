"""Graph configuration parser and validation logic."""

from typing import Any, Dict, List, Sequence

from . import parsing_errors as errors

import arcade
from PIL.ImageColor import getrgb


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
            print(exc)

    def validate_connection(self, line: str) -> None:
        """Validate a connection line and add it to both hubs."""
        _, value = self.validate_line(line)
        connection_parts = value.strip().split(' ', 1)
        if len(connection_parts) not in (1, 2):
            raise errors.FormatError(line)
        if connection_parts[0].count('-') != 1:
            raise errors.FormatError(line)
        hub1, hub2 = connection_parts[0].strip().split('-')
        # we should check that the hubs exist
        poss = self.configs['hubs']
        if hub1 not in poss or hub2 not in poss:
            raise errors.ConnectionTypeError(line)
        # we should check that the connection doesn't already exist
        for conn in self.configs['hubs'][hub1]['connection']:
            if conn['target'] == hub2:
                raise errors.DuplicateError(
                    f'Connection between {hub1} and {hub2} already exists.'
                )
        if len(connection_parts) == 2:
            metadata = self.extract_bracket_content(connection_parts[1].strip(), line)
            if '=' not in metadata or metadata.count('=') != 1:
                raise errors.MetaDataTypeError(line)
            key, value = metadata.split('=', 1)
            if key != 'max_link_capacity':
                raise errors.MetaDataTypeError(line)
            if not value.isdigit() or int(value) <= 0:
                raise errors.MetaDataTypeError(line)
            metadata_dict = {'max_link_capacity': int(value)}
        else:
            metadata_dict = {'max_link_capacity': None}

        self.configs['hubs'][hub1]['connection'].append({
            'target': hub2,
            'max_link_capacity': metadata_dict['max_link_capacity'],
        })
        self.configs['hubs'][hub2]['connection'].append({
            'target': hub1,
            'max_link_capacity': metadata_dict['max_link_capacity'],
        })

    def validate_hub(self, line: str) -> None:
        """Validate a hub line and store it in configs."""
        parts = self.validate_line(line)
        hub_type = parts[0].strip()
        self.test_zone(hub_type, line)
        data = parts[1].strip(' ').split(' ', 3)
        if not len(data) in (3, 4):
            raise errors.HubFormat(line)
        name = data[0].strip()
        self.test_name(name)

        x = data[1].strip()
        y = data[2].strip()
        self.test_coords(x, y, line)
        if len(data) == 4:
            metadata = data[3].strip()
            md = self.test_metadata(metadata, line)
        else:
            md = {}

        self.configs['hubs'][name] = {
            'type': hub_type,
            'x': x,
            'y': y,
            'meta_data': md,
            'connection': []
        }

    def test_metadata(self, metadata: str, line: str) -> dict:
        """Checks that metadata is valid."""
        metadata = self.extract_bracket_content(metadata.strip(), line)
        metadata_parts = metadata.split()
        if len(metadata_parts) > 3:
            raise errors.MetaDataTypeError(line)
        for part in metadata_parts:
            if '=' not in part or part.count('=') != 1:
                raise errors.MetaDataTypeError(line)
        color = None
        max_drones = None
        zone = None
        seen = set()
        for part in metadata_parts:
            key, value = part.split('=', 1)
            if key in seen:
                raise errors.MetaDataTypeError(line)
            seen.add(key)
            if key == 'color':
                if not isinstance(value, str) or not value:
                    raise errors.MetaDataTypeError(line)
                color = self.validate_color(value, line)
            elif key == 'max_drones':
                if not value.isdigit() or int(value) <= 0:
                    raise errors.MetaDataTypeError(line)
                max_drones = value
            elif key == 'zone':
                valid_zone_types = ('normal', 'blocked', 'restricted', 'priority')
                if value not in valid_zone_types:
                    raise errors.MetaDataTypeError(line)
                zone = value
            else:
                raise errors.MetaDataTypeError(line)
        return {'color': color, 'max_drones': max_drones, 'zone': zone}

    def validate_color(self, color: str, line: str) -> None:
        """Checks that color is a valid string and exists in arcade library."""
        if not isinstance(color, str) or not color:
            raise errors.MetaDataTypeError(line)
        raw = color.strip()
        if color == 'rainbow':
            return ('rainbow')
        try:
            rgb = getrgb(raw)
            return rgb
        except Exception:
            color_format = raw.replace(' ', '_').replace('-', '_').upper()
            if hasattr(arcade.color, color_format):
                return getattr(arcade.color, color_format)
            raise errors.ColorFormat(line)

    def extract_bracket_content(self, value: str, line: str) -> str:
        """Return the inner content when exactly one pair of brackets is present."""
        if not value.startswith('[') or not value.endswith(']'):
            raise errors.MetaDataTypeError(line)
        if value.count('[') != 1 or value.count(']') != 1:
            raise errors.MetaDataTypeError(line)
        return value[1:-1].strip()

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
        if line.endswith('\n'):
            line = line[:-1]
        if line.count(':') != 1:
            raise errors.FormatError(line)
        to_test = line.split(':')
        if len(to_test) != 2:
            raise errors.FormatError(line)
        valid_keys = ['start_hub', 'end_hub', 'hub', 'connection']
        if to_test[0].strip() not in valid_keys:
            raise errors.FormatError(line)
        return to_test
