import pygame

from src.core.controllers.base_controller import BaseController
from src.core.games.base_game import BaseGame


class GameController(BaseController):
    def __init__(self, game: BaseGame, keys: dict = None):
        super().__init__()
        self.game = game
        self.keys = keys or {
            'esc': pygame.K_ESCAPE,
        }

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.keys['esc']:
                    self.game.is_running = False
            if event.type == pygame.QUIT:
                self.game.is_running = False