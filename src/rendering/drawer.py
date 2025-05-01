import pygame

from src.game_objects.game_object import GameObject
from src.rendering.camera import Camera


class Drawer:
    def __init__(self, screen: pygame.Surface, camera: Camera):
        self.screen = screen
        self.camera = camera
        self.render_components = {}

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

    def draw_frame(self):
        self.camera.update()
        self.screen.fill((0, 0, 0))

        for component_type in sorted(self.render_components, key = lambda x: x.Z_ORDER):
            for obj in self.render_components[component_type]:
                pos = self.camera.world_to_screen(obj)
                obj.render_component.draw(self.screen, pos)

        pygame.display.flip()