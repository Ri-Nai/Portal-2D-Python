from event import GameEvent


class Wire(GameEvent):
    def __init__(self, id, type, hitbox, affect, predir, nxtdir):
        super().__init__(id, type, hitbox, affect)
        self.predir = predir
        self.nxtdir = nxtdir
    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def draw(self):
        status = "wires-" + ("on" if self.activated else "off")
        texture = None
        from game import Game
        if self.nxtdir == -1:
            texture = Game.get_instance().texture_manager.get_texture(status, "sign")
        elif self.predir == self.nxtdir:
            texture = Game.get_instance().texture_manager.get_texture(
                status, "straight-" + str(self.predir & 1)
            )
        else:
            texture = Game.get_instance().texture_manager.get_texture(status, "cursed")
        from game import Game, offset_size
        from components import Hitbox
        Game.get_instance().draw_image(
            texture,
            Hitbox(
                self.x - offset_size / 2,
                self.y - offset_size / 2,
                self.width,
                self.height,
            ),
        )
