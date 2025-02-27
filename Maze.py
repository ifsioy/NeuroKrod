import random

from HyperParameters import WALL_PERCENT


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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

    def generate_maze(self):
        self.dfs(random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        area = (self.width - 1) * (self.height - 1)
        necessary_wall_number = area / 100 * WALL_PERCENT
        print(necessary_wall_number)

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

