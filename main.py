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
from src.utils.hyper_parameters import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COUNT

sys.setrecursionlimit(10**9)

pygame.init()

config = DQNConfig()
player_model = DQNWrapper(config.input_dim, config.action_size)
player_model.load('saves/player_model.pth')

enemy_model = DQNWrapper(config.input_dim, config.action_size)
enemy_model.load('saves/enemy_model.pth')

player_buffer = ReplayBuffer(config.buffer_size)
enemy_buffer = ReplayBuffer(config.buffer_size)

player_trainer = DQNTrainer(player_model, player_buffer, config)
enemy_trainer = DQNTrainer(enemy_model, enemy_buffer, config)

game_manager = GameManager(GAME_COUNT, config, player_model, enemy_model)

train(
    game_manager,
    player_trainer,
    enemy_trainer,
    save_interval=10000,
    target_update_interval=1000)

# game = DebugGame()
# # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# drawer = Drawer(screen)
# game.set_drawer(drawer)
#
# game.run()

pygame.quit()