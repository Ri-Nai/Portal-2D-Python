from components import *
from game import basic_size

GLaDOS_X = 4 * basic_size
GLaDOS_Y = 8 * basic_size
picture_size_y = 287 * 2
blood_limit = 120


class GLaDOS(Hitbox):
    def __init__(self, still_alive = False):
        super().__init__(
            16 * basic_size - GLaDOS_X / 2,
            9 * basic_size - GLaDOS_Y / 2,
            GLaDOS_X,
            GLaDOS_Y,
        )
        self.stillAlive = still_alive
        self.shootingBuffetTime = 60
        self.movingBufferTime = 600
        self.tragetPosition = self.get_position()
        self.shootingBuffer = self.shootingBuffetTime * 2
        self.movingBuffer = self.movingBufferTime
        self.blood = blood_limit
        from bullet import Bullet
        self.bullets : list[Bullet] = []
        self.shootingStyle = 3
        self.shootingFormat = [
            self.shootingTrack,
            self.shootingRound,
            self.shootingRect,
            self.shootingFlower,
        ]
        self.baseAngle = 0

    def draw(self):
        if not self.stillAlive:
            return
        from game import Game

        texture = Game.get_instance().texture_manager.get_texture("GLaDOS")
        # Game.get_instance().draw_image(texture, self, (0, picture_size_y), (self.width, self.height))
        Game.get_instance().draw_image(
            texture,
            Hitbox(
                self.x,
                self.y - picture_size_y + self.height,
                self.width,
                picture_size_y,
            ),
        )
        for i in self.bullets:
            i.draw()

    def update(self):
        # print(self.stillAlive)
        if not self.stillAlive:
            return
        from random import uniform
        from player import player_size
        # print(self.movingBuffer)
        self.movingBuffer = max(0, self.movingBuffer - uniform(1, 1.5))
        if self.movingBuffer == 0:
            self.tragetPosition = Vector(
                uniform(0, 30 * basic_size - GLaDOS_X),
                uniform(0, 16 * basic_size - GLaDOS_Y - player_size.y - 100),
            ) + Vector(1 * basic_size, 1 * basic_size)
            self.movingBuffer = self.movingBufferTime
            self.shootingStyle = int(uniform(0, len(self.shootingFormat)))
        self.shootingBuffer = max(0, self.shootingBuffer - uniform(1, 1.5))
        if self.shootingBuffer == 0:
            self.shootingFormat[self.shootingStyle]()
            self.shootingBuffer = self.shootingBuffetTime
        self += (self.tragetPosition - self.get_position()) * uniform(0.1, 0.5) * uniform(0.2, 0.5) * uniform(0.3, 0.5)
        for i in self.bullets:
            i.update()
        # print(len(self.bullets))
        self.bullets = [i for i in self.bullets if not i.destroyed]

    def shootingTrack(self):
        from game import Game
        player = Game.get_instance().view.player
        from random import uniform
        width = uniform(0, 100) + GLaDOS_X
        height = uniform(0, 100) + GLaDOS_Y
        left = self.get_center().x - width / 2
        top = self.get_center().y - height / 2
        right = self.get_center().x + width / 2
        bottom = self.get_center().y + height / 2
        bulletNumber = int(uniform(10, 30))
        for i in range(bulletNumber):
            new_position = Vector(
                uniform(left, right),
                uniform(top, bottom),
            )
            direction = player.hitbox.get_center() - new_position
            velocity = direction.normalize() * uniform(0.5, 5)
            from bullet import Bullet
            self.bullets.append(Bullet(new_position, velocity, 3))
    def shootingRound(self):
        from random import uniform
        from math import radians, cos, sin

        # 初始化变量
        radius = uniform(100, 200)
        space = uniform(5, 10)  # 减小间隔以生成更平滑的弧形
        l = radians(uniform(-270, -150))  # 角度转换为弧度
        r = radians(uniform(-30, 90))  # 角度转换为弧度
        
        while l < r:
            # 计算方向向量
            direction = Vector(cos(l) * radius, -sin(l) * radius)
            velocity = direction.normalize() * 10  # 直接规范化并缩放速度
            
            from bullet import Bullet
            # 创建弹幕并添加到列表中
            new_position = self.get_center() + direction
            self.bullets.append(Bullet(new_position, velocity, 3))
            l += radians(space)  # 增加弧度间隔
    def shootingRect(self):
        from random import uniform
        width = uniform(0, 100) + GLaDOS_X
        height = uniform(0, 100) + GLaDOS_Y
        left = self.get_center().x - width / 2
        top = self.get_center().y - height / 2
        right = self.get_center().x + width / 2
        bottom = self.get_center().y + height / 2
        space = uniform(10, 30)
        velocity = uniform(3, 5)
        if uniform(0, 1) < 0.2:
            velocity = -velocity
        for i in range(int(left), int(right), int(space)):
            from bullet import Bullet
            self.bullets.append(Bullet(Vector(i, top), Vector(0, -velocity), 3))
            self.bullets.append(Bullet(Vector(i, bottom), Vector(0, velocity), 3))
        for i in range(int(top), int(bottom), int(space)):
            from bullet import Bullet
            self.bullets.append(Bullet(Vector(left, i), Vector(velocity, 0), 3))
            self.bullets.append(Bullet(Vector(right, i), Vector(-velocity, 0), 3))
    def shootingFlower(self):
        center = self.get_center()
        from random import uniform
        numBullets = int(uniform(36, 36 + 20))
        angle_step = 27
        # baseAngle = 0
        angleOffset = uniform(0, 360)
        for i in range(1, numBullets + 1):
            angle = angleOffset + self.baseAngle + i * angle_step
            radius = i * 2
            direction = Vector(COS(angle), -SIN(angle)) * radius
            velocity = direction.normalize() * (radius / 10) * (1 + i / 100)
            from bullet import Bullet
            self.bullets.append(Bullet(center + direction, velocity, 3))
        self.baseAngle += angle_step * uniform(0.8, 1.2)
def COS(angle: float):
    import math
    return math.cos(angle * math.pi / 180)
def SIN(angle: float):
    import math
    return math.sin(angle * math.pi / 180)
