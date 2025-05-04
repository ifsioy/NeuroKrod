import pygame

from src.rendering.components.animation import AnimationData, AnimationController
from src.rendering.components.render_component import RenderComponent


class AnimatedSpriteComponent(RenderComponent):
    def __init__(self, animations: dict[str, AnimationData], default_state: str):
        self.animations = animations
        self.controller = AnimationController()
        self.controller.play(self.animations[default_state])

    def update(self, dt: float):
        self.controller.update(dt)

    def draw(self, screen: pygame.Surface, position: tuple):
        if not self.on_screen(screen, position):
            return
        frame = self.controller.get_current_frame()
        if frame:
            rect = pygame.Rect(position)
            screen.blit(frame, rect)