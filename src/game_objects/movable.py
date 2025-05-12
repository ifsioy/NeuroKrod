from src.game_objects.game_object import GameObject


class Movable(GameObject):
    def __init__(self, x, y, width, height, speed):
        super(Movable, self).__init__(x, y, width, height)
        self.speed = speed
        self.velocity = [0, 0]
        self.prev_x = x
        self.prev_y = y

    def update_velocity(self, new_velocity: list[float]):
        self.velocity = new_velocity

    def physics_update(self, dt: float):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.velocity[0] * dt * self.speed
        self.y += self.velocity[1] * dt * self.speed
