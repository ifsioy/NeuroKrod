from src.utils.hyper_parameters import LOG_PERIOD
import matplotlib.pyplot as plt

class Logs:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.enemy_rewards = []
        self.player_rewards = []
        self.enemy_loss = []
        self.player_loss = []

        self.er_uc = 0
        self.pr_uc = 0
        self.el_uc = 0
        self.pl_uc = 0

    def append_er(self, x: float):
        self.er_uc += 1
        if self.er_uc % LOG_PERIOD == 0:
            self.er_uc = 0
            self.enemy_rewards.append(x)

    def append_pr(self, x: float):
        self.pr_uc += 1
        if self.pr_uc % LOG_PERIOD == 0:
            self.pr_uc = 0
            self.player_rewards.append(x)

    def append_el(self, x: float):
        self.el_uc += 1
        if self.el_uc % LOG_PERIOD == 0:
            self.el_uc = 0
            self.enemy_loss.append(x)

    def append_pl(self, x: float):
        self.pl_uc += 1
        if self.pl_uc % LOG_PERIOD == 0:
            self.pl_uc = 0
            self.player_loss.append(x)

    def draw_graphics(self):
        plt.plot(self.enemy_rewards, label='enemy_reward', color='red')
        plt.plot(self.player_rewards, label='player_reward', color='orange')
        plt.legend()
        plt.show()

        plt.plot(self.enemy_loss, label='enemy_loss', color='blue')
        plt.plot(self.player_loss, label='player_loss', color='purple')
        plt.legend()
        plt.show()
