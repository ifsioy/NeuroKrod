from src.game_objects.movable import Movable
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.utils.animations import ENEMY_RUN_ANIMATION
from src.utils.constants import ENEMY_SPEED


class Enemy(Movable):
    def __init__(self, x, y, width, height, speed = ENEMY_SPEED):
        super(Enemy, self).__init__(x, y, width, height, speed)
        run = ENEMY_RUN_ANIMATION
        self.render_component = AnimatedSpriteComponent({
            'idle': run,
            'run': run
        }, 'run')

    def update_velocity(self, new_velocity: list[float]):
        super().update_velocity(new_velocity)
        if self.velocity[0] > 0:
            self.render_component.flipped = True
        else:
            self.render_component.flipped = False
