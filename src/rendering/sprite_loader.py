import os
import pygame

from src.rendering.components.animation import AnimationData
from src.utils.constants import BASE_SIZE


class SpriteLoader:
    @staticmethod
    def load_sprite(path: str, width, height, alpha: bool = True) -> pygame.Surface:
        try:
            surface = pygame.image.load(path)
            surface = surface.convert_alpha() if alpha else surface.convert()
            surface = pygame.transform.scale(surface, (width * BASE_SIZE, height * BASE_SIZE))
            return surface
        except pygame.error as e:
            raise SystemExit(f'Ошибка загрузки спрайта: {path}\n{e}')

    @staticmethod
    def load_animation(folder: str, width, height) -> AnimationData:
        frames = []
        for filename in sorted(os.listdir(folder)):
            frame_path = os.path.join(folder, filename)
            frames.append(SpriteLoader.load_sprite(frame_path, width, height))
        return AnimationData(frames=frames)