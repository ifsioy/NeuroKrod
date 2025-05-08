
from src.core.games.game import Game


class DebugGame(Game):
    def draw(self):
        self.drawer.draw_frame(self.grid_manager)
