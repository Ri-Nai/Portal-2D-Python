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
        status = "wires-" + ("on" if self.activated else "off")
        texture = None
        if self.nxtdir == -1:
            texture = self.textureManager.get_texture(status, "sign")
        elif self.predir == self.nxtdir:
            texture = self.textureManager.get_texture(
                status, "straight-" + str(self.predir & 1)
            )
        else:
            texture = self.textureManager.get_texture(status, "cursed")
        from game import Game, offset_size

        Game.get_instance().draw_image(
            texture,
            (
                self.x - offset_size / 2,
                self.y - offset_size / 2,
                self.width,
                self.height,
            ),
        )
