from datetime import datetime, timedelta

import pygame

from src.ai.grid.grid_manager import GridManager
from src.core.collision_system import CollisionSystem
from src.core.controllers.base_controller import BaseController
from src.core.controllers.game_controller import GameController
from src.core.controllers.player_controller import PlayerController
from src.core.event_system import EventSystem, EventType
from src.core.games.base_game import BaseGame
from src.game_objects.game_object import GameObject
from src.rendering.drawer import Drawer
from src.utils.hyper_parameters import *

from src.core.maze import Maze
from src.rendering.camera import Camera
from src.game_objects.player import Player

class Game(BaseGame):
    def __init__(self):
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

        empty_cells = self.maze.find_empty_cells(objects_to_add)
        players = list[Player]()
        players.append(Player(empty_cells[0][1] * CELL_WIDTH, empty_cells[0][0] * CELL_HEIGHT,
                                   PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED))

        self.controllers = list[BaseController]()
        self.controllers.append(GameController(self))
        for player in players:
            objects_to_add.append(player)
            self.controllers.append(PlayerController(player))

        self.camera = Camera(players[0])

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.drawer = Drawer(self.screen, self.camera)
        self.event_system.subscribe(EventType.OBJECT_ADDED, self.drawer.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.drawer.on_object_removed)

        self.grid_manager = GridManager(MAZE_SIZE, MAZE_SIZE)
        for obj in objects_to_add:
            self.grid_manager.add(obj)

        for obj in objects_to_add:
            self.add_object(obj)

    def _cleanup_objects(self):
        for obj in self.game_objects[:]:
            if obj.is_destroyed:
                self.remove_object(obj)

    def add_object(self, obj: GameObject):
        self.game_objects.append(obj)
        self.event_system.notify(EventType.OBJECT_ADDED, {'object' : obj})

    def remove_object(self, obj: GameObject):
        if not obj in self.game_objects:
            return
        self.game_objects.remove(obj)
        self.event_system.notify(EventType.OBJECT_REMOVED, {'object' : obj})

    def update(self, dt: float):
        for obj in self.game_objects:
            self.grid_manager.remove(obj)

        events = pygame.event.get()
        for controller in self.controllers:
            controller.handle_input(events)

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


        for x in range(MAZE_SIZE):
            for y in range(MAZE_SIZE):
                cell = self.grid_manager.get_cell(x, y)


        self.drawer.draw_frame()

    def run(self):
        self.is_running = True
        fps = 0
        tm = 0
        last_time = datetime.now()
        while self.is_running:
            dt = timedelta.total_seconds(datetime.now() - last_time)
            last_time = datetime.now()
            self.update(dt)

            fps += 1
            tm += dt
            if tm > 1:
                print(fps)
                tm = 0
                fps = 0

            # if not IS_TRAINING:
            #     pygame.time.Clock().tick(100)