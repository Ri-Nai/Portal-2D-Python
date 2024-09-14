# game.py
import pygame
from Managers import *
from pause_screen import PauseScreen
from Entities.player import Player
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
            os.path.join(os.path.dirname(__file__), "assets/imgs/Textures.json")
        )
        self.data_manager = DataManager()
        self.map_manager = MapManager()
        self.mouse_manager = MouseManager(screen)
        self.keyboard_manager = KeyboardManager()
        self.sound_manager = SoundManager(
            os.path.join(os.path.dirname(__file__), "assets/audios/Sounds.json")
        )
        self.dialog_manager = DialogManager()
        self.pause_screen = PauseScreen()

        self.load()
        self.is_paused = False

    def load(self, url = "Room1.json"): 
        self.current_url = url
        self.map_manager.loadFromURL(
            os.path.join(os.path.dirname(__file__), "assets/stages/maps", url)
        )
        view_data = self.data_manager.loadJSON(
            os.path.join(os.path.dirname(__file__), "assets/stages/positions", url)
        )
        self.view = View(view_data)
        self.dialog_manager.load(
            os.path.join(os.path.dirname(__file__), "assets/stages/dialogs", url)
        )
        self.computations = []
        self.renderings = []
        
        self.computations.append(self.mouse_manager.update)
        self.computations.append(self.keyboard_manager.update)
        self.computations.append(self.view.update)
        self.computations.append(self.sound_manager.update)
        self.computations.append(self.dialog_manager.update)

        self.renderings.append(self.view.draw)
        self.renderings.append(self.mouse_manager.draw)
        self.renderings.append(self.pause_screen.draw)
        self.renderings.append(self.dialog_manager.draw)

    @classmethod
    def get_instance(cls, screen: pygame.Surface = None):
        if cls._instance is None:
            cls._instance = cls(screen)
        return cls._instance

    def draw_rect(self, color, dest_rect):
        # self.screen.fill(color, dest_rect)
        pygame.draw.rect(self.screen, color, dest_rect)

    def draw_image(self, texture, dest_rect, src_rect=None, angle=0):
        """绘制图像，从 texture 的 src_rect 区域裁剪并绘制到 dest_rect"""
        if not texture:
            print("Texture not found")
            return
        
        # 如果 src_rect 为 None，则使用整个图像
        if src_rect is None:
            src_rect = pygame.Rect(0, 0, texture.get_width(), texture.get_height())
        
        # 从源图像裁剪出 src_rect 区域
        cropped_texture = texture.subsurface(src_rect)
        
        # 缩放图像
        resized_texture = pygame.transform.smoothscale(
            cropped_texture, (dest_rect.width, dest_rect.height)
        )
        
        # 如果需要旋转
        if angle != 0:
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

    def switch_view(self, url):
        self.load(url)
        if "14" in url:
            pygame.mixer.stop()
            pygame.mixer.music.load("assets/audios/bgms/上海アリス幻樂団 - 月まで届け、不死の煙.mp3")
            pygame.mixer.music.play(-1)
        elif "over" in url:
            pygame.mixer.stop()
            pygame.mixer.music.load("assets/audios/bgms/村上純 - かえり道.mp3")
            pygame.mixer.music.play(-1)

    def loop(self):
        # 游戏主循环代码
        self.screen.fill((255, 255, 255))
        if not self.is_paused:
            for computation in self.computations:
                computation()
        for rendering in self.renderings:
            rendering()

    def toggle_pause(self, status: bool):
        self.pause() if status else self.resume()

    def pause(self):
        self.is_paused = True
        self.sound_manager.play_sound("pause")
        
    def resume(self):
        self.is_paused = False
        self.mouse_manager.capture()
        self.sound_manager.play_sound("resume")
    
    def restart(self):
        self.load(self.current_url)
        self.resume()
