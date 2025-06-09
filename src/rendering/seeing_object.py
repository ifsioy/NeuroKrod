import time

import pygame

from src.game_objects.game_object import GameObject
from src.rendering.ray import Ray
from src.utils.constants import RAYS_NUMBER, W_SHIFT, BASE_SIZE, H_SHIFT, CELL_WIDTH

import math


class SeeingObject(GameObject):
    __slots__ = ('rays', 'cast_cooldown', 'next_cast')

    def __init__(self, x, y, width, height, cast_cooldown):
        super().__init__(x, y, width, height)
        angle_step = 2 * math.pi / RAYS_NUMBER
        self.rays = [Ray(x, y, i * angle_step) for i in range(RAYS_NUMBER)]
        self.cast_cooldown = cast_cooldown / 1000
        self.next_cast = 0.0

    def cast_rays(self, items):
        now = time.time()
        if now < self.next_cast:
            return
        self.next_cast = now + self.cast_cooldown

        ox, oy = self.x, self.y
        items = [item for item in items if item is not self]

        items.sort(key=lambda i: (i.x - ox) ** 2 + (i.y - oy) ** 2)

        item_data = [
            (
                i.x - i.width / 2,  # min_x
                i.x + i.width / 2,  # max_x
                i.y - i.height / 2,  # min_y
                i.y + i.height / 2,  # max_y
                type(i)
            ) for i in items
        ]

        for ray in self.rays:
            ray.length = 1e9
            ray.bumpedType = None
            current_min = 1e9

            dx_zero = ray.dx_zero
            dy_zero = ray.dy_zero
            inv_dx = ray.inv_dx
            inv_dy = ray.inv_dy

            for min_x, max_x, min_y, max_y, item_type in item_data:
                if current_min + CELL_WIDTH < ((min_x - ox) ** 2 + (min_y - oy) ** 2) ** 0.5:
                    break

                t_near = -math.inf
                t_far = math.inf

                if not dx_zero:
                    t1 = (min_x - ox) * inv_dx
                    t2 = (max_x - ox) * inv_dx
                    if t1 > t2: t1, t2 = t2, t1
                    t_near = max(t1, t_near)
                    t_far = min(t2, t_far)
                    if t_near > t_far or t_near > current_min:
                        continue
                elif ox < min_x or ox > max_x:
                    continue

                if not dy_zero:
                    t1 = (min_y - oy) * inv_dy
                    t2 = (max_y - oy) * inv_dy
                    if t1 > t2: t1, t2 = t2, t1
                    t_near = max(t1, t_near)
                    t_far = min(t2, t_far)
                    if t_near > t_far or t_near > current_min:
                        continue
                elif oy < min_y or oy > max_y:
                    continue

                if t_far < 0:
                    continue

                t = max(t_near, 0) if t_near >= 0 else t_far
                if t >= 0 and t < current_min:
                    current_min = t
                    ray.length = t
                    ray.bumpedType = item_type

    def update(self, items):
        self.cast_rays(items)

    def draw(self, screen, camera):
        for ray in self.rays:
            if ray.length < 1e9:
                pygame.draw.line(screen, pygame.Color('white'),
                                 (W_SHIFT + (self.x - camera.x) * BASE_SIZE, H_SHIFT + (self.y - camera.y) * BASE_SIZE),
                                 (W_SHIFT + (self.x + ray.dx * ray.length - camera.x) * BASE_SIZE, H_SHIFT +
                                 (self.y + ray.dy * ray.length - camera.y) * BASE_SIZE),
                                 int(BASE_SIZE / 5))
