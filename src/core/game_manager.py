from datetime import timedelta, datetime

import pygame

from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig
from src.core.games.train_game import TrainGame
from src.rendering.drawer import Drawer
from src.utils.hyper_parameters import GAME_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT, TRAINING_FPS


class GameManager:
    def __init__(self, num_games: int, config: DQNConfig, player_model: DQNWrapper, enemy_model: DQNWrapper):
        self.num_games = num_games
        self.config = config
        self.player_model = player_model
        self.enemy_model = enemy_model
        self.games = [TrainGame(player_model, enemy_model, config) for _ in range(num_games)]
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        drawer = Drawer(self.screen)
        self.games[0].set_drawer(drawer)
        self.dt = 1 / TRAINING_FPS
        self.game_duration = GAME_DURATION

    def update(self, player_model, enemy_model):
        self.player_model = player_model
        self.enemy_model = enemy_model

    def reset_game(self, ind: int):
        self.games[ind] = TrainGame(self.player_model, self.enemy_model, self.config)
        if ind == 0:
            self.games[ind].set_drawer(Drawer(self.screen))

    def parallel_step(self):
        player_state, player_action, player_new_states, player_rewards, player_done = [], [], [], [], []
        enemy_state, enemy_action, enemy_new_states, enemy_rewards, enemy_done = [], [], [], [], []
        for i in range(self.num_games):
            states = self.games[i].get_state()
            player_state.append(states[0])
            enemy_state.append(states[1])

        # actions =

        for i in range(self.num_games):

            self.games[i].step(self.dt)
            new_states = self.games[i].get_state()
            rewards = self.games[i].get_rewards()
            action = self.games[i].get_action()

            player_new_states.append(new_states[0])
            player_rewards.append(rewards[0])
            player_action.append(action[0])

            enemy_new_states.append(new_states[1])
            enemy_rewards.append(rewards[1])
            enemy_action.append(action[1])

            if (not self.games[i].is_running or
                    timedelta.total_seconds(datetime.now() - self.games[i].start_time) > GAME_DURATION):
                self.reset_game(i)
                player_done.append(True)
                enemy_done.append(True)
            else:
                player_done.append(False)
                enemy_done.append(False)

        return player_state, player_action, player_new_states, player_rewards, player_done, \
               enemy_state, enemy_action, enemy_new_states, enemy_rewards, enemy_done


