from entity import Entity
from components import Vector, Hitbox
from Managers.map_manager import basicSize, halfSize


class Cube(Entity):
    # TODO:
    cubeSize = 0.8 * basicSize

    def __init__(self, x, y, size=Vector(cubeSize, cubeSize)):
        super(x, y, size)
        self.canPick = False
        self.isPicked = False

    def hitRange(self):
        # TODO:
        return Hitbox(
            self.hitbox.x - halfSize,
            self.hitbox.y - halfSize,
            self.hitbox.width + halfSize,
            self.hitbox.height + halfSize,
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
                -0.5 * self.cubeSize + (player.facing + 1) * (Player.PlayerSize.X) / 2,
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
