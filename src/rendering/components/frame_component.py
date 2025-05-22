import pygame

from src.rendering.components.render_component import RenderComponent


class FrameComponent(RenderComponent):
    Z_OFFSET = 1

    def __init__(self, color: tuple):
        self.color = color

    def draw(self, screen: pygame.Surface, position: tuple):
        x, y, width, height = position
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.color, rect, 5)