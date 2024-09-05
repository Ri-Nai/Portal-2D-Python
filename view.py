from components import *


class View:
    def __init__(self) -> None:
        from game import Game
        self.map_manager = Game.get_instance().map_manager
        self.mouse_manager = Game.get_instance().mouse_manager
        from player import Player
        from game import basic_size
        self.player = Player(
            Hitbox(4 * basic_size, 4 * basic_size, 1.2 * basic_size, 1.8 * basic_size)
        )
        from portal import Portal, is_valid_position, fix_position
        from portal_gun import PortalGun

        self.portals = [Portal(), Portal()]
        self.portal_gun = PortalGun()
        self.entities = [self.player]

        self.computations = []
        self.renderings = []
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
                if is_valid_position(
                    position, edge, self.portals[self.portal_gun.flyingType ^ 1]
                ):
                    position = fix_position(position, edge).copy()
                    self.portals[self.portal_gun.flyingType] = Portal(
                        position, self.portal_gun.flyingType, edge.facing
                    )

        self.computations.append(make_portal)
        self.renderings.append(self.map_manager.draw)
        self.renderings.append(self.player.draw)
        self.renderings.append(self.portal_gun.draw)

    def update(self):
        for computation in self.computations:
            computation()

    def draw(self):
        for rendering in self.renderings:
            rendering()
        self.portals[0].draw()
        self.portals[1].draw()