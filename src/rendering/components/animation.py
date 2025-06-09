from dataclasses import dataclass

import pygame

from src.utils.constants import FRAME_DURATION


@dataclass
class AnimationData:
    frames: list[pygame.Surface]
    frame_duration: float = FRAME_DURATION
    loop: bool = True

class AnimationController:
    def __init__(self):
        self.current_animation: AnimationData = None
        self.current_frame:int = 0
        self.timer:float = 0

    def play(self, animation: AnimationData):
        if self.current_animation != animation:
            self.current_animation = animation
            self.current_frame = 0
            self.timer = 0

    def update(self, dt: float):
        if self.current_animation:
            self.timer += dt
            if self.timer >= self.current_animation.frame_duration:
                self.timer = 0
                self.current_frame += 1

                if self.current_frame >= len(self.current_animation.frames):
                    if self.current_animation.loop:
                        self.current_frame = 0
                    else:
                        self.current_frame = len(self.current_animation.frames) - 1

    def get_current_frame(self) -> pygame.Surface:
        return self.current_animation.frames[self.current_frame] if self.current_animation else None