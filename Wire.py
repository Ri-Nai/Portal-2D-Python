from Event import GameEvent

class Wire(GameEvent):
    def __init__(self, id, type, x, y, width, height, affect):
        super().__init__(id, type, x, y, width, height, affect)

    def update(self):
        pass

    def onActivate(self):
        pass

    def onDeactivate(self):
        pass

    def draw(self):
        pass