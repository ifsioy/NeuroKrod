import random
from typing import List

from src.game_objects.game_object import GameObject
from src.game_objects.gates import Gates
from src.game_objects.hole import Hole
from src.game_objects.key import Key
from src.game_objects.wall import Wall
from src.utils.hyper_parameters import WALL_PERCENT, CELL_WIDTH, CELL_HEIGHT, HOLE_WIDTH, HOLE_HEIGHT, HOLES_NUMBER, \
    KEYS_NUMBER, KEY_WIDTH, KEY_HEIGHT, GATES_HEIGHT, GATES_WIDTH


class Maze:
    def __init__(self, size):
        self.width = size
        self.height = size
        self.maze = [['#' for _ in range(self.width)] for _ in range(self.height)]

    def empty_neighbours(self, x, y):
        order = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        result = 0
        for step in order:
            if x + step[0] < 0 or x + step[0] >= self.width or y + step[1] < 0 or y + step[1] >= self.height:
                continue
            if self.maze[x + step[0]][y + step[1]] == ' ':
                result += 1
        return result

    def dfs(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        order = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        random.shuffle(order)
        wall_number = 0
        for step in order:
            if x + step[0] < 0 or x + step[0] >= self.width or y + step[1] < 0 or y + step[1] >= self.height:
                continue
            if self.maze[x + step[0]][y + step[1]] == '#':
                wall_number += 1

        if wall_number < 3:
            return False

        self.maze[x][y] = ' '
        for step in order:
            self.dfs(x + step[0], y + step[1])

    def find_empty_cells(self, game_objects: List[GameObject]):
        occupied_cells = set()
        for obj in game_objects:
            column = obj.x // CELL_WIDTH
            row = obj.y // CELL_HEIGHT
            if 0 <= row < self.width and 0 <= column < self.height:
                occupied_cells.add((row, column))

        empty_cells = []
        for row in range(self.width):
            for column in range(self.height):
                if (row, column) not in occupied_cells:
                    empty_cells.append((row, column))

        return empty_cells

    def dig_holes(self, game_objects: List[GameObject]) -> List[GameObject]:
        hole_num = 0
        for obj in game_objects:
            if type(obj) is Hole:
                hole_num = hole_num + 1

        if hole_num >= HOLES_NUMBER:
            return []

        empty_cells = self.find_empty_cells(game_objects)

        random.shuffle(empty_cells)
        holes = []
        for i in range(len(empty_cells)):
            if hole_num >= HOLES_NUMBER:
                break
            cell = GameObject(empty_cells[i][1] * CELL_WIDTH, empty_cells[i][0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            hole = Hole(cell.x - cell.width / 2 + CELL_WIDTH / 3 * random.randint(0, 2) + CELL_WIDTH / 6,
                        cell.y - cell.height / 2 + CELL_HEIGHT / 3 * random.randint(0, 2) + CELL_HEIGHT / 6,
                        HOLE_WIDTH, HOLE_HEIGHT)

            if not hole in game_objects:
                hole_num = hole_num + 1
                holes.append(hole)

        return holes

    def generate_maze(self):
        self.dfs(random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        area = (self.width - 1) * (self.height - 1)
        necessary_wall_number = 0 #area / 100 * WALL_PERCENT
        # print("CIELI", necessary_wall_number)

        wall_pieces = []
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if self.maze[i][j] == '#':
                    wall_pieces.append([i, j])

        random.shuffle(wall_pieces)

        while len(wall_pieces) > necessary_wall_number:
            if self.empty_neighbours(wall_pieces[0][0], wall_pieces[0][1]) > 0:
                self.maze[wall_pieces[0][0]][wall_pieces[0][1]] = ' '
                wall_pieces.pop(0)
            else:
                random.shuffle(wall_pieces)

        game_objects = list()
        walls = list()
        empty_cells = list()
        for i in range(self.width):
            for j in range(self.height):
                if self.maze[i][j] == '#':
                    walls.append(Wall(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                else:
                    empty_cells.append(GameObject(j * CELL_WIDTH, i * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

        random.shuffle(empty_cells)
        keys = list()
        for i in range(KEYS_NUMBER):
            cell = empty_cells[0]
            keys.append(Key(cell.x - cell.width / 2 + CELL_WIDTH / 3 * random.randint(0, 2) + CELL_WIDTH / 6,
                                 cell.y - cell.height / 2 + CELL_HEIGHT / 3 * random.randint(0, 2) + CELL_HEIGHT / 6,
                                 KEY_WIDTH, KEY_HEIGHT))
            empty_cells.pop(0)

        gates = list()
        for cell in empty_cells:
            if self.maze[cell.y // CELL_HEIGHT - 1][cell.x // CELL_WIDTH] == '#':
                gates.append(Gates(cell.x, cell.y - cell.height / 2 + GATES_HEIGHT / 2, GATES_WIDTH, GATES_HEIGHT))
                empty_cells.remove(cell)
                break

        game_objects.extend(walls)
        game_objects.extend(keys)
        game_objects.extend(gates)
        game_objects.extend(self.dig_holes(game_objects))

        return game_objects

