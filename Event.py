import pygame
from map import Tile

class GameEvent(Tile):
    def __init__(self, id, type, x, y, width, height, affect):
        super().__init__(x, y, width, height, type)
        self.id = id
        self.activated = False
        self.affect = affect

    def update(self):
        entities = kong #待定
        isActivate = False
        
        for entity in entities:
            if self.hitbox.hit(entity.hitbox):
                if isActivate :return
            self.activate(self)
            isActivate = True

        self.activated = isActivate
        if not self.activated :
            self.deactivate(self)

    def activate(self):
        if not self.activated:
            self.activated = True
            self.onActivate(self)

        for id in self.affect:
            event= kong #待定
            event.activate(self)

    def deactivate(self):
        if self.activated:
            self.onDeactivate(self)
        self.activated = False
        for id in self.affect:
            event = kong #待定
            event.deactivate(self)

    def onActivate(self):
        pass

    def onDeactivate(self):
        pass

    def draw(self):   
        pass
