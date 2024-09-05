from GameEvents.event import GameEvent
from Managers.map_manager import Tile
from components import Hitbox


class Door(Tile):
    def __init__(self, type, hitbox, event):
        super().__init__(hitbox, type)
        self.event = event
        self.hitbox = Hitbox(self.x, self.y, self.width, self.height)
        self.frame = 1
        self.buffer = 5
        self.activated = False

    def draw(self):  # 暂定
        from game import Game

        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture("doors", self.frame), self
        )
        """
        window.$game.ctx.drawImage(
            window.$game.textureManager.getTexture("doors", this.frame),
            this.position.x,
            this.position.y,
            this.size.x,
            this.size.y);
        """

    def on_activate(self):
        # self.hitbox = Hitbox(0, 0, 1, 1)
        self.activated = True
        self.hitbox.x = 0
        self.hitbox.y = 0
        self.hitbox.width = 1
        self.hitbox.height = 1

    def on_deactivate(self):
        # self.hitbox = Hitbox(self.x, self.y, self.width, self.height)
        self.activated = False
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        self.hitbox.width = self.width
        self.hitbox.height = self.height

    def update(self):
        self.buffer -= 1
        if self.buffer <= 0:
            if self.activated:
                self.frame = min(7, self.frame + 1)
            else:
                self.frame = max(1, self.frame - 1)
            self.buffer = 5


class DoorEvent(GameEvent):
    def __init__(self, id, type, hitbox):
        super().__init__(id, type, hitbox, [])
        self.block = Door(101, hitbox, self)

    def update(self):
        self.block.update()
        return True
    def draw(self):
        self.block.draw()
    def on_activate(self):
        self.block.on_activate()

    def on_deactivate(self):
        self.block.on_deactivate()
