from Event import GameEvent
from map import Tile
from components import Hitbox

class Door(Tile):
    def __init__(self, type, x, y, width, height, event):
        super().__init__(x, y, width, height, type)
        self.event = event
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):#暂定
        pass

    def onActivate(self):
        self.hitbox = Hitbox(0,0,1,1)

    def onDeactivate(self):
        self.hitbox = Hitbox(self.x, self.y, self.width, self.height)

class DoorEvent(GameEvent):
    def __init__(self,id,type,x,y,width,height):
        super().__init__(id, type, x, y, width, height, None)
        self.block = Door(101, x, y, width, height, self)

    def update(self):
        pass

    def onActivate(self):
        self.block.onActivate(self)

    def onDeactivate(self):
        self.block.onDeactivate(self)