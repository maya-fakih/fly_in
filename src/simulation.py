"""Simulation module that wires together the map parser and simulation."""

from typing import Dict
from parsing.parser import GraphParser
from hub import Hub

class Simulation:
    """Run a simulation based on a map configuration file."""

    def __init__(self, map_config: str) -> None:
        """Initialize the simulation with a map configuration path."""
        self.config_map = map_config
        self.parser = GraphParser(self.config_map)
        self.nb_drones = 0
        self.map = []
        self.ok = False

    def start(self):
        self.parser.load_file()
        if self.parser.parsing_safe:
            print('Parsing successful.')
            self.create_map()
            self.set_costs()
            self.print_map()
        else:
            print('Parsing failed.')

    def get_neighbors(self, hub: Hub):
        connections = hub.connections
        targets = {hub['target'] for hub in connections}
        neighbors = {hub for hub in self.map if hub.name in targets}
        return neighbors

    def set_costs(self):
        """Uses reverse BFS algorithm to set costs for all hubs in map."""
        end_hub = next((hub for hub in self.map if hub.hub_type == 'end_hub'), None)
        if not end_hub:
            return
        # this will never happen but for safety and proper alg ^
        end_hub.cost = 0
        visited = {end_hub}
        current_level = list(self.get_neighbors(end_hub))
        cost = 1

        while current_level:
            for hub in current_level:
                if hub not in visited:
                    hub.cost = cost * hub.zone.value
                    visited.add(hub)

            next_level = set()
            for hub in current_level:
                neighbors = self.get_neighbors(hub)
                next_level.update(neighbors - visited)
            
            current_level = list(next_level)
            cost += 1

    def create_map(self):
        configs = self.parser.configs
        self.nb_drones = configs['nb_drones']
        print(self.nb_drones)
        hubs = configs['hubs']
        for name, data in hubs.items():
            self.map.append(Hub(name, data))
        
    def print_map(self):
        for hub in self.map:
            hub.show_hub()
