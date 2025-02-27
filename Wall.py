import pygame

from GameObject import GameObject

class Wall(GameObject):

    def update(self, screen, camera, items):
        self.draw(screen, camera)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, pygame.Color('blue'),
                     pygame.Rect(camera.apply(self)))
