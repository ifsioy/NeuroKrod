from src.game_objects.movable import Movable
from src.rendering.components.shape_component import ShapeComponent
from src.utils.hyper_parameters import COLOR_VIOLET


class Enemy(Movable):
    def __init__(self, x, y, width, height, speed):
        super(Enemy, self).__init__(x, y, width, height, speed)
        self.render_component = ShapeComponent(COLOR_VIOLET)
