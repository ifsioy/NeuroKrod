import sys
import pygame
import random

from GameObject import GameObject
from HyperParameters import *

from Wall import Wall
from Maze import Maze
from Camera import Camera
from Player import Player
from Key import Key
from Gates import Gates
from Hole import Hole

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
        self.maze = Maze(MAZE_SIZE, MAZE_SIZE)
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
        dig_holes(self.empty_cells, self.holes)