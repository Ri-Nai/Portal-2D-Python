import pygame
import sys
from components import Vector, Hitbox
class MouseManager:
    def __init__(self, screen):
        self.screen = screen
        self.is_capture = False
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.left = False
        self.right = False

    def capture(self):
        if not self.is_capture:
            self.is_capture = True
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

    def uncapture(self):
        if self.is_capture:
            self.is_capture = False
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

    def update(self):
        # Update mouse position
        if self.is_capture:
            self.x, self.y = pygame.mouse.get_pos()
            self.x = max(0, min(self.x, self.screen.get_width()))
            self.y = max(0, min(self.y, self.screen.get_height()))
        else:
            self.x, self.y = pygame.mouse.get_pos()

        # Check mouse buttons
        buttons = pygame.mouse.get_pressed()
        self.left = buttons[0]
        self.right = buttons[2]

    def get_position(self):
        return Vector(self.x, self.y)
