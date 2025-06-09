import pygame

from src.rendering.sprite_loader import SpriteLoader
from src.utils.constants import ENEMY_WIDTH, ENEMY_HEIGHT, GATES_WIDTH, GATES_HEIGHT, HOLE_WIDTH, \
    KEY_HEIGHT, HOLE_HEIGHT, KEY_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, CELL_WIDTH, CELL_HEIGHT, SCREEN_WIDTH, \
    SCREEN_HEIGHT, ANIMATIONS_DIR

# SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

ENEMY_RUN_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'enemy'), ENEMY_WIDTH, ENEMY_HEIGHT)
GATES_CLOSED_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'gates' / 'closed'), GATES_WIDTH, GATES_HEIGHT + 2)
GATES_OPENED_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'gates' / 'opened'), GATES_WIDTH, GATES_HEIGHT + 2)
HOLE_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'hole'), HOLE_WIDTH, HOLE_HEIGHT)
KEY_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'key'), KEY_WIDTH, KEY_HEIGHT)
PLAYER_IDLE_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'player' / 'idle'), PLAYER_WIDTH, PLAYER_HEIGHT)
PLAYER_RUN_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'player' / 'run'), PLAYER_WIDTH, PLAYER_HEIGHT)
WALL_ANIMATION = SpriteLoader.load_animation(str(ANIMATIONS_DIR / 'wall'), CELL_WIDTH, CELL_HEIGHT + 2)
FLOOR_ANIMATION = SpriteLoader.load_sprite(ANIMATIONS_DIR / 'floor' / 'floor.png', CELL_WIDTH, CELL_HEIGHT)