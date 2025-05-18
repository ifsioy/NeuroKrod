from datetime import datetime, timedelta
from typing import Dict, Type

from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.player import Player
from src.utils.hyper_parameters import CELL_GRID, CELL_WIDTH, CELL_HEIGHT


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.objects: Dict[Type, GameObject] = {}
        smell = datetime.now() - timedelta(hours=5)
        self.last_player_visit = [[smell for _ in range(CELL_GRID)] for _ in range(CELL_GRID)]
        self.last_enemy_visit = [[smell for _ in range(CELL_GRID)] for _ in range(CELL_GRID)]

    def add_object(self, obj: GameObject) -> bool:
        obj_type = type(obj)
        if obj_type in self.objects:
            return False
        self.objects[obj_type] = obj
        if obj_type == Player:
            self.on_player_enter(obj)
        if obj_type == Enemy:
            self.on_enemy_enter(obj)
        return True

    def remove_object(self, obj: GameObject) -> bool:
        obj_type = type(obj)
        if obj_type not in self.objects:
            return False
        del self.objects[obj_type]
        return True

    def contains(self, obj_type: Type) -> bool:
        return obj_type in self.objects

    def get_object(self, obj_type: Type) -> GameObject:
        return self.objects[obj_type]

    def get_pos_in_cell(self, obj: GameObject) -> tuple:
        cell_x = (obj.x + CELL_WIDTH / 2 - self.x * CELL_WIDTH) / (CELL_WIDTH / CELL_GRID)
        cell_y = (obj.y + CELL_HEIGHT / 2 - self.y * CELL_HEIGHT) / (CELL_HEIGHT / CELL_GRID)
        cell_x = int(cell_x)
        cell_y = int(cell_y)
        return cell_x, cell_y

    def on_player_enter(self, obj: GameObject):
        cell_x, cell_y = self.get_pos_in_cell(obj)
        self.last_player_visit[cell_x][cell_y] = datetime.now()

    def on_enemy_enter(self, obj: GameObject):
        cell_x, cell_y = self.get_pos_in_cell(obj)
        self.last_enemy_visit[cell_x][cell_y] = datetime.now()

    