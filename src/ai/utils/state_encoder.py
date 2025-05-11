import math
from datetime import datetime, timedelta

from src.ai.utils.config import DQNConfig
from src.core.grid.grid_manager import GridManager
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.gates import Gates
from src.game_objects.hole import Hole
from src.game_objects.key import Key
from src.game_objects.player import Player
from src.game_objects.wall import Wall
from src.utils.hyper_parameters import AREA_WIDTH, AREA_HEIGHT


class StateEncoder:
    def __init__(self, grid_manager: GridManager):
        self.grid_manager = grid_manager

    def encode(self, target: GameObject):
        cells = self.grid_manager.get_cells_in_area(target, AREA_WIDTH, AREA_HEIGHT)

        cur_time = datetime.now()
        smell = []
        for cell in cells:
            if type(target) is Player:
                smell.append(cell.last_enemy_visit)
            else:
                smell.append(cell.last_player_visit)

        for i in range(len(smell)):
            smell[i] = math.log(timedelta.total_seconds(cur_time - smell[i]))

        max_smell = max(smell)

        for i in range(len(smell)):
            smell[i] = 1 - (smell[i] / max_smell)

        objects = [Player, Enemy, Gates, Hole, Key, Wall]
        state = []
        for i in range(len(smell)):
            for obj_type in objects:
                if obj_type not in cells[i].objects.keys():
                    state.extend([0, 0, 0, 0])
                else:
                    x_offset, y_offset = self.grid_manager.get_object_offset(cells[i].objects[obj_type])
                    state.extend([1, x_offset, y_offset, smell[i]])

        return state
