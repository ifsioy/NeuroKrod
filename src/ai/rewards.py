import pygame

from src.game_objects.game_object import GameObject
from src.game_objects.movable import Movable
from src.utils.hyper_parameters import CAUGHT_EVENT, WIN_EVENT, KEY_COLLECTED_EVENT, HOLE_USED_EVENT


class RewardTracker:
    def __init__(self):
        self.last_distance = None

    def calculate_rewards(self, player: Movable, enemy: Movable, events) -> tuple:
        player_reward = -0.05
        enemy_reward = -0.1

        current_distance = self._calculate_distance(player, enemy)
        # if self.last_distance is not None:
        #     enemy_reward += 0.01 * (self.last_distance - current_distance)

        self.last_distance = current_distance

        for event in events:
            if event.type == CAUGHT_EVENT:
                player_reward -= 25
                enemy_reward += 25
            # if event.type == WIN_EVENT:
            #     player_reward += 25
            #     enemy_reward -= 25
            # if event.type == KEY_COLLECTED_EVENT:
            #     player_reward += 5
            #     enemy_reward -= 2.5

        return player_reward, enemy_reward

    @staticmethod
    def _calculate_distance(obj1: GameObject, obj2: GameObject):
        return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2