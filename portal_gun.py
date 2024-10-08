from components import Vector, Hitbox
class PortalGun:

    def __init__(self):
        self.status = [ False, False ]
        self.direction = Vector(1, 0)
        # 发射间隔
        self.buffer = self.INTERVAL = 5
        self.isShot = False
        self.isHit = False
        self.target = 0

        self.flyingType = 0
        self.COLOR = [ "blue", "orange" ]
        self.edge = None

    def update_shooting(self, player : Vector, mouse : Vector):
        if self.isShot:
            return
        self.direction = (mouse - player).normalize()
        # print(mouse, self.direction)
    def shot(self, player : Vector, type : int):
        SPEED = 25
        if self.status[ type ]:
            return
        self.buffer -= 1
        if self.buffer <= 0 and self.isShot == False:
            from game import Game
            Game.get_instance().sound_manager.play_sound("portal-shooting", str(type))
            self.buffer = self.INTERVAL
            self.position = Vector(player.x, player.y)
            self.isShot = True
            self.isHit = False
            self.target = (self.direction * SPEED).magnitude()
            self.flyingType = type
            self.edge = None

    def draw(self):
        if not self.isShot:
            return
        from game import Game
        angle = -self.direction.get_angle()
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture("portalBullets", self.COLOR[ self.flyingType ]),
            Hitbox(self.position.x, self.position.y, 20, 20),
            Hitbox(10, 10, 20, 20),
            angle
        )
    def update(self):
        if not self.isShot:
            return
        from game import Game
        # edges = window.$game.map.edges
        edges = Game.get_instance().map_manager.edges
        # superEdges = window.$game.map.superEdges
        super_edges = Game.get_instance().map_manager.super_edges

        for i in range(int(self.target)):
            self.position += self.direction

            if not is_valid_position(self.position):
                self.isShot = False
                return

            done = False
            for edge in edges:
                if edge.contains_point(self.position):
                    self.isShot = False
                    self.isHit = True
                    self.edge = edge
                    self.position = fix_position(self.position, edge)
                    done = True
                    break
            if done:
                return
            for super_edge in super_edges:
                if super_edge.contains_point(self.position):
                    self.isShot = False
                    done = True
                    break
            if done:
                return
def is_valid_position(position : Vector):
    from game import Game
    return (
        position.x >= 0 and
        position.x <= Game.get_instance().screen.get_width() and
        position.y >= 0 and
        position.y <= Game.get_instance().screen.get_height()
    )


from game import Edge
def fix_position(position : Vector, edge : Edge):
    fix = [
        Vector(position.x, edge.y),
        Vector(edge.x, position.y),
        Vector(position.x, edge.y + edge.height),
        Vector(edge.x + edge.width, position.y)
    ]
    return fix[ edge.facing ].copy()
