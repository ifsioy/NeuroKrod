import torch

from src.ai.dqn.replay_buffer import ReplayBuffer
from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig


class DQNTrainer:
    def __init__(self, model_wrapper: DQNWrapper, buffer: ReplayBuffer, config: DQNConfig):
        self.model = model_wrapper
        self.buffer = buffer
        self.config = config

    def train_step(self):
        if len(self.buffer) < self.config.batch_size:
            return

        states, actions, rewards, next_states, dones = self.buffer.sample(self.config.batch_size)
        states = torch.FloatTensor(states).to(self.model.device)
        actions = torch.LongTensor(actions).to(self.model.device)
        rewards = torch.FloatTensor(rewards).to(self.model.device)
        next_states = torch.FloatTensor(next_states).to(self.model.device)
        dones = torch.FloatTensor(dones).to(self.model.device)

        self.model.target_model.eval()
        self.model.model.train()

        current_q = self.model.model(states).gather(1, actions.unsqueeze(1))
        with torch.no_grad():
            next_q = self.model.target_model(next_states).max(1)[0].detach()
        target_q = rewards + (1 - dones) * self.config.gamma * next_q

        loss = self.model.loss(current_q.squeeze(), target_q)
        self.model.optimizer.zero_grad()
        loss.backward()
        self.model.optimizer.step()
