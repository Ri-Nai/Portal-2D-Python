from components import Vector, Hitbox
class PortalGun:

    def __init__(self):
        self.status = [ False, False ]
        self.direction = Vector(1, 0)
        # 发射间隔
        self.INTERVAL = 15
        self.buffer = 15
        self.isShot = False
        self.isHit = False
        self.target = 0

        self.flyingType = 0
        self.COLOR = [ "blue", "orange" ]
        self.edge = None

    def update(self, player : Vector, mouse : Vector):
        if self.isShot:
            return
        self.direction = (mouse + player).normalize()
    def shot(self, player : Vector, type):
        SPEED = 25
        if self.status[ type ]:
            return
        self.buffer -= 1
        if self.buffer <= 0 and self.isShot == False:
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
        from math import atan, pi

        # angle = atan(self.direction.y / self.direction.x) / pi * 180
        # (self.direction.x < 0) ? (angle > 0) ? angle -= 180 : angle += 180 : angle
        angle = self.direction.get_angle()
        from game import Game
        Game.get_instance().draw_image(
            Game.get_instance().texture_manager.get_texture("portalBullets", self.COLOR[ self.flyingType ]),
            Hitbox(self.position.x, self.position.y, 20, 20),
            Hitbox(10, 10, 20, 20),
            angle
        )
        """
        TODO:

        const texture = window.$game.textureManager.getTexture("portalBullets", self.COLOR[ self.flyingType ])
        const rotated = window.$game.textureManager.rotateTexture(texture, angle)

        window.$game.ctx.drawImage(rotated, 10, 10, 20, 20, self.position.x, self.position.y, 20, 20)
        """
    def update():
        """
        /**
         * @type {Edge[]}
         */
        const edges = window.$game.map.edges
        const superEdges = window.$game.map.superEdges

        let validEdges = edges.filter((edge) => { return edge.type == 2 })
        for (let i = 0 i < self.target i++) {
            self.position.addEqual(self.direction)

            if (not validPosition(self.position)) {
                self.isShot = False
                return
            }
            let done = False
            for (let edge of edges) {
                if (edge.hitbox.contains(self.position)) {
                    self.isShot = False
                    self.isHit = True
                    self.edge = edge
                    self.position = fixPosition(self.position, edge)
                    done = True
                    break
                }
            }
            for (let edge of gelledEdgeList) {
                if (edge.hitbox.contains(self.position)) {
                    self.isShot = False
                    self.isHit = True
                    let newEdge = new Edge(edge.type, edge.hitbox.position.copy(), edge.hitbox.size.copy(), edge.facing)
                    for (let valid of validEdges)
                        if (valid.facing == newEdge.facing and valid.hitbox.hit(newEdge.hitbox))
                            newEdge.hitbox = newEdge.hitbox.merge(valid.hitbox)
                    self.edge = newEdge
                    self.position = fixPosition(self.position, edge)
                    done = True
                    break
                }
            }
            if (done)
                return
            for (let superEdge of superEdges) {
                if (superEdge.hitbox.contains(self.position)) {
                    self.isShot = False
                    done = True
                    break
                }
            }
            if (done)
                return
        }
    }
}

        """
const validPosition = (position) => {
    return (
        position.x >= 0 and
        position.x <= window.$game.canvas.width and
        position.y >= 0 and
        position.y <= window.$game.canvas.height
    )
}

/**
 *
 * @param {Vector} position
 * @param {Edge} edge
 */
const fixPosition = (position, edge) => {
    const fix = [
        new Vector(position.x, edge.hitbox.getTopLeft().y),
        new Vector(edge.hitbox.getTopLeft().x, position.y),
        new Vector(position.x, edge.hitbox.getBottomRight().y),
        new Vector(edge.hitbox.getBottomRight().x, position.y),
    ]
    return fix[ edge.facing ]
}
