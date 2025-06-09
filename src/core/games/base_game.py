from gameobjects_serializer import register_class

from src.game_objects.enemy import Enemy
from src.game_objects.gates import Gates
from src.game_objects.hole import Hole
from src.game_objects.key import Key
from src.game_objects.player import Player
from src.game_objects.wall import Wall


class BaseGame:
    def __init__(self):
        register_class(Player)
        register_class(Enemy)
        register_class(Wall)
        register_class(Key)
        register_class(Hole)
        register_class(Gates)
        self.is_running = False

    def run(self):
        pass

    def save(self, path, fmt='json'):
        pass

    def load(self, path, fmt='json'):
        pass