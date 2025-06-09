import pygame

from src.game_objects.game_object import GameObject
from src.utils.constants import H_SHIFT, W_SHIFT, BASE_SIZE, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_SMOOTHNESS


class Camera:
    def __init__(self, target, width = CAMERA_WIDTH, height = CAMERA_HEIGHT, smoothness = CAMERA_SMOOTHNESS):
        self.x = target.x
        self.y = target.y
        self.target = target
        self.width = width
        self.height = height
        self.smoothness = smoothness

    def world_to_screen(self, obj: GameObject):
        return (W_SHIFT + (obj.x - self.x - obj.width / 2) * BASE_SIZE,
                H_SHIFT + (obj.y - self.y - obj.height / 2) * BASE_SIZE,
                obj.width * BASE_SIZE, obj.height * BASE_SIZE)

    def move(self, dt):
        def adjust_position(current, target_pos, size):
            if (target_pos < current - size / 2 or
                target_pos > current + size / 2):
                return (target_pos - current) * self.smoothness * dt
            return 0

        self.x += adjust_position(self.x, self.target.x, self.width)
        self.y += adjust_position(self.y, self.target.y, self.height)

    def update(self, dt):
        self.move(dt)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (W_SHIFT - self.width / 2 * BASE_SIZE,
                                                   H_SHIFT - self.height / 2 * BASE_SIZE,
                                                   self.width * BASE_SIZE, self.height * BASE_SIZE), int(BASE_SIZE))

        pygame.draw.circle(screen, (255, 255, 255), (W_SHIFT, H_SHIFT), BASE_SIZE)
