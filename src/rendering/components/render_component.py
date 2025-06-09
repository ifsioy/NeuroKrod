import pygame

from src.utils.constants import W_SHIFT


class RenderComponent:
    Z_ORDER = 0

    def draw(self, screen: pygame.Surface, position: tuple):
        pass

    def update(self, dt: float):
        pass