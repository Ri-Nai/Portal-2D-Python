from Managers.map_manager import Edge, basic_size, half_size
from components import Hitbox
from components import Vector
unitDirection = [
    Vector(0, -1),
    Vector(-1, 0),
    Vector(0, 1),
    Vector(1, 0)
]
# 传送门半径1.5格
portalRadius = 1 * basic_size
portalWidth = 0.5 * basic_size
portalDirection = [
    Vector(-portalRadius, 0),
    Vector(0, -portalRadius),
    Vector(-portalRadius, -portalWidth),
    Vector(-portalWidth, -portalRadius)
]
portal_size = [
    Vector(2 * portalRadius, portalWidth),
    Vector(portalWidth, 2 * portalRadius)
]
class Portal(Edge):
    def __init__(self, x, y, width, height, type, facing : int):
        position = Vector(x, y)
        position += portalDirection[facing]
        size = Vector(width, height)
        size += portal_size[ facing & 1 ]
        super().__init__(type, position.x, position.y, size.x, size.y, facing)
        self.infacing = facing + 2 & 3
    def isMoveIn(self, hitbox : Hitbox):
        this_left = self.x
        this_right = self.x + self.width
        this_top = self.y
        this_bottom = self.y + self.height

        other_left = hitbox.x
        other_right = hitbox.x + hitbox.width
        other_top = hitbox.y
        other_bottom = hitbox.y + hitbox.height

        contains_x = this_left <= other_left and other_right <= this_right
        contains_y = this_top <= other_top and other_bottom <= this_bottom
        axis = self.facing & 1
        contains_axis = contains_x if axis else contains_y
        return contains_axis and self.collidedict(hitbox)
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
        #ndow.$game.ctx.drawImage(
            window.$game.textureManager.getTexture("portals", `${self.type}-in-${self.facing}`),
            positionX, positionY,
            self.hitbox.size.x, self.hitbox.size.y,
            self.hitbox.position.x,
            self.hitbox.position.y,
            self.hitbox.size.x,
            self.hitbox.size.y
        )
        sizeX = (self.facing & 1 ^ 1) * basic_size + basic_size
        sizeY = (self.facing & 1) * basic_size + basic_size
        window.$game.ctx.drawImage(
            window.$game.textureManager.getTexture("portals", `${self.type}-out-${self.facing}`),
            0, 0, sizeX, sizeY,
            self.hitbox.position.x + unitDirection[ self.facing ].x * half_size * (2 - (self.facing >> 1)),
            self.hitbox.position.y + unitDirection[ self.facing ].y * half_size * (2 - (self.facing >> 1)),
            sizeX, sizeY
        )
    }

    /**
     * @param {Vector} position
     * @param {Edge} edge
     * @param {Portal} anotherPortal
     */
    static valid(position, edge, anotherPortal) {
        const portal_size = portal_size[ edge.facing & 1 ]
        if (edge.type != 2)
            return false
        const edgeSize = edge.hitbox.size

        const edgeLength = edge.facing & 1 ? edgeSize.y : edgeSize.x
        const portalLength = edge.facing & 1 ? portal_size.y : portal_size.x

        const leftUp = position.addVector(portalDirection[ edge.facing ])
        const rightDown = leftUp.addVector(portal_size[ edge.facing & 1 ])

        if (anothertype === -1) {
            return edgeLength >= portalLength
        }

        const hitAnother = anotherhitbox.contains(leftUp)
            || anotherhitbox.contains(rightDown)

        return edgeLength >= portalLength and !hitAnother
    }

    /**
     *
     * @param {Vector} position
     * @param {Edge} edge
     */
    static fixPosition(position, edge) {
        const leftUp = position.addVector(portalDirection[ edge.facing ])
        const rightDown = leftUp.addVector(portal_size[ edge.facing & 1 ])

        if (edge.hitbox.contains(leftUp) and edge.hitbox.contains(rightDown)) {
            return position
        }

        if (edge.hitbox.contains(rightDown)) {
            return edge.hitbox.position.subVector(portalDirection[ edge.facing ])
        }

        else {
            const delta = [
                new Vector(-self.portalRadius, -self.portalWidth),
                new Vector(-self.portalWidth, -self.portalRadius),
                new Vector(-self.portalRadius, 0),
                new Vector(0, -self.portalRadius)
            ]
            return edge.hitbox.position.addVector(edge.hitbox.size).addVector(delta[ edge.facing ])
        }
    }
}
