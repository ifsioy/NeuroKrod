
from src.game_objects.game_object import GameObject
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.utils.animations import KEY_ANIMATION


class Key(GameObject):
    def __init__(self, x, y, width, height):
        super(Key, self).__init__(x, y, width, height)
        self.render_component = AnimatedSpriteComponent({
            'idle': KEY_ANIMATION,
        }, 'idle')
