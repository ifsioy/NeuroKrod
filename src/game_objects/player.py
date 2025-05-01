
import pygame

from src.game_objects.game_object import GameObject
from src.utils.hyper_parameters import W_SHIFT, H_SHIFT, BASE_SIZE


class Player(GameObject):
    def __init__(self, x, y, width, height, speed):
        super(Player, self).__init__(x, y, width, height)
        self.speed = speed
        self.keys_collected = 0
        self.velocity = [0, 0]

    def update_velocity(self, new_velocity: list[float]):
        self.velocity = new_velocity

    def physics_update(self, dt: float):
        self.x += self.velocity[0] * dt * self.speed
        self.y += self.velocity[1] * dt * self.speed

    def key_collected(self):
        self.keys_collected += 1

    def draw(self, screen, camera):
        super(Player, self).draw(screen, camera)
        pygame.draw.rect(screen, pygame.Color('red'),
                         pygame.Rect(camera.apply(self)))

        pygame.draw.circle(screen, pygame.Color('white'), (W_SHIFT + (self.x - camera.x) * BASE_SIZE,
                                                           H_SHIFT + (self.y - camera.y) * BASE_SIZE), BASE_SIZE)
