from src.game_objects.game_object import GameObject
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.utils.animations import GATES_CLOSED_ANIMATION, GATES_OPENED_ANIMATION


class Gates(GameObject):
    def __init__(self, x, y, width, height):
        super(Gates, self).__init__(x, y, width, height)
        self.opened = False
        self.render_component = AnimatedSpriteComponent({
            'closed': GATES_CLOSED_ANIMATION,
            'opened': GATES_OPENED_ANIMATION,
        }, 'closed')

    def physics_update(self, dt: float):
        if self.opened:
            self.render_component.play('opened')