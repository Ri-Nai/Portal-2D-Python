import pygame
import sys
from components import Vector, Hitbox
class MouseManager:
    def __init__(self, screen):
        self.screen = screen
        self.is_capture = False  # 添加一个属性来跟踪捕获状态
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.left = False
        self.right = False

    def capture(self):
        self.is_capture = True
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def uncapture(self):
        self.is_capture = False
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)

    def update(self):
        # Update mouse position
        self.x, self.y = pygame.mouse.get_pos()
        self.x = max(0, min(self.x, self.screen.get_width()))
        self.y = max(0, min(self.y, self.screen.get_height()))

        # Check mouse buttons
        buttons = pygame.mouse.get_pressed()
        self.left = buttons[0]
        self.right = buttons[2]

    def draw(self):
        if self.is_capture:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x - 3, self.y - 3, 6, 6))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 2, self.y - 2, 4, 4))

    def get_position(self):
        return Vector(self.x, self.y)
