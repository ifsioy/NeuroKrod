import copy
import random
import numpy as np
import torch

from src.ai.utils.logs import Logs


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity
        self._ind = 0

    def push(self, state, action, reward, next_state, done):
        tmp = (
            state,
            action,
            reward,
            next_state,
            done
        )

        if len(self.buffer) < self.capacity:
            self.buffer.append(copy.deepcopy(tmp))
        else:
            self.buffer[self._ind] = copy.deepcopy(tmp)
            self._ind += 1

        if self._ind >= self.capacity:
            self._ind = 0


    def sample(self, batch_size, device = 'cpu'):
        batch = random.choices(self.buffer, k=batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            torch.tensor(np.array(states), dtype=torch.float32, device=device),
            torch.tensor(np.array(actions), dtype=torch.int64, device=device),
            torch.tensor(np.array(rewards, dtype=np.float32), dtype=torch.float32, device=device),
            torch.tensor(np.array(next_states), dtype=torch.float32, device=device),
            torch.tensor(np.array(dones, dtype=np.uint8), dtype=torch.float32, device=device),
        )

    def __len__(self):
        return len(self.buffer)
