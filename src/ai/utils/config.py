from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim: int = 4
    action_size: int = 8
    buffer_size: int = 100_000
    batch_size: int = 128
    gamma: float = 0.99
    lr: float = 1e-3
    sync_target_frames: int = 100
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 1_000

    area_width = 7
    area_height = 5