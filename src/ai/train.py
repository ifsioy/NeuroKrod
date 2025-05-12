import os

from src.ai.dqn.dqn_trainer import DQNTrainer
from src.ai.utils.iter_counter import IterCounter
from src.ai.utils.logs import Logs
from src.core.game_manager import GameManager
from src.utils.hyper_parameters import LOG_DRAW_PERIOD


def train(game_manager: GameManager, player_trainer: DQNTrainer, enemy_trainer: DQNTrainer, save_interval=10000, target_update_interval=1000):
    save_path = 'src/ai/models/saves'
    os.makedirs(save_path, exist_ok=True)
    mean_player_reward = 0
    mean_enemy_reward = 0
    const_for_idk = 1
    logs = Logs()

    while True:
        player_state, player_action, player_new_states, player_rewards, player_done, \
        enemy_state, enemy_action, enemy_new_states, enemy_rewards, enemy_done = game_manager.parallel_step()

        mean_player_reward = (mean_player_reward * ((const_for_idk - 1) / const_for_idk) +
                              sum(player_rewards) / len(player_rewards) / const_for_idk)
        mean_enemy_reward = (mean_enemy_reward * ((const_for_idk - 1) / const_for_idk) +
                              sum(enemy_rewards) / len(enemy_rewards) / const_for_idk)

        const_for_idk = min(const_for_idk + 1, 1000)

        IterCounter.increment()
        for i in range(len(player_state)):
            player_trainer.buffer.push(
                player_state[i], player_action[i], player_rewards[i], player_new_states[i], player_done[i]
            )
            enemy_trainer.buffer.push(
                enemy_state[i], enemy_action[i], enemy_rewards[i], enemy_new_states[i], enemy_done[i]
            )

        pl = player_trainer.train_step()
        el = enemy_trainer.train_step()

        logs.append_pl(pl)
        logs.append_el(el)
        logs.append_pr(mean_player_reward)
        logs.append_er(mean_enemy_reward)

        if IterCounter.counter % target_update_interval == 0:
            player_trainer.model.update_target_network()
            enemy_trainer.model.update_target_network()

        if IterCounter.counter % 100 == 0:
            print("YAY!")
            print(f"Player mean reward: {mean_player_reward}, Enemy mean reward: {mean_enemy_reward}")

        if IterCounter.counter % LOG_DRAW_PERIOD == 0:
            logs.draw_graphics()

        if IterCounter.counter % save_interval == 0:
            player_trainer.model.save(os.path.join(save_path, f'player_model_{IterCounter.counter}.pth'))
            enemy_trainer.model.save(os.path.join(save_path, f'enemy_model_{IterCounter.counter}.pth'))
            print(f"Models saved at step {IterCounter.counter}")


