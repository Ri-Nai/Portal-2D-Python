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

        self.left_held = False
        self.right_held = False

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
    def is_down(self, key):
        if key == "Left":
            return self.left
        if key == "Right":
            return self.right
    
    def first_down(self, key, operate = None):
        if key == "Left":
            if self.left:
                if not self.left_held:
                    if operate: operate()
                self.left_held = True
                return True
            else:
                self.left_held = False
                return False
        if key == "Right":
            if self.right:
                if not self.right_held:
                    if operate: operate()
                self.right_held = True
                return True
            else:
                self.right_held = False
                return False
    def draw(self):
        if self.is_capture:
            # pygame.draw.rect(self.screen, (255, 255, 255), (self.x - 3, self.y - 3, 6, 6))
            # pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 2, self.y - 2, 4, 4))
            from game import Game
            Game.get_instance().draw_image(Game.get_instance().texture_manager.get_texture("cursor"), Hitbox(self.x - 4, self.y - 5, 16, 22), Hitbox(12, 9, 16, 22))

    def get_position(self):
        return Vector(self.x, self.y)
