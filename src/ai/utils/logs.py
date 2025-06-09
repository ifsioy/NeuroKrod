import numpy as np

from src.utils.constants import LOG_PERIOD, LOG_SIZE
import matplotlib.pyplot as plt

class Logs:
    _instance = None

    player_rewards = 'player_rewards'
    enemy_rewards = 'enemy_rewards'
    player_loss = 'player_loss'
    enemy_loss = 'enemy_loss'
    player_rewards_per_game = 'player_rewards_per_game'
    enemy_rewards_per_game = 'enemy_rewards_per_game'
    eps = 'eps'
    game_duration = 'game_duration'
    mean_target = 'mean_target'
    mean_current = 'mean_current'
    mean_states = 'mean_states'

    mean_rew = 'mean_rew'
    mean_next = 'mean_next'

    data = {
        'enemy_rewards': [],
        'player_rewards': [],
        'enemy_loss': [],
        'player_loss': [],
        'enemy_rewards_per_game': [],
        'player_rewards_per_game': [],
        'eps': [],
        'game_duration': [],
        'mean_target': [],
        'mean_current': [],
        'mean_states': [],

        'mean_rew': [],
        'mean_next': [],
    }

    counters = {
        'enemy_rewards': 0,
        'player_rewards': 0,
        'enemy_loss': 0,
        'player_loss': 0,
        'enemy_rewards_per_game': 0,
        'player_rewards_per_game': 0,
        'eps': 0,
        'game_duration': 0,
        'mean_target': 0,
        'mean_current': 0,
        'mean_states': 0,

        'mean_rew': 0,
        'mean_next': 0,
    }

    mean = {
        'enemy_rewards': 0.,
        'player_rewards': 0.,
        'enemy_loss': 0.,
        'player_loss': 0.,
        'enemy_rewards_per_game': 0.,
        'player_rewards_per_game': 0.,
        'eps': 0.,
        'game_duration': 0.,
        'mean_target': 0.,
        'mean_current': 0.,
        'mean_states': 0.,

        'mean_rew': 0.,
        'mean_next': 0.,
    }

    actions = [0] * 8

    max_rast = 0

    const_for_idk = 1

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def append(x: float, type: str):
        if type not in Logs.data:
            raise ValueError(f"Invalid log type: {type}")


        if type == Logs.player_rewards:
            Logs.const_for_idk = min(Logs.const_for_idk + 1, 1000)

        Logs.counters[type] += 1
        Logs.mean[type] = (Logs.mean[type] * (Logs.const_for_idk - 1) / Logs.const_for_idk +
                            x / Logs.const_for_idk)

        if Logs.counters[type] % LOG_PERIOD == 0:
            Logs.counters[type] = 0
            if type == 'eps':
                Logs.data[type].append(x)
            else:
                Logs.data[type].append(Logs.mean[type])

            if len(Logs.data[type]) > LOG_SIZE:
                Logs.data[type] = Logs.data[type][-LOG_SIZE // 2:]


    @staticmethod
    def draw_graphics():
        plt.close('all')
        plt.plot(Logs.data['enemy_rewards'], label='enemy_reward', color='red')
        plt.plot(Logs.data['player_rewards'], label='player_reward', color='orange')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['player_rewards_per_game'], label='player_reward_per_game', color='green')
        plt.plot(Logs.data['enemy_rewards_per_game'], label='enemy_reward_per_game', color='olive')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['enemy_loss'], label='enemy_loss', color='blue')
        plt.legend()
        plt.show()
        plt.plot(Logs.data['player_loss'], label='player_loss', color='purple')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['eps'], label='eps', color='blue')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['game_duration'], label='game_duration', color='red')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['mean_target'], label='mean_target', color='blue')
        plt.plot(Logs.data['mean_current'], label='mean_current', color='green')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['mean_states'], label='mean_states', color='pink')
        plt.legend()
        plt.show()

        plt.plot(Logs.data['mean_rew'], label='mean_rew', color='purple')
        plt.plot(Logs.data['mean_next'], label='mean_next', color='blue')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 6))
        for i in range(8):
            bar = plt.bar(i * 20, Logs.actions[i], width=15, label=f'{i}' , color='blue', alpha=0.5)


            plt.text(
                i * 20,
                100,
                f'{i} {Logs.actions[i]}',
                ha='center', va='bottom'
            )

        plt.title('actions')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.show()

