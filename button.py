from Managers.map_manager import Tile
from components import Hitbox, Vector


class Button(Tile):

    def __init__(self, type, hitbox, event):
        super().__init__(hitbox, type)
        self.hitbox = Hitbox(self.x, self.y, self.width, self.height)
        self.event = event
        self.activated = False

    def on_activate(self):
        self.activated = True
        # self.hitbox = Hitbox(self.x, self.y + self.height / 2, self.width, self.height / 2)
        self.hitbox.y = self.y + self.height / 2
        self.hitbox.height = self.height / 2
        from game import Game
        Game.get_instance().sound_manager.play_sound("button", "0")

    def on_deactivate(self):
        self.activated = False
        self.hitbox.y = self.y
        self.hitbox.height = self.height
        from game import Game
        Game.get_instance().sound_manager.play_sound("button", "1")

    def draw(self):
        from game import Game, offset_size
        # print(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height)
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture(
                "buttons", int(self.activated)
            ),
            Hitbox(self.x, self.y - offset_size, self.width, self.height),
            Hitbox(10, 25, 60, 15)
        )
        # Game.get_instance().draw_rect("red", self.hitbox)


from event import GameEvent


class ButtonEvent(GameEvent):
    def __init__(self, id, type, hitbox, affect):
        super().__init__(id, type, hitbox, affect)
        self.block = Button(101, hitbox, self)
    def update(self):
        from game import Game
        is_activate = False
        for entity in Game.get_instance().view.entities:
            if self.colliderect(entity.hitbox + Vector(0, 1)):
                self.activate()
                is_activate = True
                break
        if not is_activate:
            self.deactivate()
        return True
    def draw(self):
        self.block.draw()
    def on_activate(self):
        self.block.on_activate()

    def on_deactivate(self):
        self.block.on_deactivate()
