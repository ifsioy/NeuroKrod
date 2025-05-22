from src.game_objects.movable import Movable
from src.rendering.components.animated_sprite_component import AnimatedSpriteComponent
from src.rendering.components.shape_component import ShapeComponent
from src.rendering.sprite_loader import SpriteLoader
from src.utils.hyper_parameters import COLOR_VIOLET, ASSETS_DIR


class Enemy(Movable):
    def __init__(self, x, y, width, height, speed):
        super(Enemy, self).__init__(x, y, width, height, speed)
        run = SpriteLoader.load_animation(ASSETS_DIR / 'enemy', width, height)
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
