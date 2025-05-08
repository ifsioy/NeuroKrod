from datetime import datetime, timedelta
from typing import Dict, Type

from src.game_objects.game_object import GameObject
from src.game_objects.player import Player


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.objects: Dict[Type, GameObject] = {}
        self.last_player_visit: datetime = datetime.now()
        self.last_player_visit -= timedelta(hours=5)

    def add_object(self, obj: GameObject) -> bool:
        obj_type = type(obj)
        if obj_type in self.objects:
            return False
        self.objects[obj_type] = obj
        if obj_type == Player:
            self.on_player_enter()
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

    def on_player_enter(self):
        self.last_player_visit = datetime.now()

    