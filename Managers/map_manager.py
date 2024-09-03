import pygame
from pygame import Rect
basic_size = 40
half_size = basic_size // 2
class Tile(Rect):
    colors = ["red", "green", "blue"]
    def __init__(self, x, y, width, height, type):
        super().__init__(x, y, width, height)
        self.type = type
        # 这里添加 Tile 类特有的初始化代码
    def __init__(self, hitbox : dict, type):
        super().__init__(hitbox["x"], hitbox["y"], hitbox["width"], hitbox["height"])
        self.type = type
    def draw(self):
        from game import Game
        for i in range(0, self.width, basic_size):
            for j in range(0, self.height, basic_size):
                pygame.draw.rect(Game.get_instance().screen, Tile.colors[self.type], (self.x + i, self.y + j, basic_size, basic_size))
class Layer:
    def __init__(self):
        self.tiles = []
        self.opacity = 1
    def draw(self):
        for tile in self.tiles:
            tile.draw()
class Edge(Tile):
    def __init__(self, x, y, width, height, type, facing):
        super().__init__(x, y, width, height, type)
        self.facing = facing
    def __init__(self, hitbox : dict, type, facing):
        super().__init__(hitbox, type)
        self.facing = facing
    def draw(self):
        from game import Game
        for i in range(0, self.width, basic_size // 2):
            for j in range(0, self.height, basic_size // 2):
                pygame.draw.rect(Game.get_instance().screen, Tile.colors[self.type], (self.x + i, self.y + j, basic_size // 2, basic_size // 2))

class MapManager:
    def __init__(self):
        self.layers : list[Layer] = []
        self.blocks : list[Tile] = []
        self.edges : list[Edge] = []
    def loadFromURL(self, url):
        from game import Game
        data = Game.get_instance().data_manager.loadJSON(url)
        for layers in data["layers"]:
            layer = Layer()
            for tile in layers["tiles"]:
                layer.tiles.append(Tile(tile["hitbox"], tile["type"]))
            self.layers.append(layer)
        for block in data["blocks"]:
            self.blocks.append(Tile(block["hitbox"], block["type"]))
        for edge in data["edges"]:
            self.edges.append(Edge(edge["hitbox"], edge["type"], edge["facing"]))
    def draw(self):
        for block in self.blocks:
            block.draw()
