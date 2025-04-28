import sys
import pygame

from src.core.game import Game

sys.setrecursionlimit(10**9)


game = Game()

game.run()

pygame.quit()