from src.core.controllers.base_controller import BaseController
from src.core.grid.grid_manager import GridManager


class AIController(BaseController):
    def __init__(self):
        super().__init__()
        self.grid_manager = None

    def set_grid_manager(self, grid_manager: GridManager):
        self.grid_manager = grid_manager