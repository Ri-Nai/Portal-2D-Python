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
    def setJumpBuffer(self):
        self.jumpBuffer = self.jumpBufferTime
    def updateFalling(self):
        self.jumpVelocity -= self.gravity
        self.jumpVelocity = max(self.jumpVelocity, -6 * self.baseJump)
from uilts import Vector
from uilts import Hitbox
class Entity:
    def __init__(self, hitbox : Hitbox) -> None:
        self.hitbox = hitbox.copy()
        self.velocity = Vector(0, 0)
    def isOnGround(self):
        # self.hitbox.collidedictall
        down_hitbox = self.hitbox.copy() + (0, 1)
        from game import Game
        for block in Game.get_instance().map_manager.blocks:
            if block.colliderect(down_hitbox):
                return True
        return False
    def rigidMove(self):
        flag = 0
        def moveDirection(delta, value):
            nonlocal flag
            self.hitbox += delta
            from game import Game
            collided = self.hitbox.checkHits(Game.get_instance().map_manager.blocks, lambda : self.hitbox.move_ip(-delta[0], -delta[1]))
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
class Player(Entity):
    """
    position: Vector
    velocity: Vector
    jumping: jumping
    """
    
    def __init__(self, hitbox : Hitbox) -> None:
        super().__init__(hitbox)
        self.jumping = Jumping(5, 10, 0.5, 10, 1)
        self.facing = 1
        self.isSpaceHeld = False
        self.MaxSpeed = 6
        self.isflying = False
    def updateJumping(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if not self.isSpaceHeld:
                self.jumping.setJumpBuffer()
            self.isSpaceHeld = True
        else:
            self.isSpaceHeld = False
        self.jumping.canJump(self.isOnGround())
        self.jumping.updateJump(self.isSpaceHeld)
    def updateX(self):
        moveLeft = pygame.key.get_pressed()[pygame.K_a]
        moveRight = pygame.key.get_pressed()[pygame.K_d]
        move = 0
        if moveLeft:
            self.facing = move = -1
        if moveRight:
            self.facing = move = 1
        from math import exp, sqrt, copysign
        nextVelocityX = self.velocity.x
        def decelerate(now, deceleration):
            return sqrt(max(now * now - deceleration * now * now, 0)) * copysign(now);
        onGround = self.isOnGround();
        if not self.isflying and abs(self.velocity.x) <= self.MaxSpeed:
            if move == 0:
                nextVelocityX = self.velocity.x * exp(-0.5);
            else:
                nextVelocityX = move * min(sqrt(self.velocity.x * self.velocity.x + 10), self.MaxSpeed);
        else:
            if move == 0:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, (0.16) * (2));
                else:
                    nextVelocityX = decelerate(self.velocity.x, (0.01) * (2));
        
            elif move * self.velocity.x > 0:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, 0.3);
                else:
                    nextVelocityX = decelerate(self.velocity.x, 0.01);
            else:
                if onGround:
                    nextVelocityX = decelerate(self.velocity.x, 0.5);
                else:
                    nextVelocityX = decelerate(self.velocity.x, 0.1);
        return nextVelocityX
    def update(self):
        self.updateJumping()
        nextVelocityY = -self.jumping.jumpVelocity
        nextVelocityX = self.updateX()
        # let side = self.rigidMove(new Vector(nextVelocityX, nextVelocityY), deltaTime)
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
        
    def draw(self):
        from game import Game
        pygame.draw.rect(Game.get_instance().screen, "pink", self.hitbox)
