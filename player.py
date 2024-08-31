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
            moveLeft = pygame.key.get_pressed()[pygame.K_a]
            moveRight = pygame.key.get_pressed()[pygame.K_d]
            move = 0
            if moveLeft:
                self.facing = move = -1
            if moveRight:
                self.facing = move = 1
            return move
        def controllerY():
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if not self.isSpaceHeld:
                    self.jumping.setJumpBuffer()
                self.isSpaceHeld = True
            else:
                self.isSpaceHeld = False
            return self.isSpaceHeld
        self.updateXY(controllerX(), controllerY())
    def draw(self):
        from game import Game
        pygame.draw.rect(Game.get_instance().screen, "pink", self.hitbox)
