from components import *


class View:
    def __init__(self, view_data : dict) -> None:
        from game import Game

        self.map_manager = Game.get_instance().map_manager
        self.mouse_manager = Game.get_instance().mouse_manager
        from Entities.player import Player
        from game import basic_size

        self.player = Player(
            Hitbox(
                view_data["player"]["x"],
                view_data["player"]["y"],
                1.2 * basic_size,
                1.8 * basic_size,
            )
        )
        from portal import Portal, is_valid_position, fix_position
        from portal_gun import PortalGun
        from Entities.cube import Cube
        if view_data["cube"]:
            self.cube = Cube(view_data["cube"]["x"], view_data["cube"]["y"])
        else:
            self.cube = None
        self.portals = [
            Portal(
                position = create_vector(view_data["portals"][0]["position"]),
                type = view_data["portals"][0]["type"],
                facing = view_data["portals"][0]["facing"]
            ),
            Portal(
                position = create_vector(view_data["portals"][1]["position"]),
                type = view_data["portals"][1]["type"],
                facing = view_data["portals"][1]["facing"]
            )]
        self.portal_gun = PortalGun()
        self.entities = [self.player]
        from Entities.GLaDOS import GLaDOS
        self.GLaDOS = GLaDOS(view_data.get("GLaDOS", False))
        print(self.GLaDOS.stillAlive)
        if self.cube:
            self.entities.append(self.cube)
        self.events = self.map_manager.events

        self.computations = []
        self.renderings = []

        def make_portal():
            self.portal_gun.update_shooting(
                self.player.hitbox.get_center(), self.mouse_manager.get_position()
            )
            if not self.player.block_move:
                if self.mouse_manager.left:
                    self.portal_gun.shot(self.player.hitbox.get_center(), 0)
                if self.mouse_manager.right:
                    self.portal_gun.shot(self.player.hitbox.get_center(), 1)
            if self.portal_gun.isHit:
                position = self.portal_gun.position.copy()
                edge = self.portal_gun.edge
                self.portal_gun.isHit = False
                if is_valid_position(
                    position, edge, self.portals[self.portal_gun.flyingType ^ 1]
                ):
                    position = fix_position(position, edge).copy()
                    self.portals[self.portal_gun.flyingType] = Portal(
                        position, self.portal_gun.flyingType, edge.facing
                    )

        for entity in self.entities:
            self.computations.append(entity.update)
        self.computations.append(self.portal_gun.update)
        self.computations.append(make_portal)
        self.computations.append(self.GLaDOS.update)
        self.computations.append(self.events.update)

        self.renderings.append(self.map_manager.draw)
        self.renderings.append(self.events.draw)
        for entity in self.entities:
            self.renderings.append(entity.draw)
        
        self.renderings.append(self.GLaDOS.draw)
        self.renderings.append(self.portal_gun.draw)
        self.renderings.append(self.GLaDOS.draw_blood)

    def update(self):
        for computation in self.computations:
            computation()

    def draw(self):
        for rendering in self.renderings:
            rendering()
        self.portals[0].draw()
        self.portals[1].draw()
