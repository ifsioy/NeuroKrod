from src.game_objects.game_object import GameObject
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.utils.animations import HOLE_ANIMATION


class Hole(GameObject):
    def __init__(self, x, y, width, height):
        super(Hole, self).__init__(x, y, width, height)
        self.render_component = AnimatedSpriteComponent({
            'idle': HOLE_ANIMATION,
        }, 'idle')

