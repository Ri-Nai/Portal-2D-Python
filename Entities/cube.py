from Entities.entity import Entity
from components import Vector, Hitbox
from Managers.map_manager import basic_size, half_size
from Entities.player import player_size


class Cube(Entity):
    cube_size = 0.8 * basic_size

    def __init__(self, x, y):
        # super(x, y, size)
        super().__init__(Hitbox(x, y, Cube.cube_size, Cube.cube_size))
        self.canPick = False
        self.isPicked = False

    def hitRange(self):
        return Hitbox(
            self.hitbox.x - half_size,
            self.hitbox.y - half_size,
            self.hitbox.width + basic_size,
            self.hitbox.height + basic_size,
        )
    def unPicked(self):
        self.isPicked = not self.isPicked
    def update(self):
        from game import Game

        player = Game.get_instance().view.player
        if player.hitbox.colliderect(self.hitRange()):
            self.canPick = True
        else:
            self.canPick = False
        if self.canPick:
            Game.get_instance().keyboard_manager.first_down("E", self.unPicked)
        if self.isPicked:
            self.hitbox.x = player.hitbox.x
            self.hitbox.y = player.hitbox.y
            offset = Vector(
                player.facing  * Cube.cube_size + (player.facing + 1) * (player_size.x - Cube.cube_size) / 2,
                0.32 * player_size.y
            )
            self.hitbox += offset
            self.velocity.x = player.velocity.x
            self.velocity.y = player.velocity.y
            self.jumping.jumpVelocity = player.jumping.jumpVelocity

        else:
            self.updateXY(0, 0)

        # this.hitbox.position = this.hitbox.position.round()
        self.check_out_of_map()

    def draw(self):
        from game import Game

        # Game.get_instance().draw_rect((255, 0, 0), self.hitbox)
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture("cubes", int(not self.isPicked and self.canPick)),
            self.hitbox,
        )
