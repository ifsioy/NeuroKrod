import pygame

from src.rendering.components.render_component import RenderComponent
from src.utils.hyper_parameters import COLOR_WHITE


class ShapeComponent(RenderComponent):
    Z_OFFSET = 1

    def __init__(self, color: tuple):
        self.color = color

    def draw(self, screen: pygame.Surface, pos: tuple):
        x, y, width, height = pos
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.color, rect)