from pathlib import Path

import pygame

ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / 'assets'
ANIMATIONS_DIR = ASSETS_DIR / 'animations'
SAVES_DIR = ROOT_DIR / 'data'/ 'model_saves'

STATE_SAVE_DIR = ROOT_DIR / 'data/state_saves/save.json'

BASE_SIZE = 15

CELL_WIDTH = 30
CELL_HEIGHT = 30
CELL_GRID = 3

pygame.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 1500

W_SHIFT = SCREEN_WIDTH // 2
H_SHIFT = SCREEN_HEIGHT // 2

#MOVABLE
COLLISION_SPEED_MOVEMENT = 3

PLAYER_SPEED = 50
PLAYER_WIDTH = CELL_WIDTH // 5
PLAYER_HEIGHT = CELL_HEIGHT // 4

ENEMY_SPEED = PLAYER_SPEED * 1.1
ENEMY_WIDTH = CELL_WIDTH // 3
ENEMY_HEIGHT = CELL_HEIGHT // 3

CAST_COOLDOWN = 0

MAZE_SIZE = 15
WALL_PERCENT = 25

KEYS_NUMBER = 5
KEY_WIDTH = CELL_WIDTH // 4
KEY_HEIGHT = CELL_HEIGHT // 4

GATES_WIDTH = CELL_WIDTH // 3
GATES_HEIGHT = CELL_HEIGHT // 5

HOLES_NUMBER = 4
HOLE_WIDTH = CELL_WIDTH // 4
HOLE_HEIGHT = CELL_HEIGHT // 4

CAMERA_WIDTH = CELL_WIDTH // 6
CAMERA_HEIGHT = CELL_HEIGHT // 6
CAMERA_SMOOTHNESS = 4

RAYS_NUMBER = 16


CAUGHT_EVENT        = pygame.USEREVENT + 1
WIN_EVENT           = pygame.USEREVENT + 2
KEY_COLLECTED_EVENT = pygame.USEREVENT + 3
HOLE_USED_EVENT     = pygame.USEREVENT + 4



CAUGHT        = pygame.event.Event(pygame.USEREVENT + 1)
WIN           = pygame.event.Event(pygame.USEREVENT + 2)
KEY_COLLECTED = pygame.event.Event(pygame.USEREVENT + 3)
HOLE_USED     = pygame.event.Event(pygame.USEREVENT + 4)


AREA_WIDTH = 3
AREA_HEIGHT = 3

SMELL_CONST = 0.85

GAME_DURATION = 30
TRAINING_FPS = 3
TRAINING_DT = 1 / TRAINING_FPS
GAME_COUNT = 16

LOG_SIZE = 1000
LOG_PERIOD = 100
LOG_DRAW_PERIOD = 2000


COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BROWN = (88, 57, 79)
COLOR_YELLOW = (255, 210, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_VIOLET = (191, 5, 247)
COLOR_DARK_GREY = (20, 20, 20)
COLOR_LIGHTER_GREY = (50, 50, 50)
COLOR_TEXT = (220, 220, 220)
COLOR_BORDER = (80, 80, 80)
COLOR_GREEN = (0, 200, 0)

FRAME_DURATION = 0.1
UPS = 60
UT = 1 / UPS

IS_TRAINING = False