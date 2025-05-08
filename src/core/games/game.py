from datetime import datetime, timedelta

import pygame

from src.core.grid.grid_manager import GridManager
from src.core.collision_system import CollisionSystem
from src.core.controllers.base_controller import BaseController
from src.core.controllers.enemy_controller import EnemyController
from src.core.controllers.game_controller import GameController
from src.core.controllers.player_controller import PlayerController
from src.core.event_system import EventSystem, EventType
from src.core.games.base_game import BaseGame
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
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

        self.controllers = list[BaseController]()
        self.controllers.append(GameController(self))

        empty_cells = self.maze.find_empty_cells(objects_to_add)
        players = list[Player]()
        players.append(Player(empty_cells[0][1] * CELL_WIDTH, empty_cells[0][0] * CELL_HEIGHT,
                              PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED))

        for player in players:
            objects_to_add.append(player)
            self.controllers.append(PlayerController(player))

        enemies = list[Enemy]()
        enemies.append(Enemy(empty_cells[-1][1] * CELL_WIDTH, empty_cells[-1][0] * CELL_HEIGHT,
                             ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED))

        for enemy in enemies:
            objects_to_add.append(enemy)
            self.controllers.append(EnemyController(enemy))


        self.camera = Camera(players[0])
        self.drawer = None

        self.grid_manager = GridManager(MAZE_SIZE, MAZE_SIZE)
        for obj in objects_to_add:
            self.grid_manager.add(obj)

        for obj in objects_to_add:
            self.add_object(obj)

    def set_drawer(self, drawer):
        if self.drawer is not None:
            self.event_system.unsubscribe(EventType.OBJECT_ADDED, self.drawer.on_object_added)
            self.event_system.unsubscribe(EventType.OBJECT_REMOVED, self.drawer.on_object_added)
        self.drawer = drawer
        self.event_system.subscribe(EventType.OBJECT_ADDED, self.drawer.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.drawer.on_object_removed)
        self.drawer.set_camera(self.camera)
        for obj in self.game_objects:
            self.drawer.register_object(obj)

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

    def draw(self):
        if self.drawer is None:
            return
        self.drawer.draw_frame(self.grid_manager)

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

        self.draw()


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

            pygame.time.Clock().tick(15)