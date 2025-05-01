from src.game_objects.game_object import GameObject
from src.rendering.components.shape_component import ShapeComponent
from src.utils.hyper_parameters import COLOR_PURPLE


class Gates(GameObject):
    def __init__(self, x, y, width, height):
        super(Gates, self).__init__(x, y, width, height)
        self.opened = False
        self.render_component = ShapeComponent(COLOR_PURPLE)