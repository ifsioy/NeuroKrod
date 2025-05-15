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

        states, actions, rewards, next_states, dones = self.buffer.sample(self.config.batch_size)

        states = torch.tensor(states, dtype=torch.float32).to(self.model.device)
        actions = torch.tensor(actions, dtype=torch.int64).to(self.model.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.model.device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.model.device)
        dones = torch.tensor(dones, dtype=torch.float32).to(self.model.device)

        # for i in range(len(actions)):
        #     state = states[i]
        #     action = actions[i]
        #     reward = rewards[i]
        #     next_state = next_states[i]
        #     done = dones[i]
        #
        #     ex, ey = state[2].item(), state[3].item()
        #     ex *= MAZE_SIZE * CELL_WIDTH
        #     ey *= MAZE_SIZE * CELL_WIDTH
        #
        #     diagonal_speed = 1 / math.sqrt(2)
        #     velocities = [
        #         [-1, 0],
        #         [-diagonal_speed, diagonal_speed],
        #         [0, 1],
        #         [diagonal_speed, diagonal_speed],
        #         [1, 0],
        #         [diagonal_speed, -diagonal_speed],
        #         [0, -1],
        #         [-diagonal_speed, -diagonal_speed]
        #     ]
        #
        #     velocity = velocities[action]
        #
        #     ex += 1 / TRAINING_FPS * velocity[0] * ENEMY_SPEED
        #     ey += 1 / TRAINING_FPS * velocity[1] * ENEMY_SPEED
        #
        #     ex /= MAZE_SIZE * CELL_WIDTH
        #     ey /= MAZE_SIZE * CELL_WIDTH
        #
        #     fex, fey = next_state[2].item(), next_state[3].item()
        #
        #     if ex != fex or ey != fey:
        #         cx, cy = fex - state[2].item(), fey - state[3].item()
        #         cx *= MAZE_SIZE * CELL_WIDTH / (1 / TRAINING_FPS * ENEMY_SPEED)
        #         cy *= MAZE_SIZE * CELL_WIDTH / (1 / TRAINING_FPS * ENEMY_SPEED)
        #
        #         if (ex - state[2].item()) * velocity[0] >= 0 and (ey - state[3].item()) * velocity[1] >= 0:
        #             continue
        #
        #
        #         print('ERROR')
        #         print("ex, ey", ex, ey)
        #         print("fex, fey", fex, fey)
        #         print("action", action)
        #         print('velocity', velocity)
        #         print("state", state)
        #         print("next_state", next_state)
        #         print("reward", reward)
        #         print("done", done)
        #
        #         print("cx, cy", cx, cy)
        #         i = 0
        #         for j in range(len(velocities)):
        #             if velocities[j][0] == cx and velocities[j][1] == cy:
        #                 i = j
        #
        #         print('MUST BE', i)
        #         print()

        self.model.target_model.eval()
        self.model.model.train()

        current_q = self.model.model(states).gather(1, actions.unsqueeze(1)).squeeze()
        with torch.no_grad():
            next_q = self.model.target_model(next_states).max(1)[0].detach()
        target_q = rewards + (1 - dones) * self.config.gamma * next_q

        if torch.min(dones) < -0.00001 or torch.max(dones) > 1.00001:
            raise RuntimeError("loh")
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
