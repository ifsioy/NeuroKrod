from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim: int = 1050
    action_size: int = 8
    buffer_size: int = 100_000
    batch_size: int = 512
    gamma: float = 0.95
    lr: float = 1e-4
    sync_target_frames: int = 100
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 4_000

    area_width = 7
    area_height = 5