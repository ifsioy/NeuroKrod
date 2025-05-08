import math
import random

from src.core.controllers.ai_controller import AIController
from src.game_objects.enemy import Enemy


class EnemyController(AIController):
    def __init__(self, enemy: Enemy):
        super().__init__()
        self.enemy = enemy
        self.velocity = [0, 0]

    def handle_input(self, events):
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
        self.enemy.update_velocity(self.velocity)