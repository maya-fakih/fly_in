import arcade


class FlyinWindow(arcade.Window):
    def __init__(self) -> None:
        self.x = 800
        self.y = 600
        super().__init__(800, 600, "Fly In")

    def on_draw(self) -> None:
        self.clear()
        # redraw

    def on_update(self, delta_time):
        self.time_accumulator += delta_time
        if self.time_accumulator >= self.turn_duration:
            self.time_accumulator = 0.0
            if not self.sim.is_finished:
                turn_moves = self.sim.step() 
                self.update_drone_animations(turn_moves)

    def map_to_screen(self, x: float, y: float) -> tuple[float, float]:
        margin = 100
        scale = 60
        return (margin + x*scale, margin + y*scale)
