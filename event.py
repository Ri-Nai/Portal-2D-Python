import pygame
from Managers.map_manager import Tile


class GameEvent(Tile):
    def __init__(self, id, type, hitbox, affect):
        super().__init__(hitbox, type)
        self.id = id
        self.activated = False
        self.affect = affect

    def update(self):
        from game import Game

        entities = Game.get_instance().view.entities
        is_activate = False

        for entity in entities:
            if self.colliderect(entity.hitbox):
                if is_activate:
                    return
                self.activate()
                is_activate = True
        self.activated = is_activate
        if not is_activate:
            self.deactivate()

    def activate(self):
        if not self.activated:
            self.activated = True
            self.on_activate()

        for id in self.affect:
            from game import Game
            event = Game.get_instance().map_manager.events.get_event(id)
            event.activate()

    def deactivate(self):
        if self.activated:
            self.on_deactivate()
        self.activated = False
        for id in self.affect:
            from game import Game
            event = Game.get_instance().map_manager.events.get_event(id)
            event.deactivate()

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def draw(self):
        pass
