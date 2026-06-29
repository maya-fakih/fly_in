import arcade

class FlyinWindow(arcade.Window):
    def __init__(self):
        self.x = 800
        self.y = 600
        super.__init__(800, 600, "Fly In")
    
    def on_draw(self):
        self.clear()
        # redraw
    
    def on_update(self, delta_time):
        # called on every drame to update simulation state here
        pass

    def map_to_screen(self, x, y):
        margin = 100
        scale = 60
        return (margin + x*scale, margin + y*scale)