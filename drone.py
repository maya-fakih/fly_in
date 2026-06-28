from hub import Hub

class Drone():
    def __init__(self, goal: Hub):
        self.current_hub = None
        self.waiting_turn = 1
        self.goal = goal

    @property
    def can_move(self):
        return self.waiting_turn <= 0
    
    @property
    def reached_goal(self):
        return self.current_hub == self.goal
    
    from simulation import Simulation
    def tick(self, sim: Simulation):
        self.waiting_turn -= 1
        if not self.can_move:
            return
        next_hub = self.next_move(sim)
        if next_hub:
            sim.move(self, next_hub)
    
    def next_move(self, sim: Simulation):
        valid = {n for n in sim.get_neighbors(self.current_hub)
                 if n.cost < self.current_hub.cost}
        if not valid:
            return None
        return min(valid, key=lambda n: n.estimate)