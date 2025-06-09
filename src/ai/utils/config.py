from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim = (14, 9, 9)
    action_size: int = 8
    buffer_size: int = 30_000
    batch_size: int = 128
    gamma: float = 0.95
    lr: float = 1e-4
    sync_target_frames: int = 4000
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 10_000
