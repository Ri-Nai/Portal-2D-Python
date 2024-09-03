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
        return Vector(self.centerx, self.centery)

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
def create_hitbox(left_up : Vector, right_down : Vector) -> Hitbox:
    return Hitbox(left_up.x, left_up.y, right_down.x - left_up.x, right_down.y - left_up.y)
