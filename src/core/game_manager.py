from datetime import timedelta, datetime

import pygame

from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig
from src.ai.utils.logs import Logs
from src.core.games.train_game import TrainGame
from src.rendering.drawer import Drawer
from src.utils.hyper_parameters import GAME_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT, TRAINING_FPS


class GameManager:
    def __init__(self, num_games: int, config: DQNConfig, player_model: DQNWrapper, enemy_model: DQNWrapper, screen):
        self.num_games = num_games
        self.config = config
        self.player_model = player_model
        self.enemy_model = enemy_model
        self.games = [TrainGame(player_model, enemy_model, config) for _ in range(num_games)]
        self.screen = screen
        drawer = Drawer(self.screen)
        self.games[0].set_drawer(drawer)
        self.dt = 1 / TRAINING_FPS
        self.game_duration = GAME_DURATION

    def update(self, player_model, enemy_model):
        self.player_model = player_model
        self.enemy_model = enemy_model

    def reset_game(self, ind: int):
        Logs.append(self.games[ind].get_sum_rewards()[0], Logs.player_rewards_per_game)
        Logs.append(self.games[ind].get_sum_rewards()[1], Logs.enemy_rewards_per_game)
        Logs.append(timedelta.total_seconds(datetime.now() - self.games[ind].start_time), Logs.game_duration)
        self.games[ind] = TrainGame(self.player_model, self.enemy_model, self.config)
        if ind == 0:
            self.games[ind].set_drawer(Drawer(self.screen))

    def parallel_step(self):
        player_states, player_actions, player_new_states, player_rewards, player_dones = [], [], [], [], []
        enemy_states, enemy_actions, enemy_new_states, enemy_rewards, enemy_dones = [], [], [], [], []
        for i in range(self.num_games):
            states = self.games[i].get_state()
            player_states.append(states[0])
            enemy_states.append(states[1])

        # actions =

        for i in range(self.num_games):
            self.games[i].step(self.dt)
            new_states = self.games[i].get_state()
            rewards = self.games[i].get_rewards()
            actions = self.games[i].get_action()

            player_new_states.append(new_states[0])
            player_rewards.append(rewards[0])
            player_actions.append(actions[0])

            enemy_new_states.append(new_states[1])
            enemy_rewards.append(rewards[1])
            enemy_actions.append(actions[1])

            if (not self.games[i].is_running or
                    timedelta.total_seconds(datetime.now() - self.games[i].start_time) > GAME_DURATION):
                self.reset_game(i)
                player_dones.append(True)
                enemy_dones.append(True)
            else:
                player_dones.append(False)
                enemy_dones.append(False)

        return player_states, player_actions, player_new_states, player_rewards, player_dones, \
               enemy_states, enemy_actions, enemy_new_states, enemy_rewards, enemy_dones


