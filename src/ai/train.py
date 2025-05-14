import os

from src.ai.dqn.dqn_trainer import DQNTrainer
from src.ai.utils.config import DQNConfig
from src.ai.utils.iter_counter import IterCounter
from src.ai.utils.logs import Logs
from src.core.game_manager import GameManager
from src.utils.hyper_parameters import LOG_DRAW_PERIOD


def train(game_manager: GameManager, player_trainer: DQNTrainer, enemy_trainer: DQNTrainer, save_interval=10000, target_update_interval=DQNConfig.sync_target_frames):
    save_path = 'src/ai/models/saves'
    os.makedirs(save_path, exist_ok=True)

    while True:
        player_state, player_action, player_new_states, player_rewards, player_done, \
        enemy_state, enemy_action, enemy_new_states, enemy_rewards, enemy_done = game_manager.parallel_step()

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


        Logs.append(sum(player_rewards) / len(player_rewards), Logs.player_rewards)
        Logs.append(sum(enemy_rewards) / len(enemy_rewards), Logs.enemy_rewards)

        Logs.append(pl, Logs.player_loss)
        Logs.append(el, Logs.enemy_loss)


        if IterCounter.counter % target_update_interval == 0:
            player_trainer.model.update_target_network()
            enemy_trainer.model.update_target_network()

        if IterCounter.counter % 100 == 0:
            print('iters - ', IterCounter.counter)

        if IterCounter.counter % LOG_DRAW_PERIOD == 0:
            Logs.draw_graphics()

        if IterCounter.counter % save_interval == 0:
            player_trainer.model.save(os.path.join(save_path, f'player_model_{IterCounter.counter}.pth'))
            enemy_trainer.model.save(os.path.join(save_path, f'enemy_model_{IterCounter.counter}.pth'))
            print(f"Models saved at step {IterCounter.counter}")


