import math
import random

from src.core.controllers.base_controller import BaseController
from src.game_objects.movable import Movable


class RandController(BaseController):
    def __init__(self, obj: Movable):
        super().__init__()
        self.obj = obj
        self.velocity = [0, 0]

    def handle(self, events):
        self.velocity = [0, 0]

        if random.randint(0, 1) == 1:
            self.velocity[1] -= 1

        if random.randint(0, 1) == 1:
            self.velocity[1] += 1

        if random.randint(0, 1) == 1:
            self.velocity[0] -= 1

        if random.randint(0, 1) == 1:
            self.velocity[0] += 1

        cur_speed = 1
        if self.velocity[0] != 0 and self.velocity[1] != 0:
            cur_speed /= math.sqrt(2)

        self.velocity[0] *= cur_speed
        self.velocity[1] *= cur_speed
        self.update()


    def update(self):
        self.obj.update_velocity(self.velocity)