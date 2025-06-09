import datetime
import time

import pygame

from src.ai.dqn.dqn_trainer import DQNTrainer
from src.ai.dqn.replay_buffer import ReplayBuffer
from src.ai.models.dqn_model import DQNWrapper
from src.ai.train import train
from src.ai.utils.config import DQNConfig
from src.core.db.records_model import RecordsModel
from src.core.game_manager import GameManager
from src.core.games.debug_game import DebugGame
from src.core.games.game import Game
from src.rendering.drawer import Drawer
from src.utils.constants import COLOR_DARK_GREY, COLOR_LIGHTER_GREY, COLOR_BORDER, COLOR_TEXT, SCREEN_HEIGHT, \
    SCREEN_WIDTH, COLOR_BLACK, COLOR_GREEN, GAME_COUNT, SAVES_DIR, ASSETS_DIR


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
            self.title_font = pygame.font.Font(ASSETS_DIR / 'fonts' / 'GNF.ttf', 74)
            self.button_font = pygame.font.Font(ASSETS_DIR / 'fonts' / 'GNF.ttf', 40)

            self.input_font = pygame.font.Font(ASSETS_DIR / 'fonts' / 'GNF.ttf', 50)
            self.leaderboard_font = pygame.font.Font(ASSETS_DIR / 'fonts' / 'GNF.ttf', 50)
            self.leaderboard_title_font = pygame.font.Font(ASSETS_DIR / 'fonts' / 'GNF.ttf', 100)
            self.message_font = pygame.font.Font(ASSETS_DIR / 'fonts' / 'GNF.ttf', 100)
        except Exception as e:
            print(f"Ошибка загрузки шрифта GNF.ttf: {e}. Используется шрифт по умолчанию.")
            self.input_font = pygame.font.Font(None, 50)
            self.leaderboard_font = pygame.font.Font(None, 30)
            self.leaderboard_title_font = pygame.font.Font(None, 50)
            self.message_font = pygame.font.Font(None, 100)
            self.title_font = pygame.font.Font(None, 100)
            self.button_font = pygame.font.Font(None, 50)

        self.buttons = []
        self.button_width = 300
        self.button_height = 55
        self.button_spacing = 15

        start_y = SCREEN_HEIGHT // 2 - (5 * (
                    self.button_height + self.button_spacing) - self.button_spacing) // 2 - 20

        button_actions = [
            ("Начать игру", "start_normal_game"),
            ("Таблица", "show_leaderboard"),
            ("Управление", "show_controls"),
            ("Дебаг", "start_debug_game"),
            ("Тренировка", "start_ai_training"),
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
                self.show_leaderboard_screen()
            elif action == "show_controls":
                self.show_controls_screen()
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

    def show_controls_screen(self):
        controls_text = [
            "Управление",
            "",
            "WASD или стрелочки — движение",
            "ESC — назад",
            "P — сохранить",
            "O — загрузить",
            "G — отключить отрисовку",
        ]

        controls_running = True
        while controls_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    controls_running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        controls_running = False
                        return

            if not self.running:
                break

            self.screen.fill(COLOR_BLACK)
            for i, line in enumerate(controls_text):
                font = self.leaderboard_title_font if i == 0 else self.leaderboard_font
                color = COLOR_GREEN if i == 0 else COLOR_TEXT
                surf = font.render(line, True, color)
                rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 120 + i * 60))
                self.screen.blit(surf, rect)

            pygame.display.flip()
            self.clock.tick(60)

    def show_leaderboard_screen(self):
        leaderboard_running = True
        try:
            records_model = RecordsModel()
            top_records = records_model.load()
            records_model.cleanup()
        except Exception as e:
            return

        title_surf = self.leaderboard_title_font.render("Таблица лидеров", True, COLOR_GREEN)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 20))

        back_prompt_surf = self.button_font.render("Нажмите ESC для возврата", True, COLOR_LIGHTER_GREY)
        back_prompt_rect = back_prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))


        while leaderboard_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    leaderboard_running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        leaderboard_running = False
                        return

            if not self.running:
                break

            self.screen.fill(COLOR_BLACK)
            self.screen.blit(title_surf, title_rect)
            self.screen.blit(back_prompt_surf, back_prompt_rect)

            start_y_offset = title_rect.bottom + 40
            line_height = self.leaderboard_font.get_linesize() + 10

            if not top_records:
                no_records_surf = self.leaderboard_font.render("Рекордов пока нет", True, COLOR_TEXT)
                no_records_rect = no_records_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(no_records_surf, no_records_rect)
            else:
                for i, record in enumerate(top_records):
                    name, score_time = record
                    minutes = int(score_time // 60)
                    seconds = int(score_time % 60)
                    milliseconds = int((score_time * 1000) % 1000)
                    time_str = f"{minutes:02}:{seconds:02}.{milliseconds:03}"

                    entry_text = f"{i + 1}. {name}: {time_str}"
                    entry_surf = self.leaderboard_font.render(entry_text, True, COLOR_TEXT)
                    entry_rect = entry_surf.get_rect(midtop=(SCREEN_WIDTH // 2, start_y_offset + i * line_height))
                    self.screen.blit(entry_surf, entry_rect)


            pygame.display.flip()
            self.clock.tick(60)

    def show_temporary_message(self, message_text, visible_duration_sec, fade_duration_sec):
        start_time = time.time()
        total_duration = fade_duration_sec * 2 + visible_duration_sec

        text_surface = self.message_font.render(message_text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        message_running = True
        while message_running:
            elapsed_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    message_running = False
                    return

            if not self.running:
                break

            alpha = 0
            if elapsed_time < fade_duration_sec:
                alpha = int((elapsed_time / fade_duration_sec) * 255)
            elif elapsed_time < fade_duration_sec + visible_duration_sec:
                alpha = 255
            elif elapsed_time < total_duration:
                alpha = int(((total_duration - elapsed_time) / fade_duration_sec) * 255)
            else:
                message_running = False
                break

            alpha = max(0, min(255, alpha))

            self.screen.fill(COLOR_BLACK)

            temp_surface = text_surface.copy()
            temp_surface.set_alpha(alpha)
            self.screen.blit(temp_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def get_player_name_input(self, prompt_text="Введите имя:"):
        player_name = ""
        input_active = True
        prompt_surface = self.input_font.render(prompt_text, True, COLOR_TEXT)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    input_active = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 20:
                            player_name += event.unicode

            if not self.running:
                return None


            self.screen.fill(COLOR_BLACK)
            self.screen.blit(prompt_surface, prompt_rect)

            name_surface = self.input_font.render(player_name, True, COLOR_TEXT)
            name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(name_surface, name_rect)

            pygame.display.flip()
            self.clock.tick(60)

        return player_name

    def run_normal_game(self):
        print("Запуск обычной игры...")
        pygame.mouse.set_visible(False)
        config = DQNConfig()
        enemy_model = DQNWrapper(config.input_dim, config.action_size)
        enemy_model.load(SAVES_DIR / 'enemy_model.pth')

        game_instance = Game(enemy_model)
        drawer = Drawer(self.screen)
        game_instance.set_drawer(drawer)
        start_time = datetime.datetime.now()
        game_instance.run()
        print("Обычная игра завершена.")
        if game_instance.win:
            self.show_temporary_message('Ты победил!', 1, 0.5)
            name = self.get_player_name_input()
            game_duration = datetime.timedelta.total_seconds(datetime.datetime.now() - start_time)
            records = RecordsModel()
            records.save(name, game_duration)
            print(name, game_duration)
        else:
            self.show_temporary_message('Ты проиграл(', 1, 0.5)

        pygame.mouse.set_visible(True)


    def run_debug_game(self):
        print("Запуск дебаг-игры...")
        config = DQNConfig()
        enemy_model = DQNWrapper(config.input_dim, config.action_size)
        enemy_model.load(SAVES_DIR / 'enemy_model.pth')
        game_instance = DebugGame(enemy_model)
        drawer = Drawer(self.screen)
        game_instance.set_drawer(drawer)
        game_instance.run()
        print("Дебаг-игра завершена.")


    def run_ai_training(self):
        print("Запуск тренировки AI...")
        config = DQNConfig()
        player_model = DQNWrapper(config.input_dim, config.action_size)
        player_model.load(SAVES_DIR / 'player_model.pth')

        enemy_model = DQNWrapper(config.input_dim, config.action_size)

        enemy_model.load(SAVES_DIR / 'enemy_model.pth')

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
        print("Тренировка AI завершена (или прервана).")