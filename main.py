import sys

import pygame

from src.core.games.game import Game

sys.setrecursionlimit(10**9)

game = Game()

game.run()

pygame.quit()