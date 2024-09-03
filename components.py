from pygame import Vector2
from pygame import Rect
class Vector(Vector2):
    def round(self):
        return Vector2(round(self.x), round(self.y))
    def get_angle(self):
        from math import atan2
        return atan2(self.y, self.x)
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
