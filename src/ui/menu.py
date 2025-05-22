import pygame

from src.ai.dqn.dqn_trainer import DQNTrainer
from src.ai.dqn.replay_buffer import ReplayBuffer
from src.ai.models.dqn_model import DQNWrapper
from src.ai.train import train
from src.ai.utils.config import DQNConfig
from src.core.game_manager import GameManager
from src.core.games.debug_game import DebugGame
from src.core.games.game import Game
from src.rendering.drawer import Drawer
from src.utils.hyper_parameters import COLOR_DARK_GREY, COLOR_LIGHTER_GREY, COLOR_BORDER, COLOR_TEXT, SCREEN_HEIGHT, \
    SCREEN_WIDTH, COLOR_BLACK, COLOR_GREEN, GAME_COUNT


class MenuButton:
    def __init__(self, text, action, rect, font, base_color=COLOR_DARK_GREY, hover_color=COLOR_LIGHTER_GREY,
                 text_color=COLOR_TEXT, border_color=COLOR_BORDER):
        self.text = text
        self.action = action
        self.rect = pygame.Rect(rect)
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.is_hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.base_color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=5)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            return self.action
        return None


class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        try:
            self.title_font = pygame.font.Font("arial", 74) if "arial" in pygame.font.get_fonts() else pygame.font.Font(
                None, 74)
            self.button_font = pygame.font.Font("arial",
                                                40) if "arial" in pygame.font.get_fonts() else pygame.font.Font(None,
                                                                                                                40)
        except:
            self.title_font = pygame.font.Font(None, 74)
            self.button_font = pygame.font.Font(None, 40)

        self.buttons = []
        self.button_width = 300
        self.button_height = 55
        self.button_spacing = 15

        start_y = SCREEN_HEIGHT // 2 - (5 * (
                    self.button_height + self.button_spacing) - self.button_spacing) // 2 - 20

        button_actions = [
            ("Начать игру", "start_normal_game"),
            ("Дебаг", "start_debug_game"),
            ("Тренировка", "start_ai_training"),
            ("Таблица", "show_leaderboard"),
            ("Выход", "exit_game")
        ]

        for i, (text, action) in enumerate(button_actions):
            button_y = start_y + i * (self.button_height + self.button_spacing)
            rect = (SCREEN_WIDTH // 2 - self.button_width // 2, button_y, self.button_width, self.button_height)
            self.buttons.append(MenuButton(text, action, rect, self.button_font))

    def step(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit_game"

            for button in self.buttons:
                action = button.handle_event(event, mouse_pos)
                if action:
                    return action

        self.draw()
        self.clock.tick(60)
        return ""

    def run(self):
        self.running = True
        while self.running:
            action = self.step()
            if action == "start_normal_game":
                self.run_normal_game()
            elif action == "start_debug_game":
                self.run_debug_game()
            elif action == "start_ai_training":
                self.run_ai_training()
            elif action == "show_leaderboard":
                print("Действие 'Таблица' пока не реализовано.")
                pygame.time.wait(1000)
            elif action == "exit_game":
                self.running = False

    def draw(self):
        self.screen.fill(COLOR_BLACK)

        title_text_surface = self.title_font.render("NeuroKrod", True, COLOR_GREEN)
        title_rect = title_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 30))
        self.screen.blit(title_text_surface, title_rect)

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()


    def run_normal_game(self):
        print("Запуск обычной игры...")
        game_instance = Game()
        drawer = Drawer(self.screen)
        game_instance.set_drawer(drawer)
        game_instance.run()
        print("Обычная игра завершена.")


    def run_debug_game(self):
        print("Запуск дебаг-игры...")
        game_instance = DebugGame()
        drawer = Drawer(self.screen)
        game_instance.set_drawer(drawer)
        game_instance.run()
        print("Дебаг-игра завершена.")


    def run_ai_training(self):
        print("Запуск тренировки AI...")
        try:
            config = DQNConfig()
            player_model = DQNWrapper(config.input_dim, config.action_size)

            enemy_model = DQNWrapper(config.input_dim, config.action_size)

            player_buffer = ReplayBuffer(config.buffer_size)
            enemy_buffer = ReplayBuffer(config.buffer_size)

            player_trainer = DQNTrainer(player_model, player_buffer, config)
            enemy_trainer = DQNTrainer(enemy_model, enemy_buffer, config)

            game_manager = GameManager(GAME_COUNT, config, player_model, enemy_model, self.screen)

            train(
                game_manager,
                player_trainer,
                enemy_trainer,
                save_interval=10000
            )
        except Exception as e:
            print(f"Ошибка во время тренировки AI: {e}")
        print("Тренировка AI завершена (или прервана).")