from entity import Entity
from components import Vector, Hitbox
from Managers.map_manager import basic_size, half_size


class Cube(Entity):
    # TODO:
    cube_size = 0.8 * basic_size

    def __init__(self, x, y, size=Vector(cube_size, cube_size)):
        super(x, y, size)
        self.canPick = False
        self.isPicked = False

    def hitRange(self):
        # TODO:
        return Hitbox(
            self.hitbox.x - half_size,
            self.hitbox.y - half_size,
            self.hitbox.width + half_size,
            self.hitbox.height + half_size,
        )

    def update(self, deltaTime):
        # TODO:
        from game import Game
        player = Game.get_instance().player
        if player.hitbox.hit(self.hitRange(self)):
            self.canPick = True
        else:
            self.canPick = False

        if self.canPick:

            pass

        if self.isPicked:
            self.hitbox.x = player.hitbox.x
            self.hitbox.y = player.hitbox.y
            offset = Vector(
                -0.5 * self.cube_size + (player.facing + 1) * (Player.PlayerSize.X) / 2,
                0.2 * Player.PlayerSize.y,
            )
            # TODO:
            # this.hitbox.position.addEqual(offset)
            self.velocity.x = player.velocity.x
            self.velocity.y = player.velocity.y
            self.jumping.jumpVelocity = player.jumping.jumpVelocity

        else:
            deltaTime = 60 * deltaTime / 1000
            # TODO:
            # self.updateXY 暂定

        # this.hitbox.position = this.hitbox.position.round();
        self.checkOutOfMap()

    def draw(self):
        pass
