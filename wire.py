from event import GameEvent

class Wire(GameEvent):
    def __init__(self, id, type, x, y, width, height, affect):
        super().__init__(id, type, x, y, width, height, affect)

    def update(self):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def draw(self):
        pass
