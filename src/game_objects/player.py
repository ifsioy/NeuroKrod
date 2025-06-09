
from src.game_objects.movable import Movable
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.utils.animations import PLAYER_IDLE_ANIMATION, PLAYER_RUN_ANIMATION
from src.utils.constants import PLAYER_SPEED


class Player(Movable):
    def __init__(self, x, y, width, height, speed):
        super(Player, self).__init__(x, y, width, height, speed = PLAYER_SPEED)
        self.keys_collected = 0
        self.render_component = AnimatedSpriteComponent({
            'idle': PLAYER_IDLE_ANIMATION,
            'run': PLAYER_RUN_ANIMATION
        }, 'run')

    def update_velocity(self, new_velocity: list[float]):
        super().update_velocity(new_velocity)
        if self.velocity[0] > 0:
            self.render_component.flipped = True
        elif self.velocity[0] < 0:
            self.render_component.flipped = False

        if (abs(self.velocity[1]) == 0 and
            abs(self.velocity[0]) == 0):
            self.render_component.play('idle')
        else:
            self.render_component.play('run')



    def key_collected(self):
        self.keys_collected += 1
