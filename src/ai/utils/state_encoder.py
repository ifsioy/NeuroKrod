import math
from datetime import datetime, timedelta

import torch

from src.ai.utils.config import DQNConfig
from src.core.grid.grid_manager import GridManager
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.gates import Gates
from src.game_objects.hole import Hole
from src.game_objects.key import Key
from src.game_objects.player import Player
from src.game_objects.wall import Wall
from src.utils.hyper_parameters import AREA_WIDTH, AREA_HEIGHT, MAZE_SIZE, CELL_WIDTH


class StateEncoder:
    def __init__(self, grid_manager: GridManager):
        self.grid_manager = grid_manager

    def encode(self, target: GameObject):
        # cells = self.grid_manager.get_cells_in_area(target, AREA_WIDTH, AREA_HEIGHT)
        #
        # cur_time = datetime.now()
        # player_smell = []
        # enemy_smell = []
        # for cell in cells:
        #     enemy_smell.append(cell.last_enemy_visit)
        #     player_smell.append(cell.last_player_visit)
        #
        # for i in range(len(player_smell)):
        #     player_smell[i] = math.log(1 + timedelta.total_seconds(cur_time - player_smell[i]))
        #     enemy_smell[i] = math.log(1 + timedelta.total_seconds(cur_time - enemy_smell[i]))
        #
        # max_smell = max(max(player_smell), max(enemy_smell))
        #
        # for i in range(len(player_smell)):
        #     player_smell[i] = 1 - (player_smell[i] / max_smell)
        #     enemy_smell[i] = 1 - (enemy_smell[i] / max_smell)
        #
        # objects = [Player, Enemy, Gates, Hole, Key, Wall]
        # state = []
        # for i in range(len(player_smell)):
        #     for obj_type in objects:
        #         if obj_type not in cells[i].objects.keys():
        #             state.extend([0, 0, 0, 0, 0])
        #         else:
        #             x_offset, y_offset = self.grid_manager.get_object_offset(cells[i].objects[obj_type])
        #             state.extend([1, x_offset, y_offset, player_smell[i], enemy_smell[i]])

        cells = self.grid_manager.get_cells_in_area(target, AREA_WIDTH, AREA_HEIGHT)

        px, py, ex, ey = 0, 0, 0, 0

        for cell in cells:
            for obj in cell.objects.values():
                if type(obj) is Player:
                    px, py = obj.x, obj.y
                elif type(obj) is Enemy:
                    ex, ey = obj.x, obj.y

        state = [px, py, ex, ey]

        for i in range(len(state)):
            state[i] /= MAZE_SIZE * CELL_WIDTH


        return torch.tensor(state, dtype=torch.float32)
