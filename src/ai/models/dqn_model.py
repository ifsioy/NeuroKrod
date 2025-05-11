import os

import torch
import torch.nn as nn
import torch.optim as optim

from src.ai.utils.config import DQNConfig


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim),
        )

    def forward(self, x):
        return self.net(x)

class DQNWrapper:
    def __init__(self, input_dim, action_space, lr = DQNConfig.lr):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(input_dim, action_space).to(self.device)
        self.target_model = DQN(input_dim, action_space).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss = nn.MSELoss()

    def update_target_network(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path))

