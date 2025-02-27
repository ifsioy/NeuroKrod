
import pygame
import math
from HyperParameters import W_SHIFT, H_SHIFT, BASE_SIZE, KEYS_NUMBER
from GameObject import GameObject
from SeeingObject import SeeingObject


class Player(SeeingObject):
    def __init__(self, x, y, width, height, speed):
        super(Player, self).__init__(x, y, width, height)
        self.speed = speed
        self.keys_collected = 0

    def move(self, items):
        keys = pygame.key.get_pressed()
        pressed_lr = False
        pressed_ud = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pressed_lr ^= True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            pressed_lr ^= True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            pressed_ud ^= True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            pressed_ud ^= True

        cur_speed = self.speed
        if pressed_lr and pressed_ud:
            cur_speed /= math.sqrt(2)

        # print(pressed_lr, ' ', pressed_ud, ' ', cur_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += cur_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= cur_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += cur_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= cur_speed

        for item in items:
            item.collision_check(self)

    def update(self, screen, camera, items):
        super(Player, self).update(screen, camera, items)
        self.draw(screen, camera)
        self.move(items)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, pygame.Color('red'),
                         pygame.Rect(camera.apply(self)))

        pygame.draw.circle(screen, pygame.Color('white'), (W_SHIFT + (self.x - camera.x) * BASE_SIZE,
                                                           H_SHIFT + (self.y - camera.y) * BASE_SIZE), BASE_SIZE)
