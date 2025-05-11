from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim: int = 840
    action_size: int = 8
    buffer_size: int = 10_000
    batch_size: int = 64
    gamma: float = 0.99
    lr: float = 1e-3
    sync_target_frames: int = 1000
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 100_000

    area_width = 7
    area_height = 5