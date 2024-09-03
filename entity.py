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
        # print(self.jumpBuffer)
    def setJumpBuffer(self):
        self.jumpBuffer = self.jumpBufferTime
    def updateFalling(self):
        self.jumpVelocity -= self.gravity
        self.jumpVelocity = max(self.jumpVelocity, -6 * self.baseJump)
from components import Vector, Hitbox
class Entity:
    def __init__(self, hitbox : Hitbox) -> None:
        self.hitbox = hitbox.copy()
        self.velocity = Vector(0, 0)
        self.jumping = Jumping(4, 9, 0.5, 10, 15)
        self.MaxSpeed = 6
        self.isflying = False
    def isOnGround(self):
        down_hitbox = self.hitbox.copy() + (0, 1)
        from game import Game
        for block in Game.get_instance().map_manager.super_edges:
            if block.colliderect(down_hitbox):
                return True
        return False
    def rigidMove(self):
        flag = 0
        def moveDirection(delta, value):
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
        from math import exp, sqrt, copysign
        nextVelocityX = self.velocity.x
        def decelerate(now, deceleration):
            return sqrt(max(now * now - deceleration * now * now, 0)) * copysign(now)
        onGround = self.isOnGround()
        if not self.isflying and abs(self.velocity.x) <= self.MaxSpeed:
            if move == 0:
                nextVelocityX = self.velocity.x * exp(-0.5)
            else:
                nextVelocityX = move * min(sqrt(self.velocity.x * self.velocity.x + 10), self.MaxSpeed)
        else:
            if move == 0:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, (0.16) * (2))
                else:
                    nextVelocityX = decelerate(self.velocity.x, (0.01) * (2))
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
    def updateXY(self, controllerX, controllerY):
        self.updateJumping(controllerY)
        nextVelocityY = -self.jumping.jumpVelocity
        nextVelocityX = self.updateX(controllerX)
        self.velocity.x = nextVelocityX
        self.velocity.y = nextVelocityY
        side = self.rigidMove()
        if side & 1:
            self.velocity.x = 0
        if side & 2:
            self.velocity.y = 0
        if self.velocity.y == 0:
            self.jumping.jumpVelocity = 0
            self.jumping.setFalling()
    def update(self):
        self.update(0, 0)
