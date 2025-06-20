from typing import List

import pygame

from src.core.controllers.base_controller import BaseController
from src.core.games.base_game import BaseGame
from src.utils.constants import CAUGHT_EVENT, WIN_EVENT, ROOT_DIR


class GameController(BaseController):
    def __init__(self, game: BaseGame, keys: dict = None):
        super().__init__()
        self.game: BaseGame = game
        self.keys = keys or {
            'esc': pygame.K_ESCAPE,
            'g' : pygame.K_g,
            'p' : pygame.K_p,
            'o' : pygame.K_o,
        }

    def handle(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = getattr(event, 'key', None)
                if key == self.keys['esc']:
                    self.game.is_running = False
                if key == self.keys['g']:
                    if hasattr(self.game, 'drawer'):
                        if hasattr(self.game.drawer, 'is_disabled'):
                            self.game.drawer.is_disabled = not self.game.drawer.is_disabled
                if key == self.keys['p']:
                    self.game.save()
                if key == self.keys['o']:
                    self.game.load()

            if event.type == pygame.QUIT:
                self.game.is_running = False

            if event.type == CAUGHT_EVENT:
                self.game.is_running = False

            if event.type == WIN_EVENT:
                self.game.win = True
                self.game.is_running = False
