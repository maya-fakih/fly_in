"""Hub file for hub representation."""
from math import inf

from hub_type import HubType

from zone_types import Zones


class Hub:
    """Dataclass to represent a hub."""
    def __init__(self, name: str, data):
        self.name = name
        self.x = data['x']
        self.y = data['y']
        self.zone: Zones = data['meta_data']['zone']
        self.color = data['meta_data']['color']
        self.max_drones = data['meta_data']['max_drones']
        self.current_drones = 0
        self.capacity = self.max_drones - self.current_drones
        self.cost = inf
        self.huristic = 0
        self.hub_type = data['type']
        # connections to other hubs (names or identifiers)
        # 'connection': [{'target': 'waypoint1', 'max_link_capacity': 2},
        #                {'target': 'goal', 'max_link_capacity': 2}]}
        self.connections = data['connection']

    def show_hub(self):
        print(f'{self.name}:')
        print(f'x={self.x}, y={self.y}, color={self.color},'
                f'zone={self.zone}, max_drones={self.max_drones},'
                f'current_drones={self.current_drones},'
                f'capacity={self.capacity}, cost_end={self.cost}'
                f'huristic={self.huristic}, hub_type={self.hub_type}'
                f'connections={self.connections}')

    def estimate(self, connction):
        cost = self.zone

