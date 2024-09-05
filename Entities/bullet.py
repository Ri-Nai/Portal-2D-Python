from Entities.entity import Entity
from game import basic_size
from components import *

bullet_size = basic_size * 0.2


class Bullet(Entity):

    def __init__(self, position: Vector, velocity: Vector, style=0):
        # super(position.subVector(Bullet.bullet_size.scale(0.5)), Bullet.bullet_size, velocity)
        super().__init__(Hitbox(position.x, position.y, bullet_size, bullet_size))
        self.destroyed = False
        self.is_bullet = True
        self.type = -1
        self.style = style
        self.velocity = velocity

    def update(self):
        if self.destroyed:
            return
        from game import Game
        # print(self.velocity.magnitude())
        player = Game.get_instance().view.player
        GLaDOS = Game.get_instance().view.GLaDOS
        direction = self.velocity.normalize()
        length = self.velocity.magnitude()
        for i in range(int(length)):
            flag = self.checkPortal(direction)
            if flag:
                direction = self.velocity.normalize()
                self.type = flag >> 1
                continue
            # self.hitbox.position += direction
            self.hitbox += direction
            # centeredPosition = self.hitbox.get_center()
            centered_position = self.hitbox.get_center()
            if self.type != -1 and GLaDOS.contains_point(centered_position):
                GLaDOS.blood -= 1
                self.destroy()
                return
            elif self.type == -1 and player.hitbox.contains_point(centered_position):
                player.blood -= 1
                self.destroy()
                return
            super_edges = Game.get_instance().map_manager.super_edges
            for edge in super_edges:
                if edge.contains_point(centered_position):
                    self.destroy()
                    return

    def destroy(self):
        self.destroyed = True
        self.velocity = Vector(0, 0)

    def draw(self):
        from game import Game

        angle = -self.velocity.get_angle() - 90
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture(
                "GLaDOSbullets", f"{self.type}-{self.style}"
            ),
            Hitbox(self.hitbox.get_position(), self.hitbox.get_size() * 2),
            angle=angle,
        )
        # Game.get_instance().draw_rect("red", self.hitbox)
