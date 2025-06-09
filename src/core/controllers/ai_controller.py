import copy
import datetime
import math
import random

import numpy as np
import torch

from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig
from src.ai.utils.iter_counter import IterCounter
from src.ai.utils.logs import Logs
from src.ai.utils.state_encoder import StateEncoder
from src.core.controllers.base_controller import BaseController
from src.core.grid.grid_manager import GridManager
from src.game_objects.enemy import Enemy
from src.game_objects.movable import Movable
from src.utils.constants import TRAINING_DT


class AIController(BaseController):
    def __init__(self, obj: Movable, grid_manager: GridManager, dqn_wrapper: DQNWrapper,
                 config: DQNConfig = DQNConfig(), is_training: bool = False):
        super().__init__()
        self.obj = obj
        self.grid_manager = grid_manager
        self.dqn = dqn_wrapper
        self.config = config
        self.encoder = StateEncoder(grid_manager)
        self.is_training = is_training
        self.frame_idx = 0
        self.last_action = 0
        self.last_time = datetime.datetime.now()

        self.velocity = [0, 0]
        self.logs = Logs()

    def get_action(self):
        state = self.encoder.encode(self.obj)
        # print(state)
        eps: float = 0.01
        if self.is_training:
            eps = self.config.epsilon_final + (self.config.epsilon_start - self.config.epsilon_final) * \
                  math.exp(-IterCounter.counter / self.config.epsilon_decay)
            Logs.append(eps, Logs.eps)

        self.frame_idx += 1

        if np.random.random() < eps:
            return np.random.randint(0, self.config.action_size)

        if not self.is_training:
            if datetime.timedelta.total_seconds(datetime.datetime.now() - self.last_time) < TRAINING_DT:
                return self.last_action

        self.dqn.model.eval()
        state_t = torch.FloatTensor(state).to(self.dqn.device).unsqueeze(0)
        q_values = self.dqn.model(state_t)[0]

        self.last_time = datetime.datetime.now()
        self.last_action = q_values.argmax().item()

        return self.last_action

    def handle(self, events):
        action = self.get_action()
        self.velocity = [0, 0]

        diagonal_speed = 1 / math.sqrt(2)
        velocities = [
            [-1, 0],
            [-diagonal_speed, diagonal_speed],
            [0, 1],
            [diagonal_speed, diagonal_speed],
            [1, 0],
            [diagonal_speed, -diagonal_speed],
            [0, -1],
            [-diagonal_speed, -diagonal_speed]
        ]

        self.velocity = velocities[action]
        self.update()

        return action

    def update(self):
        self.obj.update_velocity(self.velocity)