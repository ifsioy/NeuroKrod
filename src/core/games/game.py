import os
from datetime import datetime, timedelta
import random

from gameobjects_serializer import save_game_objects, load_game_objects

from src.ai.models.dqn_model import DQNWrapper
from src.ai.utils.config import DQNConfig
from src.core.controllers.ai_controller import AIController
from src.core.grid.grid_manager import GridManager
from src.core.collision_system import CollisionSystem
from src.core.controllers.base_controller import BaseController
from src.core.controllers.rand_controller import RandController
from src.core.controllers.game_controller import GameController
from src.core.controllers.player_controller import PlayerController
from src.core.event_system import EventSystem, EventType
from src.core.games.base_game import BaseGame
from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.key import Key
from src.rendering.drawer import Drawer
from src.utils.constants import *

from src.core.maze import Maze
from src.rendering.camera import Camera
from src.game_objects.player import Player

class Game(BaseGame):
    def __init__(self, enemy_model: DQNWrapper):
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
        random.shuffle(empty_cells)
        self.players = list[Player]()
        self.players.append(Player(empty_cells[0][0] * CELL_WIDTH, empty_cells[0][1] * CELL_HEIGHT,
                              PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED))


        self.enemies = list[Enemy]()
        self.enemies.append(Enemy(empty_cells[-1][0] * CELL_WIDTH, empty_cells[-1][1] * CELL_HEIGHT,
                             ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED))


        self.camera = Camera(self.players[0])
        self.drawer = None

        self.grid_manager = GridManager(MAZE_SIZE, MAZE_SIZE)

        self.event_system.subscribe(EventType.OBJECT_ADDED, self.grid_manager.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.grid_manager.on_object_removed)

        for player in self.players:
            objects_to_add.append(player)
            self.controllers.append(PlayerController(player))
        for enemy in self.enemies:
            objects_to_add.append(enemy)
            config = DQNConfig()
            self.controllers.append(AIController(enemy, self.grid_manager, enemy_model, config))

        for obj in objects_to_add:
            self.add_object(obj)

        self.events = []

        self.enemy_model = enemy_model
        self.is_running = True
        self.win = False
        self.start_time = datetime.now()

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

    def draw(self, dt):
        if self.drawer is None:
            return

        self.drawer.draw_frame(dt)

    def handle_events(self):
        for controller in self.controllers:
            controller.handle(self.events)

    def update_events(self):
        self.events = pygame.event.get()
        st = set()
        for event in self.events:
            if not event.dict:
                st.add(event.type)
            else:
                pygame.event.post(event)

        for event in st:
            pygame.event.post(pygame.event.Event(event))

        self.events = pygame.event.get()

    def step(self, dt: float):
        self.handle_events()

        for enemy in self.enemies:
            self.grid_manager.remove(enemy)
        for player in self.players:
            self.grid_manager.remove(player)

        t = 0
        while t < dt:
            for game_object in self.game_objects:
                game_object.physics_update(min(UT, dt - t))
            t += UT
            self.collision_system.check_collisions()
            for game_object in self.game_objects:
                if game_object.is_destroyed:
                    self.remove_object(game_object)

            for hole in self.maze.dig_holes(self.game_objects):
                self.add_object(hole)

        for enemy in self.enemies:
            self.grid_manager.add(enemy)
        for player in self.players:
            self.grid_manager.add(player)

        self.update_events()

        self.draw(dt)

    def run(self):
        self.is_running = True
        fps = 0
        tm = 0
        last_time = datetime.now()
        while self.is_running:
            dt = timedelta.total_seconds(datetime.now() - last_time)
            last_time = datetime.now()
            self.step(dt)

            fps += 1
            tm += dt
            if tm > 1:
                print(fps)
                tm = 0
                fps = 0

            # pygame.time.Clock().tick(15)

        if os.path.exists(STATE_SAVE_DIR):
            os.remove(STATE_SAVE_DIR)

    def save(self, path = STATE_SAVE_DIR, fmt='json'):
        save_game_objects(self.game_objects, path, fmt)

    def load(self, path = STATE_SAVE_DIR, fmt='json'):
        if not os.path.exists(path):
            print('Save file doesnt exist')
            return

        objects_to_add = load_game_objects(path, fmt)

        self.game_objects = list[GameObject]()
        self.collision_system = CollisionSystem()
        self.event_system = EventSystem()
        self.event_system.subscribe(EventType.OBJECT_ADDED, self.collision_system.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.collision_system.on_object_removed)

        self.controllers = list[BaseController]()
        self.controllers.append(GameController(self))

        empty_cells = self.maze.find_empty_cells(objects_to_add)
        random.shuffle(empty_cells)
        self.players = list[Player]()
        self.enemies = list[Enemy]()

        keys_collected = KEYS_NUMBER

        for obj in objects_to_add:
            if type(obj) is Player:
                self.players.append(obj)
            elif type(obj) is Enemy:
                self.enemies.append(obj)
            elif type(obj) is Key:
                keys_collected -= 1

        self.camera = Camera(self.players[0])
        self.set_drawer(Drawer(self.drawer.screen))

        self.grid_manager = GridManager(MAZE_SIZE, MAZE_SIZE)

        self.event_system.subscribe(EventType.OBJECT_ADDED, self.grid_manager.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.grid_manager.on_object_removed)

        for player in self.players:
            player.keys_collected = keys_collected
            self.controllers.append(PlayerController(player))
        for enemy in self.enemies:
            config = DQNConfig()
            self.controllers.append(AIController(enemy, self.grid_manager, self.enemy_model, config))

        for obj in objects_to_add:
            self.add_object(obj)

        self.events = []

        self.is_running = True
        self.win = False