import sys

import pygame

from src.ui.menu import MenuScreen
from src.utils.animations import SCREEN

sys.setrecursionlimit(10**9)


pygame.init()

menu = MenuScreen(SCREEN)
menu.run()

pygame.quit()