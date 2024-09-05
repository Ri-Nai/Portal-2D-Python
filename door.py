from event import GameEvent
from Managers.map_manager import Tile
from components import Hitbox


class Door(Tile):
    def __init__(self, type, hitbox, event):
        super().__init__(hitbox, type)
        self.event = event
        self.hitbox = Hitbox(self.x, self.y, self.width, self.height)
    def draw(self):  # 暂定
        #TODO:
        pass

    def on_activate(self):
        self.hitbox = Hitbox(0, 0, 1, 1)

    def on_deactivate(self):
        self.hitbox = Hitbox(self.x, self.y, self.width, self.height)


class DoorEvent(GameEvent):
    def __init__(self, id, type, hitbox):
        super().__init__(id, type, hitbox, [])
        self.block = Door(101, hitbox, self)

    def update(self):
        pass

    def on_activate(self):
        self.block.on_activate()

    def on_deactivate(self):
        self.block.on_deactivate()
