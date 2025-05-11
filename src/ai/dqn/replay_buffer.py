import copy
from collections import deque
import random

import numpy as np


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((
            copy.deepcopy(state),
            copy.deepcopy(action),
            copy.deepcopy(reward),
            copy.deepcopy(next_state),
            copy.deepcopy(done)
        ))

    #TODO возможно стоит ускорить
    def sample(self, batch_size):
        batch = random.sample(list(self.buffer), batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards, dtype=np.float32),
            np.array(next_states),
            np.array(dones, dtype=np.uint8)
        )

    def __len__(self):
        return len(self.buffer)
