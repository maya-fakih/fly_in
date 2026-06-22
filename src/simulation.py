"""Simulation module that wires together the map parser and simulation."""

from parsing.parser import GraphParser


class Simulation:
    """Run a simulation based on a map configuration file."""

    def __init__(self, map_config: str) -> None:
        """Initialize the simulation with a map configuration path."""
        self.config_map = map_config
        self.parser = GraphParser(self.config_map)
        self.ok = False
        
    def start(self):
        self.parser.load()
        if self.parser.parsing_safe:
            print('Parsing successful.')
            self.ok = True
        else:
            print('Parsing failed.')

