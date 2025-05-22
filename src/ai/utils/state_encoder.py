import math
from datetime import datetime, timedelta
from typing import List

import torch

from src.ai.utils.config import DQNConfig
from src.ai.utils.logs import Logs
from src.core.grid.grid_manager import GridManager
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.gates import Gates
from src.game_objects.hole import Hole
from src.game_objects.key import Key
from src.game_objects.player import Player
from src.game_objects.wall import Wall
from src.utils.hyper_parameters import AREA_WIDTH, AREA_HEIGHT, MAZE_SIZE, CELL_WIDTH, CELL_GRID, CELL_HEIGHT, \
    SMELL_CONST


class StateEncoder:
    def __init__(self, grid_manager: GridManager):
        self.grid_manager = grid_manager

    def encode(self, target: GameObject):
        cells = self.grid_manager.get_cells_in_area(target, AREA_WIDTH, AREA_HEIGHT)
        sx = cells[0].x
        sy = cells[0].y
        # sx = 1
        # sy = 1

        grid_w = AREA_WIDTH * CELL_GRID
        grid_h = AREA_HEIGHT * CELL_GRID

        pos_x = [0.] * (grid_w * grid_h)
        pos_y = [0.] * (grid_w * grid_h)

        player_smell = [0.] * (grid_w * grid_h)
        enemy_smell = [0.] * (grid_w * grid_h)
        key = [0.] * (grid_w * grid_h)
        hole = [0.] * (grid_w * grid_h)
        wall = [0.] * (grid_w * grid_h)
        gate = [0.] * (grid_w * grid_h)
        player = [0.] * (grid_w * grid_h)
        enemy = [0.] * (grid_w * grid_h)

        cur_time = datetime.now()
        for x in range(grid_w):
            for y in range(grid_h):
                cell_x = sx + x // CELL_GRID
                cell_y = sy + y // CELL_GRID
                idx = x * grid_h + y

                pos_x[idx] = x / grid_w
                pos_y[idx] = y / grid_h

                player_smell[idx] = SMELL_CONST ** timedelta.total_seconds(
                    cur_time - self.grid_manager.get_cell(cell_x, cell_y).last_player_visit[x % CELL_GRID][
                        y % CELL_GRID]
                )
                enemy_smell[idx] = SMELL_CONST ** timedelta.total_seconds(
                    cur_time - self.grid_manager.get_cell(cell_x, cell_y).last_enemy_visit[x % CELL_GRID][y % CELL_GRID]
                )

        all_cells = self.grid_manager.get_all_cells()
        objects = []
        for cell in all_cells:
            for obj in cell.objects.values():
                objects.append(obj)

        # Размер ячейки в мире
        subcell_w = CELL_WIDTH / CELL_GRID
        subcell_h = CELL_HEIGHT / CELL_GRID

        area_left = sx * CELL_WIDTH - CELL_WIDTH / 2
        area_top = sy * CELL_HEIGHT - CELL_HEIGHT / 2

        for obj in objects:
            # Границы объекта в мире
            obj_left = obj.x - obj.width / 2
            obj_right = obj.x + obj.width / 2
            obj_top = obj.y - obj.height / 2
            obj_bottom = obj.y + obj.height / 2

            # Индексы ячеек в локальной сетке, которые покрывает объект
            min_x = int(max(0, (obj_left - area_left) // subcell_w))
            max_x = int(min(grid_w - 1, (obj_right - area_left) // subcell_w))
            min_y = int(max(0, (obj_top - area_top) // subcell_h))
            max_y = int(min(grid_h - 1, (obj_bottom - area_top) // subcell_h))

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    # Мировые координаты центра этой ячейки
                    world_x = area_left + x * subcell_w + subcell_w / 2
                    world_y = area_top + y * subcell_h + subcell_h / 2
                    cur_area = GameObject(world_x, world_y, subcell_w, subcell_h)
                    area = (cur_area.intersection_area(obj) /
                            min(obj.square(), cur_area.square()))
                    idx = x * grid_h + y
                    if area > 0:
                        if type(obj) is Key:
                            key[idx] += area
                        elif type(obj) is Hole:
                            hole[idx] += area
                        elif type(obj) is Wall:
                            wall[idx] += area
                        elif type(obj) is Gates:
                            gate[idx] += area
                        elif type(obj) is Player:
                            player[idx] += area
                        elif type(obj) is Enemy:
                            enemy[idx] += area

        # return pos_x, pos_y, key, hole, wall, gate, player, enemy

        state = player_smell + enemy_smell + key + hole + wall + gate + player + enemy
        return torch.tensor(state, dtype=torch.float32).reshape(8, AREA_WIDTH * CELL_GRID, AREA_HEIGHT * CELL_GRID)
