import pygame

from HyperParameters import WHITE

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides(self, another):
        if (self == another or
            self.x - self.width / 2 >= another.x + another.width / 2 or
            self.x + self.width / 2 <= another.x - another.width / 2 or
            self.y - self.height / 2 >= another.y + another.height / 2 or
            self.y + self.height / 2 <= another.y - another.height / 2):
            return False
        return True

    def collision_check(self, another):
        if not self.collides(another):
            return False
        to_l = abs(another.x + another.width / 2 - self.x + self.width / 2)
        to_r = abs(self.x + self.width / 2 - another.x + another.width / 2)
        to_u = abs(self.y + self.height / 2 - another.y + another.height / 2)
        to_d = abs(another.y + another.height / 2 - self.y + self.height / 2)
        if min(to_l, to_r) < min(to_u, to_d):
            if to_l < to_r:
                another.x -= to_l
            else:
                another.x += to_r
        else:
            if to_d < to_u:
                another.y -= to_d
            else:
                another.y += to_u
        return True

    def update(self, screen, camera, items):
        self.draw(screen, camera)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, WHITE, pygame.Rect(camera.apply(self)))
