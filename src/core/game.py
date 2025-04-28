from datetime import datetime

import pygame

from src.core.collision_system import CollisionSystem
from src.core.event_system import EventSystem, EventType
from src.game_objects.game_object import GameObject
from src.utils.hyper_parameters import *

from src.core.maze import Maze
from src.rendering.camera import Camera
from src.game_objects.player import Player

class Game:
    def __init__(self):
        self.game_objects = []
        self.is_running = True
        self.collision_system = CollisionSystem()
        self.event_system = EventSystem()
        self.event_system.subscribe(EventType.OBJECT_ADDED, self.collision_system.on_object_added)
        self.event_system.subscribe(EventType.OBJECT_REMOVED, self.collision_system.on_object_removed)

        self.maze = Maze(MAZE_SIZE)
        for obj in self.maze.generate_maze():
            self.add_object(obj)
        empty_cells = self.maze.find_empty_cells(self.game_objects)
        self.player = Player(empty_cells[0][1] * CELL_WIDTH, empty_cells[0][0] * CELL_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, CAST_COOLDOWN)
        self.add_object(self.player)
        self.camera = Camera(self.player.x, self.player.y, 0, 0)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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

    def draw(self, objects):
        if IS_TRAINING:
            return
        for game_object in objects:
            game_object.draw(self.screen, self.camera)

    def update(self):
        self.collision_system.check_collisions()
        self.draw(self.game_objects)

    def run(self):
        frames = 0
        last_time = datetime.now()
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            self.screen.fill(BLACK)

            for game_object in self.game_objects:
                game_object.update(self.game_objects)

            self.update()

            for game_object in self.game_objects:
                if game_object.is_destroyed:
                    self.remove_object(game_object)

            self.draw(self.game_objects)
            self.camera.update(self.screen, self.player)

            # print(player.x, player.y)
            if not IS_TRAINING:
                pygame.display.flip()

            for hole in self.maze.dig_holes(self.game_objects):
                self.add_object(hole)

            frames += 1
            if (datetime.now() - last_time).total_seconds() >= 1:
                print(frames)
                last_time = datetime.now()
                frames = 0

            if not IS_TRAINING:
                pygame.time.Clock().tick(100)