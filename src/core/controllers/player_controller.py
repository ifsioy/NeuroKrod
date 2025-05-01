import math
import pygame

from src.core.controllers.base_controller import BaseController


class PlayerController(BaseController):
    def __init__(self, player, keys: dict = None):
        super().__init__()
        self.player = player
        self.keys = keys or {
            'up':    [pygame.K_w, pygame.K_UP],
            'down':  [pygame.K_s, pygame.K_DOWN],
            'left':  [pygame.K_a, pygame.K_LEFT],
            'right': [pygame.K_d, pygame.K_RIGHT],
        }

        self.velocity = [0, 0]


    def handle_input(self, events):
        pressed = pygame.key.get_pressed()

        self.velocity = [0, 0]

        if any(pressed[key] for key in self.keys['up']):
            self.velocity[1] -= 1

        if any(pressed[key] for key in self.keys['down']):
            self.velocity[1] += 1

        if any(pressed[key] for key in self.keys['left']):
            self.velocity[0] -= 1

        if any(pressed[key] for key in self.keys['right']):
            self.velocity[0] += 1

        cur_speed = 1
        if self.velocity[0] != 0 and self.velocity[1] != 0:
            cur_speed /= math.sqrt(2)

        self.velocity[0] *= cur_speed
        self.velocity[1] *= cur_speed
        self.update()


    def update(self):
        self.player.update_velocity(self.velocity)

