import pygame
from components import Vector, Hitbox

basic_size = 40
half_size = basic_size // 2
offset_size = 1.6

class Tile(Hitbox):
    colors = ["red", "green", "blue"]

    # 这里添加 Tile 类特有的初始化代码
    def __init__(self, hitbox, type_: int):
        if type(hitbox) == dict:
            super().__init__(
                hitbox["x"], hitbox["y"], hitbox["width"], hitbox["height"]
            )
        else:
            super().__init__(hitbox.x, hitbox.y, hitbox.width, hitbox.height)
        self.type = type_

    def draw(self, kind):
        from game import Game

        for i in range(0, self.width, basic_size):
            for j in range(0, self.height, basic_size):
                # pygame.draw.rect(Game.get_instance().screen, Tile.colors[self.type], (self.x + i, self.y + j, basic_size, basic_size))
                Game.get_instance().draw_image(
                    Game.get_instance().texture_manager.get_texture(kind, self.type),
                    Hitbox(self.x + i - offset_size, self.y + j - offset_size, basic_size + offset_size * 2, basic_size + offset_size * 2),
                )


class Layer:
    def __init__(self):
        self.tiles = []
        self.opacity = 1

    def draw(self, kind):
        for tile in self.tiles:
            tile.draw(kind)


class Edge(Tile):
    def __init__(self, hitbox, type: int, facing: int):
        super().__init__(hitbox, type)
        self.facing = facing

    def draw(self):
        from game import Game

        """
        for i in range(0, self.width, basic_size // 2):
            for j in range(0, self.height, basic_size // 2):
                # pygame.draw.rect(Game.get_instance().screen, Tile.colors[self.type], (self.x + i, self.y + j, basic_size // 2, basic_size // 2))
                Game.get_instance().draw_rect(Tile.colors[self.type], (self.x + i, self.y + j, basic_size // 2, basic_size // 2))
        """

typename = ["backgrounds", "", "", "backgroundTextures", "", "", ""]
class MapManager:
    def __init__(self):
        self.layers: list[Layer] = []
        self.blocks: list[Tile] = []
        self.edges: list[Edge] = []
        self.super_edges: list[Edge] = []

    def loadFromURL(self, url):
        from game import Game

        data = Game.get_instance().data_manager.loadJSON(url)
        for layers in data["layers"]:
            layer = Layer()
            for tile in layers["tiles"]:
                layer.tiles.append(Tile(tile["hitbox"], tile["type"]))
            self.layers.append(layer)
        print(self.layers)
        for block in data["blocks"]:
            self.blocks.append(Tile(block["hitbox"], block["type"]))
        for edge in data["edges"]:
            self.edges.append(Edge(edge["hitbox"], edge["type"], edge["facing"]))
        for super_edge in data["super_edges"]:
            self.super_edges.append(
                Edge(super_edge["hitbox"], super_edge["type"], super_edge["facing"])
            )

    def draw(self):
        for i, layer in enumerate(self.layers):
            layer.draw(typename[i])
        for block in self.blocks:
            block.draw("blocks")
