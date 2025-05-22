import pygame

from src.rendering.components.animation import AnimationData, AnimationController
from src.rendering.components.render_component import RenderComponent


class AnimatedSpriteComponent(RenderComponent):
    def __init__(self, animations: dict[str, AnimationData], default_state: str):
        self.animations = animations
        self.controller = AnimationController()
        self.controller.play(self.animations[default_state])
        self.flipped = False

    def play(self, state: str):
        self.controller.play(self.animations[state])

    def update(self, dt: float):
        self.controller.update(dt)

    def draw(self, screen: pygame.Surface, position: tuple):
        frame = self.controller.get_current_frame()
        if self.flipped:
            frame = pygame.transform.flip(frame, 1, 0)
        if frame:
            rect = pygame.Rect(position)
            screen.blit(frame, rect)