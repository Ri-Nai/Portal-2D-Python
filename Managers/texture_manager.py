import pygame
import json

class TextureManager:
    def __init__(self, json_path):
        self.textures = {}
        self.load_textures(json_path)

    def load_textures(self, json_path):
        """从 JSON 文件中读取图像路径并加载图像资源"""
        with open(json_path, 'r') as file:
            data = json.load(file)
            for category, textures in data.items():
                self.textures[category] = {}
                for key, path in textures.items():
                    self.textures[category][key] = pygame.image.load(path)

    def get_texture(self, category, key):
        """获取图像资源"""
        return self.textures.get(str(category), {}).get(str(key))
