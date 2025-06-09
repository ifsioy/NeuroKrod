import math
from datetime import datetime, timedelta
from typing import List
from queue import Queue

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
from src.utils.constants import AREA_WIDTH, AREA_HEIGHT, MAZE_SIZE, CELL_WIDTH, CELL_GRID, CELL_HEIGHT, \
    SMELL_CONST


class StateEncoder:
    def __init__(self, grid_manager: GridManager):
        self.grid_manager = grid_manager

    def get_dijkstra_path(self, target: GameObject):
        sx, sy = self.grid_manager.world_to_grid(target.x, target.y)
        self.grid_manager.get_cell(sx, sy).dir = [0, 0, 0, 0]
        q = Queue()
        q.put((sx, sy))
        while not q.empty():
            x, y = q.get()
            steps = [
                [0, 1],
                [0, -1],
                [1, 0],
                [-1, 0],
            ]

            for i in range(len(steps)):
                cx, cy = x + steps[i][0], y + steps[i][1]
                if ((cx != sx or cy != sy) and
                    0 <= cx < MAZE_SIZE and
                    0 <= cy < MAZE_SIZE and
                    not self.grid_manager.get_cell(cx, cy).contains(Wall) and
                    self.grid_manager.get_cell(cx, cy).dir is None):
                    self.grid_manager.get_cell(cx, cy).dir = [0, 0, 0, 0]
                    self.grid_manager.get_cell(cx, cy).dir[i] = 1
                    q.put((cx, cy))


    def encode(self, target: GameObject):
        cells = self.grid_manager.get_cells_in_area(target, AREA_WIDTH, AREA_HEIGHT)
        sx = cells[0].x
        sy = cells[0].y
        # sx = 1
        # sy = 1

        grid_w = AREA_WIDTH * CELL_GRID
        grid_h = AREA_HEIGHT * CELL_GRID


        key = [0.] * (grid_w * grid_h)
        hole = [0.] * (grid_w * grid_h)
        wall = [0.] * (grid_w * grid_h)
        gate = [0.] * (grid_w * grid_h)
        player = [0.] * (grid_w * grid_h)
        enemy = [0.] * (grid_w * grid_h)

        player_dir_up = []
        player_dir_down = []
        player_dir_left = []
        player_dir_right = []

        enemy_dir_up = []
        enemy_dir_down = []
        enemy_dir_left = []
        enemy_dir_right = []

        all_cells = self.grid_manager.get_all_cells()
        objects = []
        player_obj = None
        enemy_obj = None
        for cell in all_cells:
            cell.dir = None
            for obj in cell.objects.values():
                objects.append(obj)
                if type(obj) == Player:
                    player_obj = obj
                elif type(obj) == Enemy:
                    enemy_obj = obj

        if player is None or enemy is None:
            print('Slomalos')

        self.get_dijkstra_path(player_obj)

        for x in range(grid_w):
            for y in range(grid_h):
                cell_x = sx + x // CELL_GRID
                cell_y = sy + y // CELL_GRID

                if self.grid_manager.get_cell(cell_x, cell_y).dir is None:
                    player_dir_up.append(0)
                    player_dir_down.append(0)
                    player_dir_left.append(0)
                    player_dir_right.append(0)
                else:
                    player_dir_up.append(self.grid_manager.get_cell(cell_x, cell_y).dir[0])
                    player_dir_down.append(self.grid_manager.get_cell(cell_x, cell_y).dir[1])
                    player_dir_left.append(self.grid_manager.get_cell(cell_x, cell_y).dir[2])
                    player_dir_right.append(self.grid_manager.get_cell(cell_x, cell_y).dir[3])

        for cell in all_cells:
            cell.dir = None
        self.get_dijkstra_path(enemy_obj)

        for x in range(grid_w):
            for y in range(grid_h):
                cell_x = sx + x // CELL_GRID
                cell_y = sy + y // CELL_GRID

                if self.grid_manager.get_cell(cell_x, cell_y).dir is None:
                    enemy_dir_up.append(0)
                    enemy_dir_down.append(0)
                    enemy_dir_left.append(0)
                    enemy_dir_right.append(0)
                else:
                    enemy_dir_up.append(self.grid_manager.get_cell(cell_x, cell_y).dir[0])
                    enemy_dir_down.append(self.grid_manager.get_cell(cell_x, cell_y).dir[1])
                    enemy_dir_left.append(self.grid_manager.get_cell(cell_x, cell_y).dir[2])
                    enemy_dir_right.append(self.grid_manager.get_cell(cell_x, cell_y).dir[3])



        subcell_w = CELL_WIDTH / CELL_GRID
        subcell_h = CELL_HEIGHT / CELL_GRID

        area_left = sx * CELL_WIDTH - CELL_WIDTH / 2
        area_top = sy * CELL_HEIGHT - CELL_HEIGHT / 2

        for obj in objects:
            obj_left = obj.x - obj.width / 2
            obj_right = obj.x + obj.width / 2
            obj_top = obj.y - obj.height / 2
            obj_bottom = obj.y + obj.height / 2

            min_x = int(max(0, (obj_left - area_left) // subcell_w))
            max_x = int(min(grid_w - 1, (obj_right - area_left) // subcell_w))
            min_y = int(max(0, (obj_top - area_top) // subcell_h))
            max_y = int(min(grid_h - 1, (obj_bottom - area_top) // subcell_h))

            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
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

        # return (player_dir_up, player_dir_down, player_dir_left, player_dir_right,
        #          enemy_dir_up, enemy_dir_down, enemy_dir_left, enemy_dir_right,
        #          key, hole, wall, gate, player, enemy)

        state = (player_dir_up + player_dir_down + player_dir_left + player_dir_right +
                 enemy_dir_up + enemy_dir_down + enemy_dir_left + enemy_dir_right +
                 key + hole + wall + gate + player + enemy)
        return torch.tensor(state, dtype=torch.float32).reshape(14, AREA_WIDTH * CELL_GRID, AREA_HEIGHT * CELL_GRID)
