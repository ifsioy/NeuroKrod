from src.rendering.components.frame_component import FrameComponent
from src.utils.hyper_parameters import COLOR_WHITE


class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.render_component = FrameComponent(COLOR_WHITE)
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True

    def physics_update(self, dt: float):
        self.render_component.update(dt)

    def square(self):
        return self.width * self.height

    def intersection_area(self, other):
        left_a = self.x - self.width / 2
        right_a = self.x + self.width / 2
        top_a = self.y - self.height / 2
        bottom_a = self.y + self.height / 2

        left_b = other.x - other.width / 2
        right_b = other.x + other.width / 2
        top_b = other.y - other.height / 2
        bottom_b = other.y + other.height / 2

        overlap_x = max(0, min(right_a, right_b) - max(left_a, left_b))
        overlap_y = max(0, min(bottom_a, bottom_b) - max(top_a, top_b))

        return overlap_x * overlap_y
