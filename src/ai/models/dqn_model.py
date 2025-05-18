import os

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import tqdm
import torchvision.transforms as transforms

from src.ai.utils.config import DQNConfig

from tqdm import tqdm

device = 'cuda'

class Block(nn.Module):
    def __init__(self, input_channels, output_channels, layers, p, use_max_pool=True):
        super(Block, self).__init__()
        self.skip_connection = nn.Identity() if input_channels == output_channels else nn.Conv2d(input_channels, output_channels, kernel_size=1)
        self.layers = nn.Sequential(
            nn.Conv2d(input_channels, output_channels, kernel_size=3, padding='same'),
            *[
                layer
                for _ in range(layers - 1)
                for layer in (nn.ReLU(), nn.Conv2d(output_channels, output_channels, kernel_size=3, padding='same'))
            ]
        )
        self.activation = nn.ReLU()
        if use_max_pool:
            self.pooling = nn.MaxPool2d(kernel_size=2, stride=2)
        else:
            self.pooling = nn.Identity()
        self.dropout = nn.Dropout(p=p)
        self.batch_norm = nn.BatchNorm2d(output_channels)

    def forward(self, x):
        return self.batch_norm(self.dropout(self.pooling(self.activation(self.skip_connection(x) + self.layers(x)))))

class DQN(nn.Module):
    #8, 21, 21
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()

        block_num_layers = [2, 2, 2]
        blocks_num_channels = [input_dim[0], 16, 32, 64]
        use_max_pool = [True, True, True]
        dropouts = [0.05, 0.05, 0.05]
        fc_dropouts = [0.05, 0.05]

        fc_sizes = [64, 32, output_dim]

        self.net = nn.Sequential(
            *[
                Block(blocks_num_channels[i], blocks_num_channels[i + 1], block_num_layers[i], dropouts[i], use_max_pool[i]) for i in range(len(block_num_layers))
            ],
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(fc_sizes[0], fc_sizes[1]),
            *[
                layer for i in range(1, len(fc_sizes) - 1) for layer in (nn.ReLU(), nn.Dropout(fc_dropouts[i]), nn.BatchNorm1d(fc_sizes[i]), nn.Linear(fc_sizes[i], fc_sizes[i + 1]))
            ]
        )

    def forward(self, x):
        return self.net(x)

class CNNModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        #(1, 28, 28)
        super(CNNModel, self).__init__()
        self.net = nn.Sequential(*[
            nn.Conv2d(input_dim[0], 16, kernel_size=3, padding='same'),
            nn.MaxPool2d(2),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, padding='same'),
            nn.MaxPool2d(2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding='same'),
            nn.MaxPool2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(64 * 3 * 3, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        ])

    def forward(self, x):
        return self.net(x)

class DQNWrapper:
    def __init__(self, input_dim, action_space, lr = DQNConfig.lr):
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = 'cpu'
        self.model = DQN(input_dim, action_space).to(self.device)
        self.target_model = DQN(input_dim, action_space).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss = nn.MSELoss()

    def update_target_network(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path))


model = DQN((8, 21, 21), 9)
inp = torch.randn(64, 8, 21, 21)
out = model(inp)
print(out.shape)