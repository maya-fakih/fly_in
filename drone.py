from __future__ import annotations
from typing import TYPE_CHECKING

from hub import Hub

if TYPE_CHECKING:
    from simulation import Simulation


class Drone():
    """Represents a drone agent navigating the map."""

    def __init__(self, goal: Hub):
        self.current_hub = None
        self.goal = goal
        self.in_transit_to = None

    @property
    def reached_goal(self) -> bool:
        return self.current_hub == self.goal
    
    def tick(self, sim: Simulation):
        if self.reached_goal:
            return
        if self.in_transit_to:
            sim.arrive(self)
            return
        next_hub = self.next_move(sim)
        if not next_hub:
            return
        if next_hub.zone.value == 2:
            sim.leave(self, next_hub)
        else:
            sim.move(self, next_hub)
    
    def next_move(self, sim: Simulation):
        valid = {n for n in sim.get_neighbors(self.current_hub)
                 if n.cost < self.current_hub.cost}
        if not valid:
            return None
        return min(valid, key=lambda n: n.estimate)