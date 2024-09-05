import pygame
class Jumping:
    def __init__(self, baseJump, maxJump, gravity, coyoteTime, jumpBufferTime) -> None:
        self.baseJump = baseJump
        self.maxJump = maxJump
        self.gravity = gravity
        self.coyoteTime = coyoteTime
        self.jumpBufferTime = jumpBufferTime

        self.isJumping = False
        self.isFalling = False
        self.jumpVelocity = 0
        self.chargeTime = 0
        self.coyoteTimer = 0
        self.jumpBuffer = 0
        self.isSpaceHeld = False
    def canJump(self, onGround):
        if (onGround):
            # print(self.coyoteTimer)
            self.coyoteTimer = self.coyoteTime
            self.isJumping = False
            self.isFalling = False
            self.jumpVelocity = 0
            if self.jumpBuffer > 0:
                self.startJump()
        else:
            if not self.isJumping:
                self.isFalling = True
            self.coyoteTimer = max(self.coyoteTimer - 1, 0)
            # print(pygame.time.get_ticks() / 1000, self.isJumping, self.coyoteTimer, self.jumpBuffer)
            if not self.isJumping and self.jumpBuffer > 0 and self.coyoteTimer > 0:
                self.startJump()
    def startJump(self):
        self.isJumping = True
        self.isFalling = False
        self.chargeTime = 0
        self.jumpBuffer = 0
        self.coyoteTimer = 0
    def setFalling(self):
        self.isFalling = True
        self.isJumping = False
    def updateJump(self, isSpaceHeld : bool):
        if self.isJumping:
            if not self.isFalling and isSpaceHeld and self.chargeTime < self.maxJump:
                self.chargeTime += 1
                self.jumpVelocity = min(self.baseJump + (self.chargeTime / self.maxJump) * (self.maxJump - self.baseJump), self.maxJump)
            else:
                self.isFalling = True
                self.jumpVelocity -= self.gravity
        elif self.isFalling:
            self.jumpVelocity -= self.gravity
        self.jumpBuffer = max(self.jumpBuffer - 1, 0)
        self.jumpVelocity = max(self.jumpVelocity, -6 * self.baseJump)
        # print(self.jumpBuffer)
    def setJumpBuffer(self):
        self.jumpBuffer = self.jumpBufferTime
    def updateFalling(self):
        self.jumpVelocity -= self.gravity
        self.jumpVelocity = max(self.jumpVelocity, -6 * self.baseJump)
