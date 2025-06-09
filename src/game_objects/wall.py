from src.game_objects.game_object import GameObject
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.utils.animations import WALL_ANIMATION


class Wall(GameObject):
    def __init__(self, x, y, width, height):
        super(Wall, self).__init__(x, y, width, height)
        self.render_component = AnimatedSpriteComponent({
            'idle': WALL_ANIMATION,
        }, 'idle')

