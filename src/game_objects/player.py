
from src.game_objects.game_object import GameObject
from src.rendering.components.shape_component import ShapeComponent
from src.utils.hyper_parameters import COLOR_RED


class Player(GameObject):
    def __init__(self, x, y, width, height, speed):
        super(Player, self).__init__(x, y, width, height)
        self.render_component = ShapeComponent(COLOR_RED)
        self.speed = speed
        self.keys_collected = 0
        self.velocity = [0, 0]

    def update_velocity(self, new_velocity: list[float]):
        self.velocity = new_velocity

    def physics_update(self, dt: float):
        self.x += self.velocity[0] * dt * self.speed
        self.y += self.velocity[1] * dt * self.speed

    def key_collected(self):
        self.keys_collected += 1
