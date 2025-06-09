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
        super(Movable, self).physics_update(dt)
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.velocity[0] * dt * self.speed
        self.y += self.velocity[1] * dt * self.speed

    def to_dict(self):
        return {
            "class": self.__class__.__name__,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "speed": self.speed,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['x'], d['y'], d['width'], d['height'], d['speed'])