# game.py
import pygame
from Managers import DataManager
from Managers import MapManager, Edge, basic_size
from Managers import MouseManager
from Managers import KeyboardManager
from Managers import TextureManager
from player import Player
from components import Hitbox, Vector
import portal
import portal_gun
from portal import Portal
from portal_gun import PortalGun
from view import View
import os


class Game:
    _instance = None

    def __init__(self, screen: pygame.Surface):
        if Game._instance is not None:
            raise RuntimeError("Game instance already exists!")
        Game._instance = self  # 使用类属性来存储单例实例
        self.screen = screen
        self.texture_manager = TextureManager(
            os.path.join(os.path.dirname(__file__), "assets/imgs/textures.json")
        )
        self.data_manager = DataManager()
        self.map_manager = MapManager()
        self.map_manager.loadFromURL(
            os.path.join(os.path.dirname(__file__), "assets/stages/maps", "Test2.json")
        )
        self.mouse_manager = MouseManager(screen)
        self.keyboard_manager = KeyboardManager()
        self.view = View()

        self.computations = []
        self.renderings = []
        
        self.computations.append(self.mouse_manager.update)
        self.computations.append(self.keyboard_manager.update)
        self.computations.append(self.view.update)

        self.renderings.append(self.view.draw)
        self.renderings.append(self.mouse_manager.draw)

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
        # 如果 src_rect 为 None，则绘制整个图像
        if src_rect is None:
            src_rect = pygame.Rect(0, 0, texture.get_width(), texture.get_height())

        # 缩放图像
        resized_texture = pygame.transform.smoothscale(
            texture, (dest_rect.width, dest_rect.height)
        )

        # 如果需要旋转
        if angle != 0:
            # 计算旋转前的图像中心
            center = resized_texture.get_rect(center=(src_rect.centerx, src_rect.centery))
            # 旋转图像
            rotated_texture = pygame.transform.rotate(resized_texture, angle)
            # 获取旋转后图像的矩形
            rotated_rect = rotated_texture.get_rect()
            # 将旋转后图像的中心移动到目标矩形的中心
            rotated_rect.center = dest_rect.center
        else:
            # 如果不需要旋转，直接使用缩放后的图像
            rotated_texture = resized_texture
            rotated_rect = rotated_texture.get_rect()
            rotated_rect.center = dest_rect.center

        # 绘制图像
        self.screen.blit(rotated_texture, rotated_rect.topleft)

    def loop(self):
        # 游戏主循环代码
        self.screen.fill((255, 255, 255))
        for computation in self.computations:
            computation()
        for rendering in self.renderings:
            rendering()
        # print(self.portals[0].type)
        
