
from src.core.games.game import Game


class DebugGame(Game):
    def draw(self, dt):
        self.drawer.draw_frame(dt, self.grid_manager)
