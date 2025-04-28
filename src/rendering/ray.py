import math


class Ray:
    __slots__ = (
    'angle', 'x', 'y', 'dx', 'dy', 'inv_dx', 'inv_dy', 'dx_zero', 'dy_zero', 'length', 'bumpedType')  # Memory optimization

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.dx_zero = abs(self.dx) < 1e-9
        self.dy_zero = abs(self.dy) < 1e-9
        self.inv_dx = 1.0 / self.dx if not self.dx_zero else 0
        self.inv_dy = 1.0 / self.dy if not self.dy_zero else 0
        self.length = 1e9
        self.bumpedType = None