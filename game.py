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
        self.texture_manager = TextureManager(
            os.path.join(os.path.dirname(__file__), "assets/imgs/textures.json")
        )
        self.player = Player(
            Hitbox(4 * basic_size, 4 * basic_size, 1.2 * basic_size, 1.8 * basic_size)
        )

        self.portals = [Portal(), Portal()]
        self.portal_gun = PortalGun()

        self.computations = []
        self.renderings = []
        self.computations.append(self.mouse_manager.update)
        self.computations.append(self.keyboard_manager.update)
        self.computations.append(self.player.update)
        self.computations.append(self.portal_gun.update)
        def make_portal():
            self.portal_gun.update_shooting(
                self.player.hitbox.get_center(), self.mouse_manager.get_position()
            )
            if self.mouse_manager.left:
                self.portal_gun.shot(self.player.hitbox.get_center(), 0)
            if self.mouse_manager.right:
                self.portal_gun.shot(self.player.hitbox.get_center(), 1)
            if self.portal_gun.isHit:
                position = self.portal_gun.position.copy()
                edge = self.portal_gun.edge
                self.portal_gun.isHit = False
                if portal.is_valid_position(
                    position, edge, self.portals[self.portal_gun.flyingType ^ 1]
                ):
                    position = portal.fix_position(position, edge).copy()
                    # print(position, self.portal_gun.flyingType, edge.facing)
                    self.portals[self.portal_gun.flyingType] = Portal(
                        # self.portal_gun.flyingType, position, edge.facing
                        position, self.portal_gun.flyingType, edge.facing
                    )

        self.computations.append(make_portal)
        self.renderings.append(self.map_manager.draw)
        self.renderings.append(self.mouse_manager.draw)
        self.renderings.append(self.player.draw)
        self.renderings.append(self.portal_gun.draw)

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
        self.portals[0].draw()
        self.portals[1].draw()
