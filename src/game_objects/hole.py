import pygame

from src.game_objects.game_object import GameObject
from src.rendering.components.shape_component import ShapeComponent
from src.utils.hyper_parameters import COLOR_BROWN


class Hole(GameObject):
    def __init__(self, x, y, width, height):
        super(Hole, self).__init__(x, y, width, height)
        self.render_component = ShapeComponent(COLOR_BROWN)

