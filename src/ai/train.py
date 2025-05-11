import os

from src.ai.dqn.dqn_trainer import DQNTrainer
from src.core.game_manager import GameManager


def train(game_manager: GameManager, player_trainer: DQNTrainer, enemy_trainer: DQNTrainer, save_interval=10000, target_update_interval=1000):
    step_counter = 0
    save_path = 'models/saves'
    os.makedirs(save_path, exist_ok=True)

    while True:
        player_state, player_action, player_new_states, player_rewards, player_done, \
        enemy_state, enemy_action, enemy_new_states, enemy_rewards, enemy_done = game_manager.parallel_step()

        step_counter += 1
        for i in range(len(player_state)):
            player_trainer.buffer.push(
                player_state[i], player_action[i], player_rewards[i], player_new_states[i], player_done[i]
            )
            enemy_trainer.buffer.push(
                enemy_state[i], enemy_action[i], enemy_rewards[i], enemy_new_states[i], enemy_done[i]
            )

        player_trainer.train_step()
        enemy_trainer.train_step()
        if step_counter % target_update_interval == 0:
            player_trainer.model.update_target_network()
            enemy_trainer.model.update_target_network()

        if step_counter % 100 == 0:
            print("YAY!")

        if step_counter % save_interval == 0:
            player_trainer.model.save(os.path.join(save_path, f'player_model_{step_counter}.pth'))
            enemy_trainer.model.save(os.path.join(save_path, f'enemy_model_{step_counter}.pth'))
            print(f"Models saved at step {step_counter}")


