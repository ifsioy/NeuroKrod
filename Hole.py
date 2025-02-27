import pygame

from GameObject import GameObject
from HyperParameters import BROWN
from Player import Player


class Hole(GameObject):
    def __init__(self, x, y, width, height):
        super(Hole, self).__init__(x, y, width, height)
        self.used = False

    def collision_check(self, another):
        if not self.collides(another):
            return False

        if not self.used and type(another) == Player:
            self.used = True
            print('TRAVELING INTO THE DARK')
        return True

    def update(self, screen, camera, items):
        self.draw(screen, camera)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, BROWN, pygame.Rect(camera.apply(self)))

