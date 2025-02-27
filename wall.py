import pygame

from game_object import GameObject

class Wall(GameObject):
    def draw(self, screen, camera):
        pygame.draw.rect(screen, pygame.Color('blue'),
                     pygame.Rect(camera.apply(self)))
