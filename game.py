from datetime import datetime
from typing import Any

import pygame
import random

from game_object import GameObject
from hyper_parameters import *

from wall import Wall
from maze import Maze
from camera import Camera
from player import Player
from key import Key
from gates import Gates
from hole import Hole

class Game:
    def dig_holes(self):
        random.shuffle(self.empty_cells)
        for i in range(len(self.empty_cells)):
            if len(self.holes) == HOLES_NUMBER:
                break
            cell = self.empty_cells[i]
            hole = Hole(cell.x - cell.width / 2 + CELL_WIDTH / 3 * random.randint(0, 2) + CELL_WIDTH / 6,
                        cell.y - cell.height / 2 + CELL_HEIGHT / 3 * random.randint(0, 2) + CELL_HEIGHT / 6,
                        HOLE_WIDTH, HOLE_HEIGHT)

            if not hole in self.holes:
                self.holes.append(hole)

    def __init__(self):
        self.maze = Maze(MAZE_SIZE)
        self.maze.generate_maze()
        for line in self.maze.maze:
            print(line)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.walls = list()
        self.empty_cells = list()
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                if self.maze.maze[i][j] == '#':
                    self.walls.append(Wall(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                else:
                    self.empty_cells.append(GameObject(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

        random.shuffle(self.empty_cells)
        self.keys = list()
        for i in range(KEYS_NUMBER):
            cell = self.empty_cells[0]
            self.keys.append(Key(cell.x - cell.width / 2 + CELL_WIDTH / 3 * random.randint(0, 2) + CELL_WIDTH / 6,
                            cell.y - cell.height / 2 + CELL_HEIGHT / 3 * random.randint(0, 2) + CELL_HEIGHT / 6,
                            KEY_WIDTH, KEY_HEIGHT))
            self.empty_cells.pop(0)

        self.gates = Gates
        for cell in self.empty_cells:
            if self.maze.maze[cell.y // CELL_HEIGHT - 1][cell.x // CELL_WIDTH] == '#':
                self.gates = Gates(cell.x, cell.y - cell.height / 2 + GATES_HEIGHT / 2, GATES_WIDTH, GATES_HEIGHT)
                self.empty_cells.remove(cell)
                break

        self.holes = list()
        self.dig_holes()

        self.player = Player(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED)
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                if self.maze.maze[i][j] == ' ':
                    self.player.x = j * CELL_WIDTH
                    self.player.y = i * CELL_HEIGHT
                    break
            else:
                continue
            break

        self.camera = Camera(self.player.x, self.player.y, 0, 0)

        self.all_objects : list[Any] = self.walls
        self.all_objects.extend(self.keys)
        self.all_objects.extend(self.holes)
        self.all_objects.append(self.gates)
        self.all_objects.append(self.player)

    def draw(self, objects):
        for game_object in objects:
            game_object.draw(self.screen, self.camera)

    def run(self):
        running = True
        frames = 0
        start = datetime.now()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(BLACK)

            self.draw(self.all_objects)

            objects_to_delete = list()
            for game_object in self.all_objects:
                game_object.update(self.all_objects)
                if type(game_object) == Key and game_object.collected:
                    self.player.keys_collected += 1
                    objects_to_delete.append(game_object)
                    self.keys.remove(game_object)
                    continue
                if type(game_object) == Hole and game_object.used:
                    objects_to_delete.append(game_object)
                    self.holes.remove(game_object)
                    if len(self.holes) != 0:
                        hole = self.holes.pop(0)
                        objects_to_delete.append(hole)
                        self.player.x = hole.x
                        self.player.y = hole.y
                    else:
                        print('OUT OF HOLES')

                    continue


            for game_object in objects_to_delete:
                self.all_objects.remove(game_object)

            self.camera.update(self.screen, self.player)

            # print(player.x, player.y)

            pygame.display.flip()

            if len(self.holes) < HOLES_NUMBER:
                self.dig_holes()
                for hole in self.holes:
                    if not hole in self.all_objects:
                        self.all_objects.append(hole)

            pygame.time.Clock().tick(100)
            frames += 1
            fps = frames / (datetime.now() - start).total_seconds()
            print(fps)

        pygame.quit()