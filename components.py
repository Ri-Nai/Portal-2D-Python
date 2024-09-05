from pygame import Vector2
from pygame import Rect
class Vector(Vector2):
    def round(self):
        return Vector2(round(self.x), round(self.y))
    def get_angle(self):
        from math import atan2, pi
        return atan2(self.y, self.x) * 180 / pi
    def to_rect(self):
        return Rect(self.x, self.y, 0, 0)
    def copy(self):
        return Vector(self.x, self.y)
    def rotate(self, angle):
        from math import cos, sin
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        return Vector(x, y)
class Hitbox(Rect):
    def checkHits(self, hitboxes, operate = None) -> bool:
        for hitbox in hitboxes:
            if self.colliderect(hitbox):
                if operate != None:
                    operate()
                return True
        return False
    def get_size(self):
        return Vector(self.width, self.height)
    def get_position(self):
        return Vector(self.x, self.y)
    def get_center(self):
        return Vector(self.x + self.width / 2, self.y + self.height / 2)
    def set_position(self, position : Vector):
        self.x = position.x
        self.y = position.y
    def copy(self):
        return Hitbox(self.x, self.y, self.width, self.height)
    def contains_point(self, point : Vector) -> bool:
        return point.x >= self.x and point.x <= self.right and point.y >= self.y and point.y <= self.bottom
    def __add__(self, other):
        if type(other) == tuple:
            return Hitbox(self.x + other[0], self.y + other[1], self.width, self.height)
        return Hitbox(self.x + other.x, self.y + other.y, self.width, self.height)
    def __sub__(self, other):
        if type(other) == tuple:
            return Hitbox(self.x - other[0], self.y - other[1], self.width, self.height)
        return Hitbox(self.x - other.x, self.y - other.y, self.width, self.height)
    def __iadd__(self, other):
        if type(other) == tuple:
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other.x
            self.y += other.y
        return self
    def __isub__(self, other):
        if type(other) == tuple:
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other.x
            self.y -= other.y
        return self
def create_hitbox(left_up : Vector, right_down : Vector) -> Hitbox:
    return Hitbox(left_up.x, left_up.y, right_down.x - left_up.x, right_down.y - left_up.y)
def create_vector(dic : dict) -> Vector:
    return Vector(dic["x"], dic["y"])
