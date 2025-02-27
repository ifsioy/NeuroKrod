import math

import pygame

from HyperParameters import BASE_SIZE, W_SHIFT, H_SHIFT


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = 0
        self.bumpedType = Ray

    def ray_rectangle_intersection(self, rect):
        rect_left = rect.x - rect.width / 2
        rect_right = rect.x + rect.width / 2
        rect_bottom = rect.y - rect.height / 2
        rect_top = rect.y + rect.height / 2

        if (rect_left <= self.x <= rect_right) and (rect_bottom <= self.y <= rect_top):
            return 0.0

        intersections = []

        cos_angle = math.cos(self.angle)
        if not math.isclose(cos_angle, 0, abs_tol=1e-9):
            t_left = (rect_left - self.x) / cos_angle
            if t_left >= 0:
                y = self.y + math.sin(self.angle) * t_left
                if rect_bottom <= y <= rect_top:
                    intersections.append(t_left)

            t_right = (rect_right - self.x) / cos_angle
            if t_right >= 0:
                y = self.y + math.sin(self.angle) * t_right
                if rect_bottom <= y <= rect_top:
                    intersections.append(t_right)

        sin_angle = math.sin(self.angle)
        if not math.isclose(sin_angle, 0, abs_tol=1e-9):
            t_bottom = (rect_bottom - self.y) / sin_angle
            if t_bottom >= 0:
                x = self.x + math.cos(self.angle) * t_bottom
                if rect_left <= x <= rect_right:
                    intersections.append(t_bottom)

            t_top = (rect_top - self.y) / sin_angle
            if t_top >= 0:
                x = self.x + math.cos(self.angle) * t_top
                if rect_left <= x <= rect_right:
                    intersections.append(t_top)

        return min(intersections) if intersections else None

    def draw(self, screen, camera):
        end_x = self.x + self.length * math.cos(self.angle)
        end_y = self.y + self.length * math.sin(self.angle)

        pygame.draw.line(screen, pygame.Color('white'),
                         (W_SHIFT + (self.x - camera.x) * BASE_SIZE, H_SHIFT + (self.y - camera.y) * BASE_SIZE),
                         (W_SHIFT + (end_x - camera.x) * BASE_SIZE, H_SHIFT + (end_y - camera.y) * BASE_SIZE),
                          int(BASE_SIZE / 5))