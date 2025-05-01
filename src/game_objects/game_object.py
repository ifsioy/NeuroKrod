from src.rendering.components.render_component import RenderComponent

class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.render_component = RenderComponent()
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True

    def physics_update(self, dt: float):
        pass
