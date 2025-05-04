import os
import pygame


class SpriteLoader:
    @staticmethod
    def load_sprite(path: str, alpha: bool = True) -> pygame.Surface:
        try:
            surface = pygame.image.load(path)
            return surface.convert() if alpha else surface.convert()
        except pygame.error as e:
            raise SystemExit(f'Ошибка загрузки спрайта: {path}\n{e}')

    @staticmethod
    def load_animation(folder: str) -> list[pygame.Surface]:
        frames = []
        for filename in sorted(os.listdir(folder)):
            frame_path = os.path.join(folder, filename)
            frames.append(SpriteLoader.load_sprite(frame_path))
        return frames