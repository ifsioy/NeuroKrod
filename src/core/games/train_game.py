import copy
from datetime import datetime

import pygame

from src.ai.models.dqn_model import DQNWrapper
from src.ai.rewards import RewardTracker
from src.ai.utils.config import DQNConfig
from src.ai.utils.state_encoder import StateEncoder
from src.core.collision_system import CollisionSystem
from src.core.controllers.ai_controller import AIController
from src.core.controllers.base_controller import BaseController
from src.core.controllers.game_controller import GameController
from src.core.controllers.player_controller import PlayerController
from src.core.controllers.rand_controller import RandController
from src.core.event_system import EventSystem, EventType
from src.core.games.game import Game
from src.core.grid.grid_manager import GridManager
from src.core.maze import Maze
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.player import Player
from src.rendering.camera import Camera
from src.utils.hyper_parameters import MAZE_SIZE, CELL_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, CELL_HEIGHT, PLAYER_WIDTH, \
    ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED


class TrainGame(Game):
    def __init__(self, player_model: DQNWrapper, enemy_model: DQNWrapper, config: DQNConfig):
        super().__init__()
        objects_to_add = list[GameObject]()
        self.game_objects = list[GameObject]()
        self.collision_system = CollisionSystem()
        self.event_system = EventSystem()
        self.event_system.subscribe(EventType.OBJECT_ADDED, self.collision_system.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.collision_system.on_object_removed)

        self.maze = Maze(MAZE_SIZE)
        for obj in self.maze.generate_maze():
            objects_to_add.append(obj)

        self.controllers = list[BaseController]()
        self.controllers.append(GameController(self))

        empty_cells = self.maze.find_empty_cells(objects_to_add)
        self.players = list[Player]()
        self.players.append(Player(empty_cells[0][1] * CELL_WIDTH, empty_cells[0][0] * CELL_HEIGHT,
                                   PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED))

        for player in self.players:
            objects_to_add.append(player)
            self.controllers.append(AIController(player, self.grid_manager, player_model, config, True))

        self.enemies = list[Enemy]()
        self.enemies.append(Enemy(empty_cells[-1][1] * CELL_WIDTH, empty_cells[-1][0] * CELL_HEIGHT,
                                  ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED))

        for enemy in self.enemies:
            objects_to_add.append(enemy)
            self.controllers.append(AIController(enemy, self.grid_manager, enemy_model, config, True))

        self.camera = Camera(self.players[0])
        self.drawer = None

        self.grid_manager = GridManager(MAZE_SIZE, MAZE_SIZE)
        for obj in objects_to_add:
            self.grid_manager.add(obj)

        for obj in objects_to_add:
            self.add_object(obj)

        self.events = []
        self.reward_tracker = RewardTracker()
        self.state_encoder = StateEncoder(self.grid_manager)

        self.is_running = True
        self.start_time = datetime.now()
        self.action = [0, 0]

    def get_player(self):
        return self.players[0]

    def get_enemy(self):
        return self.enemies[0]

    def get_rewards(self) -> tuple:
        return self.reward_tracker.calculate_rewards(self.get_player(), self.get_enemy(), self.events)

    def get_state(self) -> tuple:
        return self.state_encoder.encode(self.get_player()), self.state_encoder.encode(self.get_enemy())

    def get_action(self) -> tuple:
        return self.action[0], self.action[1]

    def step(self, dt: float):
        for obj in self.game_objects:
            self.grid_manager.remove(obj)

        for controller in self.controllers:
            action = controller.handle(self.events)

            if type(controller) == AIController:
                if type(controller.obj) == Enemy:
                    self.action[1] = action
                elif type(controller.obj) == Player:
                    self.action[0] = action

        for game_object in self.game_objects:
            game_object.physics_update(dt)

        for game_object in self.game_objects:
            if game_object.is_destroyed:
                self.remove_object(game_object)

        self.collision_system.check_collisions()
        for hole in self.maze.dig_holes(self.game_objects):
            self.add_object(hole)

        for obj in self.game_objects:
            self.grid_manager.add(obj)

        self.draw()
        self.events = pygame.event.get()
