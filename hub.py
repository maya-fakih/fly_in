"""Hub file for hub representation."""
from math import inf

from zone_types import Zones


class Hub:
    """Dataclass to represent a hub."""
    def __init__(self, name: str, data):
        self.name = name
        self.x = int(data['x'])
        self.y = int(data['y'])
        zone = data['meta_data']['zone']
        self.zone: Zones = zone if isinstance(zone, Zones) else Zones[zone]
        self.color = data['meta_data']['color']
        self.max_drones = data['meta_data']['max_drones']
        self.current_drones = 0
        self.cost = inf
        self.heuristic = 0
        self.hub_type = data['type']
        # connections to other hubs (names or identifiers)
        # 'connection': [{'target': 'waypoint1', 'max_link_capacity': 2},
        #                {'target': 'goal', 'max_link_capacity': 2}]}
        self.connections = {
            conn['target']: {
                'max_link_capacity': conn['max_link_capacity'],
                'current_link_drones': 0
            }
            for conn in data['connection']
        }

    @property
    def traffic(self):
        if self.max_drones == inf:
            return 0
        return self.current_drones / self.max_drones

    @property
    def capacity(self):
        return self.max_drones - self.current_drones

    @property
    def estimate(self):
        return self.cost + self.heuristic + self.traffic

    def link_available(self, neighbor: 'Hub') -> bool:
        conn = self.connections[neighbor.name]
        return conn['current_link_drones'] < conn['max_link_capacity']

    def show_hub(self):
        status = f'[{self.current_drones}/{self.max_drones}]'
        transit = ''
        in_transit = [
            target for target, conn in self.connections.items()
            if conn['current_link_drones'] > 0
        ]
        if in_transit:
            transit = f' → in transit: {", ".join(in_transit)}'
        h = self.heuristic
        print(f'{self.name} {status} cost={self.cost} h={h}{transit}')
