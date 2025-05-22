import math

import torch

from src.ai.dqn.replay_buffer import ReplayBuffer
from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig
from src.ai.utils.logs import Logs
from src.utils.hyper_parameters import TRAINING_FPS, ENEMY_SPEED, MAZE_SIZE, CELL_WIDTH


class DQNTrainer:
    def __init__(self, model_wrapper: DQNWrapper, buffer: ReplayBuffer, config: DQNConfig):
        self.model = model_wrapper
        self.buffer = buffer
        self.config = config
        self.POASDFJIOAS = 0
        self.pjsdaofasdjiof = 0

    def train_step(self):
        if len(self.buffer) < self.config.batch_size:
            return 0

        states, actions, rewards, next_states, dones = self.buffer.sample(self.config.batch_size, self.model.device)

        self.model.target_model.eval()
        self.model.model.train()

        current_q = self.model.model(states).gather(1, actions.unsqueeze(1)).squeeze()
        with torch.no_grad():
            # next_q = self.model.target_model(next_states).max(1)[0].detach()

            #DoubleDQN
            next_actions = self.model.model(next_states).argmax(dim=1, keepdim=True)
            next_q = self.model.target_model(next_states).gather(1, next_actions).squeeze().detach()

        target_q = rewards + (1 - dones) * self.config.gamma * next_q

        # if torch.min(dones) < -0.00001 or torch.max(dones) > 1.00001:
        #     raise RuntimeError("loh")
        # adifjbapfdiogjfaiod = torch.mean(torch.abs(target_q))
        # self.POASDFJIOAS = 0.9999 * self.POASDFJIOAS + 0.0001 * adifjbapfdiogjfaiod
        # print('MEuihsadfpioauhsdfsadf ', self.POASDFJIOAS)
        # рывфгафоывшавоызшщ = torch.mean(torch.abs(current_q.squeeze()))
        # self.pjsdaofasdjiof = 0.9999 * self.pjsdaofasdjiof + 0.0001 * рывфгафоывшавоызшщ
        # print("aspdjifpasiodjfpsaoijpio", self.pjsdaofasdjiof)

        loss = self.model.loss(current_q, target_q)
        self.model.optimizer.zero_grad()
        loss.backward()
        self.model.optimizer.step()

        # print("saoijdifaposdijfasdfij", loss.item())
        # print("oaijjfdosdpafjasdpo", ((target_q - current_q.squeeze())**2).mean())
        # print(target_q)
        # print(current_q.squeeze())
        # print()
        # print()

        return loss.item()
