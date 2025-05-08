import sys

import pygame

from src.core.games.debug_game import DebugGame
from src.core.games.game import Game
from src.rendering.drawer import Drawer
from src.utils.hyper_parameters import SCREEN_WIDTH, SCREEN_HEIGHT

sys.setrecursionlimit(10**9)

pygame.init()

game = Game()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
drawer = Drawer(screen)
game.set_drawer(drawer)

game.run()

pygame.quit()