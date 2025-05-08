from datetime import datetime, timedelta

import pygame

from src.ai.grid.grid_manager import GridManager
from src.game_objects.game_object import GameObject
from src.rendering.camera import Camera
from src.utils.hyper_parameters import CELL_WIDTH, CELL_HEIGHT, BASE_SIZE


class Drawer:
    def __init__(self, screen: pygame.Surface, camera: Camera = Camera(GameObject(0, 0, 0, 0))):
        self.screen = screen
        self.camera = camera
        self.render_components = {}

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

    def draw_frame(self, grid_manager: GridManager = None):
        self.camera.update()
        self.screen.fill((0, 0, 0))

        for component_type in sorted(self.render_components, key = lambda x: x.Z_ORDER):
            for obj in self.render_components[component_type]:
                pos = self.camera.world_to_screen(obj)
                obj.render_component.draw(self.screen, pos)

        if grid_manager is not None:
            self._draw_debug_info(grid_manager)

        pygame.display.flip()

    def _draw_debug_info(self, grid_manager: GridManager):
        for x in range(grid_manager.width):
            for y in range(grid_manager.height):
                cell = grid_manager.get_cell(x, y)

                objects = [t.__name__ for t in cell.objects.keys()]
                time_str = str(cell.last_player_visit.hour) + ' '
                time_str += str(cell.last_player_visit.minute) + ' '
                time_str += str(cell.last_player_visit.second) + ' '
                time_str += str(cell.last_player_visit.microsecond)

                text = f"{time_str}"

                font = pygame.font.Font(None, 20)
                text_surface = font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                obj = GameObject(CELL_WIDTH * x + CELL_WIDTH // 2,
                                 CELL_HEIGHT * y + CELL_HEIGHT // 2,
                                 CELL_WIDTH, CELL_HEIGHT)

                pos = self.camera.world_to_screen(obj)
                text_rect.center = (pos[0], pos[1])

                self.screen.blit(text_surface, text_rect)