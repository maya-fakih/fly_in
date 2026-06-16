from parsing.parser import GraphParser


class Simulation():
    def __init__(self, map_config: str):
        self.config_map = map_config
        self.Parser = GraphParser(self.config_map)
