
from src.game_objects.game_object import GameObject
from src.game_objects.movable import Movable
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.rendering.components.shape_component import ShapeComponent
from src.rendering.sprite_loader import SpriteLoader
from src.utils.hyper_parameters import COLOR_RED, ASSETS_DIR


class Player(Movable):
    def __init__(self, x, y, width, height, speed):
        super(Player, self).__init__(x, y, width, height, speed)
        self.keys_collected = 0
        idle = SpriteLoader.load_animation(ASSETS_DIR / 'player' / 'idle', width, height)
        run = SpriteLoader.load_animation(ASSETS_DIR / 'player' / 'run', width, height)
        self.render_component = AnimatedSpriteComponent({
            'idle': idle,
            'run': run
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
