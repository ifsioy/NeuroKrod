import random

import pygame

from src.ai.utils.logs import Logs
from src.game_objects.game_object import GameObject
from src.game_objects.movable import Movable
from src.utils.hyper_parameters import CAUGHT_EVENT, WIN_EVENT, KEY_COLLECTED_EVENT


class RewardTracker:
    def __init__(self):
        self.last_distance = None

    def calculate_rewards(self, player: Movable, enemy: Movable, events) -> tuple:
        player_reward = 0.025
        enemy_reward = -0.025

        if random.random() < 0.001:
            print(Logs.max_rast)

        current_distance = self._calculate_distance(player, enemy)
        if self.last_distance is not None:
            Logs.max_rast = max(Logs.max_rast, abs(self.last_distance - current_distance))
            enemy_reward += 0.001 * (self.last_distance - current_distance)
            player_reward -= 0.001 * (self.last_distance - current_distance)
        self.last_distance = current_distance

        for event in events:
            if event.type == CAUGHT_EVENT:
                player_reward -= 25
                enemy_reward += 25
            if event.type == WIN_EVENT:
                player_reward += 25
                enemy_reward -= 25
            if event.type == KEY_COLLECTED_EVENT:
                player_reward += 5
                enemy_reward -= 2.5

        return player_reward, enemy_reward

    @staticmethod
    def _calculate_distance(obj1: GameObject, obj2: GameObject):
        return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5