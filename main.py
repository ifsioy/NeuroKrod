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

sys.setrecursionlimit(10**9)

def dig_holes(empty_cells, holes):
    random.shuffle(empty_cells)
    for i in range(len(empty_cells)):
        if len(holes) == HOLES_NUMBER:
            break
        cell = empty_cells[i]
        hole = Hole(cell.x - cell.width / 2 + CELL_WIDTH / 3 * random.randint(0, 2) + CELL_WIDTH / 6,
                          cell.y - cell.height / 2 + CELL_HEIGHT / 3 * random.randint(0, 2) + CELL_HEIGHT / 6,
                          HOLE_WIDTH, HOLE_HEIGHT)

        if not hole in holes:
            holes.append(hole)

maze = Maze(MAZE_SIZE, MAZE_SIZE)
maze.generate_maze()
for line in maze.maze:
    print(line)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

walls = list()
empty_cells = list()
for i in range(maze.width):
    for j in range(maze.height):
        if maze.maze[i][j] == '#':
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

gates = Gates
for cell in empty_cells:
    if maze.maze[cell.y // CELL_HEIGHT - 1][cell.x // CELL_WIDTH] == '#':
        gates = Gates(cell.x, cell.y - cell.height / 2 + GATES_HEIGHT / 2, GATES_WIDTH, GATES_HEIGHT)
        empty_cells.remove(cell)
        break

holes = list()
dig_holes(empty_cells, holes)

player = Player(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED)
for i in range(maze.width):
    for j in range(maze.height):
        if maze.maze[i][j] == ' ':
            player.x = j * CELL_WIDTH
            player.y = i * CELL_HEIGHT
            break
    else:
        continue
    break

camera = Camera(player.x, player.y, 0, 0)

all_objects = list(walls)
all_objects.extend(keys)
all_objects.extend(holes)
all_objects.append(gates)
all_objects.append(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)

    # print(len(all_objects), player.keys_collected)

    objects_to_delete = list()
    for game_object in all_objects:
        game_object.update(screen, camera, all_objects)
        if type(game_object) == Key and game_object.collected:
            player.keys_collected += 1
            objects_to_delete.append(game_object)
            keys.remove(game_object)
            continue
        if type(game_object) == Hole and game_object.used:
            objects_to_delete.append(game_object)
            holes.remove(game_object)
            if len(holes) != 0:
                hole = holes.pop(0)
                objects_to_delete.append(hole)
                player.x = hole.x
                player.y = hole.y
            else:
                print('OUT OF HOLES')

            continue

    for game_object in objects_to_delete:
        all_objects.remove(game_object)

    camera.update(screen, player)

    # print(player.x, player.y)

    pygame.display.flip()

    if len(holes) < HOLES_NUMBER:
        dig_holes(empty_cells, holes)
        for hole in holes:
            if not hole in all_objects:
                all_objects.append(hole)


    pygame.time.Clock().tick(100)

pygame.quit()