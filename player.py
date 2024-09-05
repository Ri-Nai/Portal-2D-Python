import pygame
from components import Hitbox, Vector
from entity import Entity
from game import basic_size

player_size = Vector(1.2 * basic_size, 1.8 * basic_size)
player_offset = Vector(0.7 * basic_size, 0.4 * basic_size)

class Animation:
    Framerate = {
        "run": 6,
        "jump": 30,
        "fall": 30,
        "stand": 8,
    }
    Frames = {
        "run": 6,
        "jump": 4,
        "fall": 2,
        "stand": 7,
    }
    def __init__(self):
        self.status = "run"
        self.facing = 1
        self.frame = 1
        self.frameRun = 0
    def setStatus(self, status, facing):
        if (status != self.status or facing != self.facing):
            self.frame = 1
            self.frameRun = 0
            self.status = status
            self.facing = facing
    def update(self):
        self.frameRun += 1
        if self.frameRun > Animation.Framerate[ self.status ]:
            self.frame += 1
            self.frameRun = 0
        if self.frame > Animation.Frames[ self.status ]:
            if self.status == "run" or self.status == "stand":
                self.frame = 1
            else:
                self.frame -= 1
    def getFrame(self):
        from game import Game
        return Game.get_instance().texture_manager.get_texture(self.status, self.frame * self.facing)
class Player(Entity):
    """
    position: Vector
    velocity: Vector
    jumping: jumping
    """

    def __init__(self, hitbox : Hitbox) -> None:
        super().__init__(hitbox)
        self.facing = 1
        self.isSpaceHeld = False
        self.animation = Animation()
        self.is_player = True
    def update(self):
        move = 0
        def controllerX():
            from game import Game
            nonlocal move
            moveLeft = Game.get_instance().keyboard_manager.isKeysDown(["A", "Left"])
            moveRight = Game.get_instance().keyboard_manager.isKeysDown(["D", "Right"])
            if moveLeft:
                self.facing = move = -1
            if moveRight:
                self.facing = move = 1
            return move
        def controllerY():
            from game import Game
            return Game.get_instance().keyboard_manager.firstDown("Space", self.jumping.setJumpBuffer)
        self.updateXY(controllerX(), controllerY())
        if self.jumping.jumpVelocity > 0:
            self.animation.setStatus("jump", self.facing)
        elif not self.isOnGround() and self.jumping.jumpVelocity < 0:
            self.animation.setStatus("fall", self.facing)
        else:
            if move:
                self.animation.setStatus("run", self.facing)
            else:
                self.animation.setStatus("stand", self.facing)
        self.animation.update()
        # self.check_out_of_map()
    def draw(self):
        from game import Game
        Game.get_instance().draw_rect("pink", self.hitbox)
        Game.get_instance().draw_image(
            self.animation.getFrame(),
            Hitbox(
                self.hitbox.x - player_offset.x,
                self.hitbox.y - 2 * player_offset.y,
                self.hitbox.width + player_offset.x * 2,
                self.hitbox.height + player_offset.y * 2,
            ),
        )
