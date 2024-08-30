# game.py
import pygame
import map
from datamanager import DataManager
from map import MapManager
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
        self.map_manager.loadFromURL(os.path.join(os.path.dirname(__file__), "Test2.json"))
 
        self.player = Player(Hitbox(4 * map.basicSize, 4 * map.basicSize, 1.2 * map.basicSize, 1.8 * map.basicSize))
        self.computations = []
        self.renderings = []
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

