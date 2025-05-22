from datetime import timedelta, datetime

import numpy as np
import pygame

from src.ai.utils.logs import Logs
from src.ai.utils.state_encoder import StateEncoder
from src.core.grid.grid_manager import GridManager
from src.game_objects.game_object import GameObject
from src.rendering.camera import Camera
from src.utils.hyper_parameters import CELL_WIDTH, CELL_HEIGHT, CELL_GRID, AREA_WIDTH, AREA_HEIGHT


class Drawer:
    def __init__(self, screen: pygame.Surface, camera: Camera = Camera(GameObject(0, 0, 0, 0))):
        self.screen = screen
        self.camera = camera
        self.render_components = {}
        self.is_disabled = False

    def set_camera(self, camera: Camera):
        self.camera = camera

    def register_object(self, obj: GameObject):
        if hasattr(obj, 'render_component'):
            component_type = type(obj.render_component)
            if component_type not in self.render_components:
                self.render_components[component_type] = []
            self.render_components[component_type].append(obj)

    def unregister_object(self, obj: GameObject):
        if hasattr(obj, 'render_component'):
            component_type = type(obj.render_component)
            if (component_type in self.render_components and
               obj in self.render_components[component_type]):
                self.render_components[component_type].remove(obj)

    def on_object_added(self, data : dict):
        obj = data['object']
        self.register_object(obj)

    def on_object_removed(self, data : dict):
        obj = data['object']
        self.unregister_object(obj)

    def draw_frame(self, dt, grid_manager: GridManager = None):
        if self.is_disabled:
            return
        self.camera.update(dt)
        self.screen.fill((100, 100, 100))

        for component_type in sorted(self.render_components, key = lambda x: x.Z_ORDER):
            for obj in self.render_components[component_type]:
                pos = self.camera.world_to_screen(obj)
                obj.render_component.draw(self.screen, pos)

        if grid_manager is not None:
            self._draw_debug_info(grid_manager)

        pygame.display.flip()

    def _draw_debug_info(self, grid_manager: GridManager):
        encoder = StateEncoder(grid_manager)
        encoder.encode(self.camera.target)
        return

        cells = grid_manager.get_cells_in_area(self.camera.target, AREA_WIDTH, AREA_HEIGHT)
        # sx, sy = cells[0].x * CELL_WIDTH, cells[0].y * CELL_HEIGHT
        sx, sy = 1 * CELL_WIDTH, 1 * CELL_HEIGHT

        encoder = StateEncoder(grid_manager)
        player_smell, enemy_smell, key, hole, wall, gate, player, enemy = encoder.encode(self.camera.target)


        w = AREA_WIDTH * CELL_GRID
        h = AREA_WIDTH * CELL_GRID

        for x in range(w):
            for y in range(h):
                text = f'{enemy_smell[x * w + y]:.1f}'
                obj = GameObject(sx + x * CELL_WIDTH // CELL_GRID + CELL_WIDTH // CELL_GRID // 2,
                                 sy + y * CELL_HEIGHT // CELL_GRID + CELL_HEIGHT // CELL_GRID // 2,
                                 CELL_WIDTH, CELL_HEIGHT)
                pos = self.camera.world_to_screen(obj)
                font = pygame.font.Font(None, 20)
                text_surface = font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.center = (pos[0], pos[1])
                self.screen.blit(text_surface, text_rect)

        # for cell in cells:
        #     objects = [t.__name__ for t in cell.objects.keys()]
        #
        #     for x in range(CELL_GRID):
        #         for y in range(CELL_GRID):
        #             time_str_sec = str(timedelta.total_seconds(datetime.now() - cell.last_enemy_visit[x][y]))
        #
        #             text = f"{time_str_sec}"
        #
        #             font = pygame.font.Font(None, 20)
        #             text_surface = font.render(text, True, (255, 255, 255))
        #             text_rect = text_surface.get_rect()
        #             obj = GameObject(CELL_WIDTH * cell.x + x * CELL_WIDTH // CELL_GRID + CELL_WIDTH // CELL_GRID // 2,
        #                              CELL_HEIGHT * cell.y + y * CELL_HEIGHT // CELL_GRID + CELL_HEIGHT // CELL_GRID // 2,
        #                              CELL_WIDTH, CELL_HEIGHT)
        #
        #             pos = self.camera.world_to_screen(obj)
        #             text_rect.center = (pos[0], pos[1])
        #
        #             self.screen.blit(text_surface, text_rect)