from typing import List, Dict, Type, Callable

import pygame

from src.game_objects.enemy import Enemy
from src.game_objects.game_object import GameObject
from src.game_objects.gates import Gates
from src.game_objects.hole import Hole
from src.game_objects.key import Key
from src.game_objects.movable import Movable
from src.game_objects.player import Player
from src.game_objects.wall import Wall
from src.utils.hyper_parameters import KEYS_NUMBER, CAUGHT, WIN, HOLE_USED, KEY_COLLECTED


class CollisionSystem:
    def __init__(self):
        self._collision_groups: Dict[Type[GameObject], List[GameObject]] = {
            Wall: [],
            Key: [],
            Hole: [],
            Player: [],
            Enemy: [],
            Gates: []
        }

        self._collision_handlers: Dict[tuple, Callable] = {
            (Player, Wall): self._handle_movable_wall,
            (Player, Key): self._handle_player_key,
            (Player, Hole): self._handle_player_hole,
            (Player, Gates): self._handle_player_gates,
            (Enemy, Player): self._handle_enemy_player,
            (Enemy, Wall): self._handle_movable_wall
        }

    def on_object_added(self, data : dict):
        obj = data['object']
        self.register_object(obj)

    def on_object_removed(self, data : dict):
        obj = data['object']
        self.unregister_object(obj)

    def register_object(self, obj: GameObject):
        for obj_type in self._collision_groups:
            if isinstance(obj, obj_type):
                self._collision_groups[obj_type].append(obj)
                break

    def unregister_object(self, obj: GameObject):
        for obj_type in self._collision_groups:
            if isinstance(obj, obj_type) and obj in self._collision_groups[obj_type]:
                self._collision_groups[obj_type].remove(obj)
                break

    @staticmethod
    def _get_object_bounds(obj: GameObject):
        half_w = obj.width / 2
        half_h = obj.height / 2
        return (
            obj.x - half_w,
            obj.x + half_w,
            obj.y - half_h,
            obj.y + half_h,
        )

    @staticmethod
    def _aabb_collision(a: GameObject, b: GameObject):
        a_left, a_right, a_top, a_bottom = CollisionSystem._get_object_bounds(a)
        b_left, b_right, b_top, b_bottom = CollisionSystem._get_object_bounds(b)
        return (a_left < b_right and
                a_right > b_left and
                a_top < b_bottom and
                a_bottom > b_top)

    @staticmethod
    def _ray_collision(a: GameObject, b: GameObject):
        a_left, a_right, a_top, a_bottom = CollisionSystem._get_object_bounds(a)
        b_left, b_right, b_top, b_bottom = CollisionSystem._get_object_bounds(b)

    def _resolve_collision(self, obj: GameObject, other: GameObject):
        handler = self._collision_handlers.get((type(obj), type(other)))
        if handler:
            handler(obj, other)

    def _check_collisions_for(self, obj: GameObject):
        for obj_type, objects in self._collision_groups.items():
            if obj_type == type(obj):
                continue

            for other in objects:
                if self._aabb_collision(obj, other):
                    self._resolve_collision(obj, other)

    def check_collisions(self):
        for player in self._collision_groups[Player]:
            self._check_collisions_for(player)

        for enemy in self._collision_groups[Enemy]:
            self._check_collisions_for(enemy)

    @staticmethod
    def _handle_movable_wall(obj: Movable, wall: Wall):
        p_left, p_right, p_top, p_bottom = CollisionSystem._get_object_bounds(obj)
        w_left, w_right, w_top, w_bottom = CollisionSystem._get_object_bounds(wall)

        overlap_x = min(p_right - w_left, w_right - p_left)
        overlap_y = min(p_bottom - w_top, w_bottom - p_top)

        if overlap_x < overlap_y:
            if p_right > w_left > p_left:
                obj.x = w_left - obj.width / 2
            else:
                obj.x = w_right + obj.width / 2
        else:
            if p_bottom > w_top > p_top:
                obj.y = w_top - obj.height / 2
            else:
                obj.y = w_bottom + obj.height / 2


    def _handle_player_key(self, player: Player, key: Key):
        if not key in self._collision_groups[Key]:
            return
        player.key_collected()
        key.destroy()
        pygame.event.post(KEY_COLLECTED)

    def _handle_player_hole(self, player: Player, hole: Hole):
        if not hole in self._collision_groups[Hole]:
            return
        hole.destroy()
        self._collision_groups[Hole].remove(hole)
        if len(self._collision_groups[Hole]) != 0:
            hole = self._collision_groups[Hole].pop(0)
            hole.destroy()
            player.x = hole.x
            player.y = hole.y
            pygame.event.post(HOLE_USED)
        else:
            print('OUT OF HOLES')

    def _handle_player_gates(self, player: Player, gates: Gates):
        if not gates in self._collision_groups[Gates]:
            return
        if player.keys_collected == KEYS_NUMBER:
            print('TRAVELING INTO THE DARK')
            pygame.event.post(WIN)

    @staticmethod
    def _handle_enemy_player(enemy: Enemy, player: Player):
        pygame.event.post(CAUGHT)

