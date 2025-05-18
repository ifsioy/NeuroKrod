from dataclasses import dataclass


@dataclass
class DQNConfig:
    input_dim = (8, 21, 21)
    action_size: int = 9
    buffer_size: int = 100_000
    batch_size: int = 128
    gamma: float = 0.9
    lr: float = 5e-4
    sync_target_frames: int = 1000
    epsilon_start: float = 1.0
    epsilon_final: float = 0.01
    epsilon_decay: int = 3000

    area_width = 7
    area_height = 5