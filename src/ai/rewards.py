import random


from src.ai.utils.logs import Logs
from src.ai.utils.state_encoder import StateEncoder
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.movable import Movable
from src.game_objects.player import Player
from src.game_objects.wall import Wall
from src.utils.constants import CAUGHT_EVENT, WIN_EVENT, KEY_COLLECTED_EVENT, TRAINING_DT, MAZE_SIZE, HOLE_USED_EVENT


class RewardTracker:
    def __init__(self):
        self.last_distance = None

    def calculate_rewards(self, player: Movable, enemy: Movable, events, state_encoder: StateEncoder) -> tuple:
        player_reward = 1e-2
        enemy_reward = -1e-2

        for cell in state_encoder.grid_manager.get_all_cells():
            cell.dir = None
        state_encoder.get_dijkstra_path(player)

        prev_x, prev_y = enemy.x, enemy.y
        prev_x, prev_y = state_encoder.grid_manager.world_to_grid(prev_x, prev_y)
        prev_cell = state_encoder.grid_manager.get_cell(prev_x, prev_y)

        if abs(enemy.prev_x - enemy.x) + abs(enemy.prev_y - enemy.y) > 0:
            if prev_cell.dir[0] == 1:
                enemy_reward -= 5e-2 * enemy.velocity[1]
            if prev_cell.dir[1] == 1:
                enemy_reward += 5e-2 * enemy.velocity[1]
            if prev_cell.dir[2] == 1:
                enemy_reward -= 5e-2 * enemy.velocity[0]
            if prev_cell.dir[3] == 1:
                enemy_reward += 5e-2 * enemy.velocity[0]


        # current_distance = self._calculate_distance(player, enemy)
        # if self.last_distance is not None:
        #     Logs.max_rast = max(Logs.max_rast, abs(self.last_distance - current_distance))
        #     enemy_reward += 1e-5 * (self.last_distance - current_distance)
        #     player_reward -= 1e-5 * (self.last_distance - current_distance)
        # self.last_distance = current_distance

        for event in events:
            if event.type == CAUGHT_EVENT:
                player_reward -= 1
                enemy_reward += 1
            if event.type == WIN_EVENT:
                player_reward += 1
                enemy_reward -= 1
            if event.type == KEY_COLLECTED_EVENT:
                player_reward += 0.5
                enemy_reward -= 0.1
            if event.type == HOLE_USED_EVENT:
                player_reward += 0.3
                enemy_reward -= 0.1

        return player_reward, enemy_reward

    @staticmethod
    def _calculate_distance(obj1: GameObject, obj2: GameObject):
        return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5