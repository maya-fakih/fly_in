"""Simulation module that wires together the map parser and simulation."""

from typing import Any
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
        self.map: dict[str, Hub] = {}
        self.file = "log.txt"
        self.drones = []
        
        self.start()
        self.setup()

    def setup(self) -> None:
        """Initialize drones and place them at the start hub."""
        from drone import Drone
        if not self.map:
            return
            
        start = next(h for h in self.map.values() if h.hub_type == 'start_hub')
        goal = next(h for h in self.map.values() if h.hub_type == 'end_hub')
        
        self.drones = [Drone(goal) for _ in range(self.nb_drones)]
        for drone in self.drones:
            self.move(drone, start)

    def step(self) -> list[str]:
        """Advances the simulation by exactly one turn.
        
        Returns:
            A list of logs representing drone movements this turn (e.g., ['D0-junction']).
        """
        moves = []
        for i in range(len(self.drones)):
            log = self.drones[i].tick(self)
            if log:
                moves.append(f"D{i}-{log}")
        return moves

    @property
    def is_finished(self) -> bool:
        """Check if all drones have reached their goals."""
        return all(d.reached_goal for d in self.drones)

    def run(self) -> None:
        """Headless runner loop that writes to log.txt until finished."""
        with open(self.file, "w") as file:
            pass
        while not self.is_finished:
            moves = self.step()
            with open(self.file, "a") as file:
                line = " ".join(moves)
                file.write(f"{line}\n")
        print('all drones reached end successfully')

    def move(self, drone: Any, next_hub: Hub) -> None:
        # (Your original move code continues here...)
        if drone.current_hub:
            drone.current_hub.current_drones -= 1
        drone.current_hub = next_hub
        next_hub.current_drones += 1