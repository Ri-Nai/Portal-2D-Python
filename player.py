import pygame
from components import Hitbox, Vector
from entity import Entity
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
    def update(self):
        def controllerX():
            from game import Game
            moveLeft = Game.get_instance().keyboard_manager.isKeysDown(["A", "Left"])
            moveRight = Game.get_instance().keyboard_manager.isKeysDown(["D", "Right"])
            move = 0
            if moveLeft:
                self.facing = move = -1
            if moveRight:
                self.facing = move = 1
            return move
        def controllerY():
            from game import Game
            return Game.get_instance().keyboard_manager.firstDown("Space", self.jumping.setJumpBuffer())
        self.updateXY(controllerX(), controllerY())
    def draw(self):
        from game import Game
        pygame.draw.rect(Game.get_instance().screen, "pink", self.hitbox)
