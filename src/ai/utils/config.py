from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim: int = 4
    action_size: int = 8
    buffer_size: int = 100_000
    batch_size: int = 64
    gamma: float = 0.99
    lr: float = 1e-4
    sync_target_frames: int = 3_000
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 20_000

    area_width = 7
    area_height = 5