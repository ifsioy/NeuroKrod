import math
from datetime import datetime

from game_object import GameObject
from hyper_parameters import RAYS_NUMBER, CELL_HEIGHT, CAST_COOLDOWN
from ray import Ray

def ray_rectangle_intersection(ray, rect):
    ox, oy = ray.x, ray.y
    dx, dy = math.cos(ray.angle), math.sin(ray.angle)
    t_near = -math.inf
    t_far = math.inf

    min_x = rect.x - rect.width / 2
    min_y = rect.y - rect.height / 2
    max_x = rect.x + rect.width / 2
    max_y = rect.y + rect.height / 2

    if dx != 0:
        t1 = (min_x - ox) / dx
        t2 = (max_x - ox) / dx
        x_min, x_max = sorted((t1, t2))
        t_near, t_far = max(x_min, t_near), min(x_max, t_far)
    elif ox < min_x or ox > max_x:
        return None

    if dy != 0:
        t1 = (min_y - oy) / dy
        t2 = (max_y - oy) / dy
        y_min, y_max = sorted((t1, t2))
        t_near, t_far = max(y_min, t_near), min(y_max, t_far)
    elif oy < min_y or oy > max_y:
        return None

    if t_near > t_far or t_far < 0:
        return None

    t = t_near if t_near >= 0 else t_far
    return t if t >= 0 else None


class SeeingObject(GameObject):
    def __init__(self, x, y, width, height):
        super(SeeingObject, self).__init__(x, y, width, height)
        self.last_cast_time = datetime.now()
        self.rays = list()
        for i in range(RAYS_NUMBER):
            self.rays.append(Ray(self.x, self.y, math.radians(360 / RAYS_NUMBER * i)))

    def cast_rays(self, items):
        for ray in self.rays:
            ray.x = self.x
            ray.y = self.y
            ray.length = 1e9
            ray.bumpedType = None
            for item in items:
                if item == self:
                    continue
                distance = ray_rectangle_intersection(ray, item)
                if distance is not None and distance < ray.length:
                    ray.length = distance
                    ray.bumpedType = type(item)

    def update(self, items):
        if (datetime.now() - self.last_cast_time).total_seconds() > CAST_COOLDOWN / 1000:
            self.cast_rays(items)
            self.last_cast_time = datetime.now()

    def draw(self, screen, camera):
        for ray in self.rays:
            ray.draw(screen, camera)
