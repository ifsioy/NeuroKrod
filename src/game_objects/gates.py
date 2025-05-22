from src.game_objects.game_object import GameObject
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.rendering.components.shape_component import ShapeComponent
from src.rendering.sprite_loader import SpriteLoader
from src.utils.hyper_parameters import COLOR_PURPLE, ASSETS_DIR


class Gates(GameObject):
    def __init__(self, x, y, width, height):
        super(Gates, self).__init__(x, y, width, height)
        self.opened = False
        idle = SpriteLoader.load_animation(ASSETS_DIR / 'gates', width, height)
        self.render_component = AnimatedSpriteComponent({
            'idle': idle,
        }, 'idle')