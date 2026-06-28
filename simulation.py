"""Simulation module that wires together the map parser and simulation."""

from typing import Dict
from math import inf
from parser import GraphParser
from hub import Hub

class Simulation:
    """Run a simulation based on a map configuration file."""

    def __init__(self, map_config: str) -> None:
        """Initialize the simulation with a map configuration path."""
        self.config_map = map_config
        self.parser = GraphParser(self.config_map)
        self.nb_drones = 0
        self.map = {}
        self.start()


    def run(self):
        from drone import Drone
        start = next(h for h in self.map.values() if h.hub_type == 'start_hub')
        goal = next(h for h in self.map.values() if h.hub_type == 'end_hub')
        self.drones = [Drone(goal) for _ in range(self.nb_drones)]
        for drone in self.drones:
            self.move(drone, start)

        while not all(d.reached_goal for d in self.drones):
            for drone in self.drones:
                drone.tick(self)

    def move(self, drone, next_hub: Hub):
        if drone.current_hub:
            drone.current_hub.current_drones -= 1
        next_hub.current_drones += 1
        drone.current_hub = next_hub    

    def leave(self, drone, next_hub):
        if drone.current_hub:
            drone.current_hub.current_drones -= 1
        c = drone.current_hub
        c.connections[next_hub.name]['current_link_drones'] += 1
        next_hub.connections[c.name]['current_link_drones'] += 1
        drone.in_transit_to = next_hub

    def arrive(self, drone):
        drone.current_hub.connections[drone.in_transit_to.name]['current_link_drones'] -= 1
        drone.in_transit_to.connections[drone.current_hub.name]['current_link_drones'] -= 1
        drone.in_transit_to.current_drones += 1
        drone.current_hub = drone.in_transit_to
        drone.in_transit_to = None

    def update_edge(self, from_hub, to_hub):
        from_hub.connections[to_hub.name]['current_link_drones'] += 1
        to_hub.connections[from_hub.name]['current_link_drones'] += 1

    def start(self):
        self.parser.load_file()
        if self.parser.parsing_safe:
            print('Parsing successful.')
            self.create_map()
            self.set_costs()
            self.set_heuristics()
            self.print_map()
        else:
            print('Parsing failed.')

    def get_neighbors(self, hub: Hub):
        return {
            self.map[target]
            for target in hub.connections
            if self.map[target].zone.value != inf
        }

    def set_costs(self):
        end_hub = next((hub for hub in self.map.values() if hub.hub_type == 'end_hub'), None)
        start_hub = next((hub for hub in self.map.values() if hub.hub_type == 'start_hub'), None)
        end_hub.cost = 0
        visited = {end_hub}
        current_level = list(self.get_neighbors(end_hub))
        cost = 1

        while current_level:
            for hub in current_level:
                if hub not in visited:
                    if hub.zone.value != inf:
                        hub.cost = cost + hub.zone.value -1
                    visited.add(hub)
                    if hub == start_hub:
                        return

            next_level = set()
            for hub in current_level:
                next_level.update(self.get_neighbors(hub) - visited)
            
            current_level = list(next_level)
            cost += 1

    def set_heuristics(self):
        from math import sqrt
        end_hub = next((hub for hub in self.map.values() if hub.hub_type == 'end_hub'), None)
        if not end_hub:
            return
        for hub in self.map.values():
            if hub.cost == inf:
                hub.heuristic = inf
            else:
                dx = hub.x - end_hub.x
                dy = hub.y - end_hub.y
                hub.heuristic = int(sqrt(dx * dx + dy * dy))

    def print_map(self):
        for hub in self.map.values():
            hub.show_hub()
        
    def create_map(self):
        configs = self.parser.configs
        self.nb_drones = configs['nb_drones']
        for name, data in configs['hubs'].items():
            self.map[name] = Hub(name, data)