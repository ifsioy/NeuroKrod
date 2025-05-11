from typing import List

import pygame


class BaseController:
    def __init__(self):
        pass

    def handle(self, events: List[pygame.event.Event]):
        pass

    def update(self):
        pass