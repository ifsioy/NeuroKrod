
from src.game_objects.game_object import GameObject
from src.game_objects.movable import Movable
from src.rendering.components.shape_component import ShapeComponent
from src.utils.hyper_parameters import COLOR_RED


class Player(Movable):
    def __init__(self, x, y, width, height, speed):
        super(Player, self).__init__(x, y, width, height, speed)
        self.render_component = ShapeComponent(COLOR_RED)
        self.keys_collected = 0

    def key_collected(self):
        self.keys_collected += 1
