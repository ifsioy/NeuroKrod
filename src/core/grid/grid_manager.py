from typing import List

from src.core.grid.cell import Cell
from src.game_objects.game_object import GameObject
from src.utils.hyper_parameters import CELL_WIDTH, CELL_HEIGHT


class GridManager:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    @staticmethod
    def world_to_grid(x: int, y: int) -> tuple:
        return (
            int((x + CELL_WIDTH // 2) // CELL_WIDTH),
            int((y + CELL_HEIGHT // 2) // CELL_HEIGHT)
        )

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return Cell(x, y)
        return self.grid[x][y]

    def remove(self, obj: GameObject):
        x, y = self.world_to_grid(obj.x, obj.y)
        self.get_cell(x, y).remove_object(obj)

    def add(self, obj: GameObject):
        x, y = self.world_to_grid(obj.x, obj.y)
        self.get_cell(x, y).add_object(obj)

    def get_cells_in_area(self, obj: GameObject, width: int, height: int) -> List[List[Cell]]:
        centre_x, centre_y = self.world_to_grid(obj.x, obj.y)
        return [[self.get_cell(x, y)
                for y in range(centre_y - height // 2, centre_y + height // 2 + 1)]
                for x in range(centre_x - width // 2, centre_x + width // 2 + 1)]