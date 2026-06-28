from hub import Hub

class Drone():
    def __init__(self, goal: Hub):
        self.current_hub = None
        self.goal = goal
        self.in_transit_to = None

    @property
    def reached_goal(self):
        return self.current_hub == self.goal
    
    from simulation import Simulation
    def tick(self, sim: Simulation):
        if self.in_transit_to:
            sim.move(self, self.in_transit_to)
            self.in_transit_to = None
            return
        next_hub = self.next_move(sim)
        if not next_hub:
            return
        if next_hub.zone.value == 2:
            self.in_transit_to = next_hub
            sim.leave(self)
        else:
            sim.move(self, next_hub)
    
    def next_move(self, sim: Simulation):
        valid = {n for n in sim.get_neighbors(self.current_hub)
                 if n.cost < self.current_hub.cost}
        if not valid:
            return None
        return min(valid, key=lambda n: n.estimate)