import pygame
import pytest
from src.core.collision_system import CollisionSystem
from src.game_objects.game_object import GameObject
from src.game_objects.wall import Wall
from src.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

@pytest.fixture
def collision_system():
    return CollisionSystem()

def test_aabb_collision_when_colliding(collision_system):
    obj_a = GameObject(x=0, y=0, width=10, height=10)
    obj_b = GameObject(x=5, y=5, width=10, height=10)
    assert collision_system._aabb_collision(obj_a, obj_b) == True

def test_aabb_collision_when_not_colliding(collision_system):
    obj_a = GameObject(x=0, y=0, width=10, height=10)
    obj_b = GameObject(x=20, y=20, width=10, height=10)
    assert collision_system._aabb_collision(obj_a, obj_b) == False

def test_aabb_collision_when_touching_edges(collision_system):
    obj_a = GameObject(x=0, y=0, width=10, height=10)
    obj_b = GameObject(x=10, y=0, width=10, height=10)
    assert collision_system._aabb_collision(obj_a, obj_b) == False

def test_aabb_collision_when_one_contains_another(collision_system):
    obj_a = GameObject(x=0, y=0, width=20, height=20)
    obj_b = GameObject(x=5, y=5, width=5, height=5)
    assert collision_system._aabb_collision(obj_a, obj_b) == True

def test_aabb_collision_with_identical_objects_at_same_position(collision_system):
    obj_a = GameObject(x=0, y=0, width=10, height=10)
    obj_b = GameObject(x=0, y=0, width=10, height=10)
    assert collision_system._aabb_collision(obj_a, obj_b) == True

def test_register_single_player_object(collision_system):
    wall = Wall(x=0, y=0, width=10, height=10)
    collision_system.register_object(wall)
    assert wall in collision_system._collision_groups[Wall]
    assert len(collision_system._collision_groups[Wall]) == 1

def test_register_multiple_objects_same_type(collision_system):
    wall1 = Wall(x=0, y=0, width=10, height=10)
    wall2 = Wall(x=20, y=0, width=10, height=10)
    collision_system.register_object(wall1)
    collision_system.register_object(wall2)
    assert wall1 in collision_system._collision_groups[Wall]
    assert wall2 in collision_system._collision_groups[Wall]
    assert len(collision_system._collision_groups[Wall]) == 2

