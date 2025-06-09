import math

import torch

from src.ai.dqn.replay_buffer import ReplayBuffer
from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig
from src.ai.utils.logs import Logs
from src.utils.constants import TRAINING_FPS, ENEMY_SPEED, MAZE_SIZE, CELL_WIDTH


class DQNTrainer:
    def __init__(self, model_wrapper: DQNWrapper, buffer: ReplayBuffer, config: DQNConfig):
        self.model = model_wrapper
        self.buffer = buffer
        self.config = config

    def train_step(self):
        if len(self.buffer) < self.config.batch_size:
            return 0

        states, actions, rewards, next_states, dones = self.buffer.sample(self.config.batch_size, self.model.device)

        self.model.target_model.eval()
        self.model.model.train()

        current_q = self.model.model(states).gather(1, actions.unsqueeze(1)).squeeze()
        with torch.no_grad():
            next_q = self.model.target_model(next_states).max(1)[0].detach()

            #DoubleDQN
            # next_actions = self.model.model(next_states).argmax(dim=1, keepdim=True)
            # next_q = self.model.target_model(next_states).gather(1, next_actions).squeeze().detach()

        target_q = rewards + (1 - dones) * self.config.gamma * next_q

        mean_target = torch.mean(target_q)
        mean_current = torch.mean(current_q.squeeze())
        mean_states = torch.mean(states)

        mean_rew = torch.mean(rewards)
        mean_next = torch.mean(next_q)

        Logs.append(mean_target.item(), 'mean_target')
        Logs.append(mean_current.item(), 'mean_current')
        Logs.append(mean_states.item(), 'mean_states')

        Logs.append(mean_rew.item(), 'mean_rew')
        Logs.append(mean_next.item(), 'mean_next')

        loss = self.model.loss(current_q, target_q)
        self.model.optimizer.zero_grad()
        torch.nn.utils.clip_grad_norm_(self.model.model.parameters(), max_norm=1.0)  # Gradient clipping
        loss.backward()
        self.model.optimizer.step()

        # print("saoijdifaposdijfasdfij", loss.item())
        # print("oaijjfdosdpafjasdpo", ((target_q - current_q.squeeze())**2).mean())
        # print(target_q)
        # print(current_q.squeeze())
        # print()
        # print()

        return loss.item()
