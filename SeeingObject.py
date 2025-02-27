import math

from GameObject import GameObject
from HyperParameters import RAYS_NUMBER, CELL_HEIGHT
from Ray import Ray

class SeeingObject(GameObject):
    def __init__(self, x, y, width, height):
        super(SeeingObject, self).__init__(x, y, width, height)
        self.rays = list()
        for i in range(RAYS_NUMBER):
            self.rays.append(Ray(self.x, self.y, math.radians(360 / RAYS_NUMBER * i)))

    def let_rays(self, items):
        for ray in self.rays:
            ray.x = self.x
            ray.y = self.y
            ray.length = 1e9
            ray.bumpedType = None
            for item in items:
                if item == self:
                    continue
                distance = ray.ray_rectangle_intersection(item)
                if distance is not None and distance < ray.length:
                    ray.length = distance
                    ray.bumpedType = type(item)

    def update(self, screen, camera, items):
        self.let_rays(items)
        for ray in self.rays:
            ray.draw(screen, camera)


