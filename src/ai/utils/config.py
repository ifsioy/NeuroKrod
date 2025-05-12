from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim: int = 1050
    action_size: int = 8
    buffer_size: int = 1_000_000
    batch_size: int = 1024
    gamma: float = 0.95
    lr: float = 5e-4
    sync_target_frames: int = 200
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 10_000

    area_width = 7
    area_height = 5