import sys

import pygame

from src.ui.menu import MenuScreen
from src.utils.hyper_parameters import SCREEN_WIDTH, SCREEN_HEIGHT

sys.setrecursionlimit(10**9)


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
menu = MenuScreen(screen)
menu.run()

pygame.quit()