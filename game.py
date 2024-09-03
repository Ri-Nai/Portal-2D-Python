# game.py
import pygame
from Managers import DataManager
from Managers import MapManager, basic_size
from Managers import MouseManager
from Managers import KeyboardManager
from Managers import TextureManager
from player import Player
from components import Hitbox, Vector
import os


class Game:
    _instance = None

    def __init__(self, screen: pygame.Surface):
        if Game._instance is not None:
            raise RuntimeError("Game instance already exists!")
        Game._instance = self  # 使用类属性来存储单例实例
        self.screen = screen
        self.data_manager = DataManager()
        self.map_manager = MapManager()
        self.map_manager.loadFromURL(
            os.path.join(os.path.dirname(__file__), "assets/stages/maps", "Test2.json")
        )
        self.mouse_manager = MouseManager(screen)
        self.keyboard_manager = KeyboardManager()
        self.texture_manager = TextureManager(os.path.join(os.path.dirname(__file__), "assets/imgs/textures.json"))

        self.player = Player(
            Hitbox(4 * basic_size, 4 * basic_size, 1.2 * basic_size, 1.8 * basic_size)
        )
        self.computations = []
        self.renderings = []
        self.computations.append(self.mouse_manager.update)
        self.computations.append(self.keyboard_manager.update)
        self.computations.append(self.player.update)
        self.renderings.append(self.map_manager.draw)
        self.renderings.append(self.mouse_manager.draw)
        self.renderings.append(self.player.draw)

    @classmethod
    def get_instance(cls, screen: pygame.Surface = None):
        if cls._instance is None:
            cls._instance = cls(screen)
        return cls._instance
    def draw_rect(self, color, dest_rect):
        # self.screen.fill(color, dest_rect)
        pygame.draw.rect(self.screen, color, dest_rect)
    def draw_image(self, texture, dest_rect, src_rect=None, angle=0):
        """绘制图像"""
        if not texture:
            print("Texture not found")
            return
        resized_texture = pygame.transform.smoothscale(texture, (dest_rect.width, dest_rect.height))
        # 如果 src_rect 为 None，则绘制整个图像
        if angle == 0:
            return self.screen.blit(resized_texture, dest_rect, src_rect)
        center = src_rect.width // 2, src_rect.height // 2
        rotated_texture = pygame.transform.rotate(resized_texture, angle)
        rotated_rect = rotated_texture.get_rect(center=(center, center))
        dest_center = dest_rect.center
        rotated_rect.center = dest_center
        self.screen.blit(rotated_texture, rotated_rect.topleft)

    def loop(self):
        # 游戏主循环代码
        self.screen.fill((255, 255, 255))
        for computation in self.computations:
            computation()
        for rendering in self.renderings:
            rendering()
