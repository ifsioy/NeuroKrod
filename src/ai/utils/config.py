from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim = (8, 33, 33)
    action_size: int = 8
    buffer_size: int = 30_000
    batch_size: int = 128
    gamma: float = 0.9
    lr: float = 5e-5
    sync_target_frames: int = 2000
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 20_000
