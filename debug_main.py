import sys

import pygame

from src.ai.dqn.dqn_trainer import DQNTrainer
from src.ai.dqn.replay_buffer import ReplayBuffer
from src.ai.models.dqn_model import DQNWrapper
from src.ai.train import train
from src.ai.utils.config import DQNConfig
from src.core.game_manager import GameManager
from src.core.games.debug_game import DebugGame
from src.core.games.game import Game
from src.rendering.drawer import Drawer
from src.utils.hyper_parameters import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COUNT, WIN, CAUGHT

sys.setrecursionlimit(10**9)


pygame.init()

game = DebugGame()
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
drawer = Drawer(screen)
game.set_drawer(drawer)

game.run()

pygame.quit()