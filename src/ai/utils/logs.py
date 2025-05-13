from src.utils.hyper_parameters import LOG_PERIOD, LOG_SIZE
import matplotlib.pyplot as plt

class Logs:
    _instance = None

    enemy_rewards = []
    player_rewards = []
    enemy_loss = []
    player_loss = []
    eps = []

    er_uc = 0
    pr_uc = 0
    el_uc = 0
    pl_uc = 0
    eps_uc = 0

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def append_er(self, x: float):
        self.er_uc += 1
        if self.er_uc % LOG_PERIOD == 0:
            self.er_uc = 0
            self.enemy_rewards.append(x)

            if len(self.enemy_rewards) > LOG_SIZE:
                self.enemy_rewards = self.enemy_rewards[-LOG_SIZE // 2:]

    def append_pr(self, x: float):
        self.pr_uc += 1
        if self.pr_uc % LOG_PERIOD == 0:
            self.pr_uc = 0
            self.player_rewards.append(x)

            if len(self.player_rewards) > LOG_SIZE:
                self.player_rewards = self.player_rewards[-LOG_SIZE // 2:]

    def append_el(self, x: float):
        self.el_uc += 1
        if self.el_uc % LOG_PERIOD == 0:
            self.el_uc = 0
            self.enemy_loss.append(x)

            if len(self.enemy_loss) > LOG_SIZE:
                self.enemy_loss = self.enemy_loss[-LOG_SIZE // 2:]

    def append_pl(self, x: float):
        self.pl_uc += 1
        if self.pl_uc % LOG_PERIOD == 0:
            self.pl_uc = 0
            self.player_loss.append(x)

            if len(self.player_loss) > LOG_SIZE:
                self.player_loss = self.player_loss[-LOG_SIZE // 2:]

    def append_eps(self, x: float):
        self.eps_uc += 1
        if self.eps_uc % LOG_PERIOD == 0:
            self.eps_uc = 0
            self.eps.append(x)

            if len(self.eps) > LOG_SIZE:
                self.eps = self.eps[-LOG_SIZE // 2:]

    def draw_graphics(self):
        plt.plot(self.enemy_rewards, label='enemy_reward', color='red')
        plt.plot(self.player_rewards, label='player_reward', color='orange')
        plt.legend()
        plt.show()

        plt.plot(self.enemy_loss, label='enemy_loss', color='blue')
        plt.plot(self.player_loss, label='player_loss', color='purple')
        plt.legend()
        plt.show()

        plt.plot(self.eps, label='eps', color='blue')
        plt.legend()
        plt.show()