from components import Vector, Hitbox
class Entity:
    def __init__(self, hitbox : Hitbox):
        self.hitbox = hitbox.copy()
        self.velocity = Vector(0, 0)
        self.jumping = Jumping(4, 9, 0.5, 10, 15)
        self.MaxSpeed = 6
        self.flyingBuffer = 240
        self.portalBuffer = 3
        self.is_flying = False
        self.in_portal = False
        self.is_player = False
        self.is_bullet = False

    def isOnGround(self):
        down_hitbox = self.hitbox.copy() + Vector(0, 1)
        from game import Game
        if self.velocity.y < 0:
            return False
        if self.checkPortal(Vector(0, 1)):
            return False
        for block in Game.get_instance().map_manager.super_edges:
            if block.colliderect(down_hitbox):
                self.is_flying = 0
                return True
        return False
    def rotateVelocity(self, infacing : int, outfacing : int):
        from math import pi
        angle = pi / 2 * (infacing - outfacing + 4 & 3)
        self.velocity = self.velocity.rotate(angle)
        self.jumping.jumpVelocity = -self.velocity.y
    def checkPortal(self, delta : Vector):
        from game import Game
        portals = Game.get_instance().view.portals
        if portals[0].type == -1 or portals[1].type == -1:
            return False
        self.hitbox += delta
        for i in range(2):
            flag = portals[i].isMoveIn(self.hitbox)
            if flag:
                infacing = portals[i].infacing
                new_position = self.moveOutPortalPosition(portals[i ^ 1])
                if new_position == None:
                    break
                from portal import unit_direction
                if self.velocity.dot(unit_direction[infacing]) <= self.MaxSpeed * 1.2:
                    if unit_direction[infacing].x != 0:
                        self.velocity.x = unit_direction[infacing].x * self.MaxSpeed * 1.2
                    else:
                        self.velocity.y = unit_direction[infacing].y * self.MaxSpeed * 1.2
                self.rotateVelocity(infacing, portals[i ^ 1].facing)
                if portals[i ^ 1].facing & 1:
                    self.is_flying = self.flyingBuffer
                    self.facing = portals[i ^ 1].facing - 2
                self.hitbox.set_position(new_position)
                return 1 << (i ^ 1)
        self.hitbox -= delta
        return 0

    from portal import Portal
    def moveOutPortalPosition(self, portal : Portal):
        # 从碰撞箱顶点开始的offsets
        from portal import portal_width, portal_radius
        offsets = [
            Vector(0, -self.hitbox.height),
            Vector(-self.hitbox.width, 0),
            Vector(0, portal_width),
            Vector(portal_width, 0)
        ]
        new_position = portal.get_position() + offsets[portal.facing]
        if portal.facing & 1:
            new_position += Vector(0, portal_radius - 0.5 * self.hitbox.height)
        else:
            new_position += Vector(portal_radius - 0.5 * self.hitbox.width, 0)
        new_position = new_position.round()
        from game import Game
        if (Hitbox(new_position, self.hitbox.get_size()).checkHits(Game.get_instance().map_manager.super_edges)):
            return None
        self.in_portal = self.portalBuffer
        return new_position
    
    def rigidMove(self):
        flag = 0
        def moveDirection(delta : Vector, value):
            if self.checkPortal(delta):
                return False
            nonlocal flag
            self.hitbox += delta
            from game import Game
            collided = self.hitbox.checkHits(Game.get_instance().map_manager.super_edges, lambda : self.hitbox.move_ip(-delta[0], -delta[1]))
            if collided:
                flag |= 1 << value
            return not collided
        now = self.hitbox.y
        move = self.velocity.round()
        lengthX = round(abs(move.x))
        from numpy import sign
        for i in range(lengthX):
            if not moveDirection((sign(self.velocity.x), 0, 0, 0), 0):
                break
        move = self.velocity.round()
        lengthY = round(abs(move.y))
        cnt = 0
        for i in range(lengthY):
            cnt += 1
            if not moveDirection((0, sign(self.velocity.y), 0, 0), 1):
                break
        return flag
    def updateJumping(self, isSpaceHeld):

        self.jumping.canJump(self.isOnGround())
        self.jumping.updateJump(isSpaceHeld)
    def updateX(self, move):
        from math import exp, sqrt
        nextVelocityX = self.velocity.x
        # print(nextVelocityX, self.MaxSpeed)
        def sign(x):
            return -1 if x < 0 else 1
        def decelerate(now, deceleration):
            return sqrt(max(now * now - deceleration * now * now, 0)) * sign(now)
        onGround = self.isOnGround()
        if not self.is_flying and abs(self.velocity.x) <= self.MaxSpeed:
            if move == 0:
                nextVelocityX = self.velocity.x * exp(-0.5)
            else:
                nextVelocityX = move * min(sqrt(self.velocity.x * self.velocity.x + 10), self.MaxSpeed)
        else:
            if move == 0:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, (0.16) * (1 + self.is_player))
                else:
                    nextVelocityX = decelerate(self.velocity.x, (0.01) * (1 + self.is_player))
            elif move * self.velocity.x > 0:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, 0.3)
                else:
                    nextVelocityX = decelerate(self.velocity.x, 0.01)
            else:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, 0.5)
                else:
                    nextVelocityX = decelerate(self.velocity.x, 0.1)
        return nextVelocityX
    def updateXY(self, controllerX : int, controllerY : int):
        self.updateJumping(controllerY)
        self.is_flying = max(0, self.is_flying - 1)
        self.in_portal = max(0, self.in_portal - 1)
        nextVelocityY = -self.jumping.jumpVelocity
        # nextVelocityX = self.updateX(controllerX)
        nextVelocityX = self.velocity.x
        if not self.in_portal or self.jumping.jumpVelocity <= -4 * self.jumping.maxJump:
            nextVelocityX = self.updateX(controllerX)
        self.velocity.x = nextVelocityX
        self.velocity.y = nextVelocityY
        side = self.rigidMove()
        if side & 1:
            self.velocity.x = 0
            self.is_flying = 0
        if side & 2:
            self.velocity.y = 0
        if self.velocity.y == 0:
            self.jumping.jumpVelocity = 0
            self.jumping.setFalling()
    def update(self):
        self.update(0, 0)
    def check_out_of_map(self):
        from game import Game
        if not self.hitbox.colliderect(Hitbox(0, 0, Game.get_instance().screen.get_width(), Game.get_instance().screen.get_height())):
            Game.get_instance().restart()
