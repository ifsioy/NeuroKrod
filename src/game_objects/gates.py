import pygame

from src.game_objects.game_object import GameObject
from src.game_objects.player import Player
from src.utils.hyper_parameters import PURPLE, KEYS_NUMBER


class Gates(GameObject):
    def __init__(self, x, y, width, height):
        super(Gates, self).__init__(x, y, width, height)
        self.opened = False

    def collision_check(self, another):
        if not self.collides(another):
            return False

        if type(another) == Player and another.keys_collected == KEYS_NUMBER:
            print('AND NOW, THE END IS NEAR')
        return True

    def draw(self, screen, camera):
        pygame.draw.rect(screen, PURPLE, pygame.Rect(camera.apply(self)))