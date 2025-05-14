import copy
import random
import numpy as np


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

        if self._ind >= len(self.buffer):
            self._ind = 0

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
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
