from components import *
from game import basic_size

GLaDOS_X = 4 * basic_size
GLaDOS_Y = 8 * basic_size
picture_size_y = 287 * 2
blood_limit = 120


class GLaDOS(Hitbox):
    def __init__(self, still_alive=False):
        super().__init__(
            16 * basic_size - GLaDOS_X / 2,
            9 * basic_size - GLaDOS_Y / 2,
            GLaDOS_X,
            GLaDOS_Y,
        )
        self.still_alive = still_alive
        self.shootingBuffetTime = 60
        self.movingBufferTime = 600
        self.tragetPosition = self.get_position()
        self.shootingBuffer = self.shootingBuffetTime * 2
        self.movingBuffer = self.movingBufferTime
        self.blood = blood_limit
        from Entities.bullet import Bullet

        self.bullets: list[Bullet] = []
        self.shootingStyle = 3
        self.shootingFormat = [
            self.shootingTrack,
            self.shootingRound,
            self.shootingRect,
            self.shootingFlower,
        ]
        self.base_angle = 0

    def draw(self):
        if not self.still_alive:
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
        # print(self.still_alive)
        if not self.still_alive:
            return

        from Entities.player import player_size

        # print(self.movingBuffer)
        self.movingBuffer = max(0, self.movingBuffer - RANDOM(1, 1.5))

        if self.movingBuffer == 0:
            self.tragetPosition = Vector(
                RANDOM(0, 30 * basic_size - GLaDOS_X),
                RANDOM(0, 16 * basic_size - GLaDOS_Y - player_size.y - 100),
            ) + Vector(1 * basic_size, 1 * basic_size)
            self.movingBuffer = self.movingBufferTime
            self.shootingStyle = int(RANDOM(0, len(self.shootingFormat)))

        self.shootingBuffer = max(0, self.shootingBuffer - RANDOM(1, 1.5))
        if self.shootingBuffer == 0:
            self.shootingFormat[self.shootingStyle]()
            self.shootingBuffer = self.shootingBuffetTime

        self += (
            (self.tragetPosition - self.get_position())
            * RANDOM(0.1, 0.5)
            * RANDOM(0.2, 0.5)
            * RANDOM(0.3, 0.5)
        )
        for i in self.bullets:
            i.update()
        # print(len(self.bullets))
        self.bullets = [i for i in self.bullets if not i.destroyed]
        if self.blood <= 0:
            self.still_alive = False
            from game import Game
            Game.get_instance().switch_view("over.json")

    def shootingTrack(self):
        from game import Game

        player = Game.get_instance().view.player

        width = RANDOM(0, 100) + GLaDOS_X
        height = RANDOM(0, 100) + GLaDOS_Y
        left = self.get_center().x - width / 2
        top = self.get_center().y - height / 2
        right = self.get_center().x + width / 2
        bottom = self.get_center().y + height / 2
        bulletNumber = int(RANDOM(10, 30))
        for i in range(bulletNumber):
            new_position = Vector(
                RANDOM(left, right),
                RANDOM(top, bottom),
            )
            direction = player.hitbox.get_center() + new_position.scale(-1)
            velocity = direction.normalize().scale(RANDOM(1, 5))
            print(direction.normalize())
            from Entities.bullet import Bullet

            self.bullets.append(Bullet(new_position, velocity, 3))

    def shootingRound(self):

        from math import radians, cos, sin

        # 初始化变量
        radius = RANDOM(100, 200)
        space = RANDOM(5, 10)  # 减小间隔以生成更平滑的弧形
        l = radians(RANDOM(-270, -150))  # 角度转换为弧度
        r = radians(RANDOM(-30, 90))  # 角度转换为弧度
        while l < r:
            # 计算方向向量
            direction = Vector(cos(l) * radius, -sin(l) * radius)
            velocity = direction.normalize().scale(10)  # 直接规范化并缩放速度

            from Entities.bullet import Bullet

            # 创建弹幕并添加到列表中
            print(space)
            new_position = self.get_center() + direction
            self.bullets.append(Bullet(new_position, velocity, 1))
            l += radians(space)  # 增加弧度间隔

    def shootingRect(self):

        width = RANDOM(0, 100) + GLaDOS_X
        height = RANDOM(0, 100) + GLaDOS_Y
        left = self.get_center().x - width / 2
        top = self.get_center().y - height / 2
        right = self.get_center().x + width / 2
        bottom = self.get_center().y + height / 2
        space = RANDOM(10, 30)
        velocity = RANDOM(3, 5)
        if RANDOM(0, 1) < 0.2:
            velocity = -velocity
        for i in range(int(left), int(right), int(space)):
            from Entities.bullet import Bullet

            self.bullets.append(Bullet(Vector(i, top), Vector(0, -velocity), 1))
            self.bullets.append(Bullet(Vector(i, bottom), Vector(0, velocity), 1))
        for i in range(int(top), int(bottom), int(space)):
            from Entities.bullet import Bullet

            self.bullets.append(Bullet(Vector(left, i), Vector(velocity, 0), 1))
            self.bullets.append(Bullet(Vector(right, i), Vector(-velocity, 0), 1))

    def shootingFlower(self):
        center = self.get_center()
        num_bullets = int(RANDOM(36, 36 + 20))
        angle_step = 23
        angle_offset = RANDOM(0, 360)
        for i in range(1, num_bullets + 1):
            angle = angle_offset + self.base_angle + i * angle_step
            radius = i * 2
            direction = Vector(COS(angle), -SIN(angle)).scale(radius)
            velocity = direction.scale((1 + i / 100) / radius ** 0.5 * RANDOM(0.5, 1))
            from Entities.bullet import Bullet
            self.bullets.append(Bullet(center + direction, velocity, 2))
        self.base_angle += angle_step * RANDOM(0.8, 1.2)
    def draw_blood(self):
        if not self.still_alive:
            return
        from game import Game
        # 绘制玩家和GLaDOS的血条,就红条就行了,玩家的在下,GLaDOS的在上,用红色画,没有素材
        Game.get_instance().draw_rect("white", Hitbox(640 - 200, 30, 400, 30))
        Game.get_instance().draw_rect("red", Hitbox(640 - 200, 30, 400 * self.blood / blood_limit, 30))
        player = Game.get_instance().view.player

        Game.get_instance().draw_rect("white", Hitbox(640 - 200, 660, 400, 30))
        Game.get_instance().draw_rect("red", Hitbox(640 - 200, 660, 400 * player.blood / blood_limit, 30))

def COS(angle):
    import math

    return math.cos(angle * math.pi / 180)


def SIN(angle):
    import math

    return math.sin(angle * math.pi / 180)


def RANDOM(_min, _max):
    from random import random
    return random() * (_max - _min) + _min
