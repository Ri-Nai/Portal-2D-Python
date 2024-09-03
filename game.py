# game.py
import pygame
from Managers import DataManager
from Managers import MapManager, basic_size
from Managers import MouseManager
from Managers import KeyboardManager
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
        self.map_manager.loadFromURL(os.path.join(os.path.dirname(__file__), "assets/stages/maps", "Test2.json"))
        self.mouse_manager = MouseManager(screen)
        self.keyboard_manager = KeyboardManager()

        self.player = Player(Hitbox(4 * basic_size, 4 * basic_size, 1.2 * basic_size, 1.8 * basic_size))
        self.computations = []
        self.renderings = []
        self.computations.append(self.mouse_manager.update)
        self.computations.append(self.keyboard_manager.update)
        self.computations.append(self.player.update)
        self.renderings.append(self.map_manager.draw)
        self.renderings.append(self.player.draw)

    @classmethod
    def get_instance(cls, screen: pygame.Surface = None):
        if cls._instance is None:
            cls._instance = cls(screen)
        return cls._instance

    def loop(self):
        # 游戏主循环代码
        self.screen.fill((255, 255, 255))
        for computation in self.computations:
            computation()
        for rendering in self.renderings:
            rendering()

