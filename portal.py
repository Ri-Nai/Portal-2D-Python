from Managers.map_manager import Edge, basic_size, half_size
from components import Hitbox, Vector, create_hitbox
unit_direction = [
    Vector(0, -1),
    Vector(-1, 0),
    Vector(0, 1),
    Vector(1, 0)
]
# 传送门半径1.5格
portal_radius = 1 * basic_size
portal_width = 0.5 * basic_size
portalDirection = [
    Vector(-portal_radius, 0),
    Vector(0, -portal_radius),
    Vector(-portal_radius, -portal_width),
    Vector(-portal_width, -portal_radius)
]
portal_size = [
    Vector(2 * portal_radius, portal_width),
    Vector(portal_width, 2 * portal_radius)
]
class Portal(Edge):
    def __init__(self, position = Vector(), type = -1, facing : int  = 0):
        position = position.copy() + portalDirection[facing]
        # size = Vector(width, height)
        size = portal_size[ facing & 1 ]
        super().__init__(Hitbox(position.x, position.y, size.x, size.y), type, facing)
        self.infacing = facing + 2 & 3
        # print(self.type)
    def isMoveIn(self, hitbox : Hitbox):
        contains_x = self.left <= hitbox.left and hitbox.right <= self.right
        contains_y = self.top <= hitbox.top and hitbox.bottom <= self.bottom
        # print(hitbox)
        axis = self.facing & 1
        contains_axis = contains_y if axis else contains_x
        return contains_axis and self.colliderect(hitbox)
    def draw(self):
        if self.type == -1:
            return
        #0, 0, 80, 20
        #0, 0, 20, 80
        #0, 20, 80, 20
        #20, 0, 20, 80
        positionX = (self.facing >> 1) * (self.facing & 1) * half_size
        positionY = (self.facing >> 1) * (self.facing & 1  ^ 1) * half_size

        #0, 0, 80, 40
        #0, 0, 40, 80
        #0, 0, 80, 40
        #0, 0, 40, 80
        from game import Game
        # print("!")
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture("portals", f"{self.type}-in-{self.facing}"),
            self,
            Hitbox(positionX, positionY, self.width, self.height)
        )
        sizeX = (self.facing & 1 ^ 1) * basic_size + basic_size
        sizeY = (self.facing & 1) * basic_size + basic_size
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture("portals", f"{self.type}-out-{self.facing}"),
            Hitbox(self.get_position() + unit_direction[ self.facing ] * half_size * (2 - (self.facing >> 1)), Vector(sizeX, sizeY)),
            Hitbox(0, 0, sizeX, sizeY)
        )
        """
        window.$game.ctx.drawImage(
            window.$game.textureManager.getTexture("portals", `${self.type}-in-${self.facing}`),
            positionX, positionY,
            self.hitbox.size.x, self.hitbox.size.y,
            self.hitbox.position.x,
            self.hitbox.position.y,
            self.hitbox.size.x,
            self.hitbox.size.y
        )
        window.$game.ctx.drawImage(
            window.$game.textureManager.getTexture("portals", `${self.type}-out-${self.facing}`),
            0, 0, sizeX, sizeY,
            self.hitbox.position.x + unit_direction[ self.facing ].x * half_size * (2 - (self.facing >> 1)),
            self.hitbox.position.y + unit_direction[ self.facing ].y * half_size * (2 - (self.facing >> 1)),
            sizeX, sizeY
        )
        """
def is_valid_position(position : Vector, edge : Edge, anotherPortal : "Portal"):
    portal_size_now = portal_size[ edge.facing & 1 ]

    if edge.type != 2:
        return False

    edge_length = edge.height if (edge.facing & 1) else edge.width
    portal_length = portal_size_now.y if (edge.facing & 1) else portal_size_now.x

    left_up = position + portalDirection[ edge.facing ]
    right_down = left_up + portal_size[ edge.facing & 1 ]

    if anotherPortal.type == -1:
        return edge_length >= portal_length
    hitAnother = anotherPortal.colliderect(create_hitbox(left_up, right_down))

    return edge_length >= portal_length and not hitAnother
def fix_position(position : Vector, edge : Edge):
    left_up = position + portalDirection[ edge.facing ]
    right_down = left_up + portal_size[ edge.facing & 1 ]
    if edge.contains_point(left_up) and edge.contains_point(right_down):
        return position
    if edge.contains_point(right_down):
        return edge.get_position() - portalDirection[ edge.facing ]
    delta = [
        Vector(-portal_radius, -portal_width),
        Vector(-portal_width, -portal_radius),
        Vector(-portal_radius, 0),
        Vector(0, -portal_radius)
    ]
    return edge.get_position() + (edge.get_size()) + delta[ edge.facing ]
