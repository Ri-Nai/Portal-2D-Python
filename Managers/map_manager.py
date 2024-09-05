import pygame
from components import Vector, Hitbox

basic_size = 40
half_size = basic_size // 2
offset_size = 1.6


class Tile(Hitbox):
    colors = ["red", "green", "blue"]

    def __init__(self, hitbox, type_: int):
        if type(hitbox) == dict:
            super().__init__(
                hitbox["x"], hitbox["y"], hitbox["width"], hitbox["height"]
            )
        else:
            super().__init__(hitbox.x, hitbox.y, hitbox.width, hitbox.height)
        self.type = type_

    def draw(self, kind, screen=None):
        from game import Game

        if screen == None:
            screen = Game.get_instance().screen
        if kind == "backgroundObjects":
            texture = Game.get_instance().texture_manager.get_texture(
                kind, self.type
            )
            if texture:
                scaled_texture = pygame.transform.smoothscale(
                    texture,
                    (self.width, self.height),
                )
                screen.blit(scaled_texture, self)
            else:
                print(f"Texture not found for type {self.type} in kind {kind}")
        else:
            for i in range(0, self.width, basic_size):
                for j in range(0, self.height, basic_size):
                    texture = Game.get_instance().texture_manager.get_texture(
                        kind, self.type
                    )
                    if texture:
                        scaled_texture = pygame.transform.smoothscale(
                            texture,
                            (basic_size + offset_size * 2, basic_size + offset_size * 2),
                        )
                        dest_rect = pygame.Rect(
                            self.x + i - offset_size,
                            self.y + j - offset_size,
                            basic_size + offset_size * 2,
                            basic_size + offset_size * 2,
                        )
                        screen.blit(scaled_texture, dest_rect)
                    else:
                        print(f"Texture not found for type {self.type} in kind {kind}")


class Layer:
    def __init__(self):
        self.tiles = []
        self.opacity = 1

    def draw(self, kind, screen):
        for tile in self.tiles:
            tile.draw(kind, screen)


class Edge(Tile):
    def __init__(self, hitbox, type: int, facing: int):
        super().__init__(hitbox, type)
        self.facing = facing


typename = [
    "backgrounds",
    "",
    "",
    "backgroundTextures",
    "backgroundObjects",
    "",
    "signs",
]


class MapManager:
    def __init__(self):
        self.clear()
    def clear(self):
        self.layers: list[Layer] = []
        self.blocks: list[Tile] = []
        self.edges: list[Edge] = []
        self.super_edges: list[Edge] = []
        from event_list import EventList
        self.events = EventList()
        self.prerendered_map_surface = None
    def loadFromURL(self, url):
        from game import Game
        self.clear()
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
        for super_edge in data["super_edges"]:
            self.super_edges.append(
                Edge(super_edge["hitbox"], super_edge["type"], super_edge["facing"])
            )
        self.events.init(data["events"])
        print(data["events"])
        self.prerender_map()

    def prerender_map(self):
        from game import Game

        screen_width, screen_height = Game.get_instance().screen.get_size()
        self.prerendered_map_surface = pygame.Surface((screen_width, screen_height))
        self.prerendered_map_surface.fill((0, 0, 0))  # 用黑色填充背景

        # 遍历所有砖块并绘制到 Surface 上
        for i, layer in enumerate(self.layers):
            layer.draw(typename[i], self.prerendered_map_surface)
        for block in self.blocks:
            block.draw("blocks", self.prerendered_map_surface)

    def draw(self):
        from game import Game

        if self.prerendered_map_surface:
            Game.get_instance().screen.blit(self.prerendered_map_surface, (0, 0))
