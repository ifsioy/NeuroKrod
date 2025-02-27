import pygame
from HyperParameters import H_SHIFT, W_SHIFT, BASE_SIZE


class Camera:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def apply(self, item):
        return (W_SHIFT + (item.x - self.x - item.width / 2) * BASE_SIZE,
                H_SHIFT + (item.y - self.y - item.height / 2) * BASE_SIZE,
                item.width * BASE_SIZE, item.height * BASE_SIZE)

    def move(self, target):
        def adjust_position(current, target_pos, size):
            if target_pos < current - size / 2:
                return target_pos + size / 2
            elif target_pos > current + size / 2:
                return target_pos - size / 2
            return current

        self.x = adjust_position(self.x, target.x, self.width)
        self.y = adjust_position(self.y, target.y, self.height)

    def update(self, screen, target):
        self.move(target)
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (W_SHIFT - self.width / 2 * BASE_SIZE,
                                                   H_SHIFT - self.height / 2 * BASE_SIZE,
                                                   self.width * BASE_SIZE, self.height * BASE_SIZE), int(BASE_SIZE))

        pygame.draw.circle(screen, (255, 255, 255), (W_SHIFT, H_SHIFT), BASE_SIZE)
