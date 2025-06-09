from src.ai.models.dqn_model import DQNWrapper
from src.core.controllers.rand_controller import RandController
from src.core.games.game import Game
from src.game_objects.enemy import Enemy


class DebugGame(Game):

    def __init__(self, enemy_model: DQNWrapper):
        super().__init__(enemy_model)

        for i in range(len(self.controllers)):
            if hasattr(self.controllers[i], 'obj') and type(self.controllers[i].obj) is Enemy:
                self.controllers[i] = RandController(self.controllers[i].obj)

    def draw(self, dt):
        self.drawer.draw_frame(dt, self.grid_manager)
