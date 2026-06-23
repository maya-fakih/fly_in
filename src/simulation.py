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
        """Uses reverse Djxstra algorithm to set costs for all hubs in map."""
        end_hub = next((hub for hub in self.map if hub.hub_type == 'end_hub'), None)
        next_level = list(self.get_neighbors(end_hub))
        cost = 1
        for i in range(len(next_level)):
            hub = next_level[i]
            hub.cost = cost
            if i == len(next_level) -1:
                n = []
                while next_level:
                    current = next_level.pop()
                    n.append(self.get_neighbors(current))
                cost +=1
                next_level.append(n)

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
