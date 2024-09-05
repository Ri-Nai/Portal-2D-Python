from entity import Entity
from components import Vector, Hitbox
from Managers.map_manager import basic_size, half_size
from player import player_size

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
            self.hitbox.width + basic_size,
            self.hitbox.height + basic_size
        )

    def update(self, deltaTime):
        # TODO:
        from game import Game
        player = Game.get_instance().view.player
        if player.hitbox.colliderect(self.hitRange(self)):
            self.canPick = True
        else:
            self.canPick = False

        if self.canPick:
            self.hitbox.position.x = player.hitbox.position.x;
            self.hitbox.position.y = player.hitbox.position.y;
            
            offset = Vector(player.facing * Cube.cubeSize + (player.facing + 1) * (Player.PlayerSize.x - Cube.cubeSize) / 2, 0.32 * Player.PlayerSize.y);
            self.hitbox.position.addEqual(offset);
            self.velocity.x = player.velocity.x;
            self.velocity.y = player.velocity.y;
            self.jumping.jumpVelocity = player.jumping.jumpVelocity;

        if self.isPicked:
            self.hitbox.x = player.hitbox.x
            self.hitbox.y = player.hitbox.y
            offset = Vector(
                -0.5 * self.cube_size + (player.facing + 1) * (player_size.x) / 2,
                0.2 * player_size.y,
            )
            self.hitbox += offset
            self.velocity.x = player.velocity.x
            self.velocity.y = player.velocity.y
            self.jumping.jumpVelocity = player.jumping.jumpVelocity

        else:
            self.updateXY(0, 0)

        # this.hitbox.position = this.hitbox.position.round()
        self.checkOutOfMap()

    def draw(self):
        pass
