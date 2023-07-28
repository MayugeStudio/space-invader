import math

import pygame

from entity import Entity
from constants import *


class Player(Entity):
    def __init__(self, image_path: str, image_size: tuple[int, int], position: tuple[int, int]) -> None:
        super().__init__(image_path, image_size, position)
        self.speed = 100
        self.direction = pygame.math.Vector2(0, 0)
    
    def update(self, dt: float) -> None:
        self.input()
        self.move(dt)

    def input(self) -> None:
        # 斜め移動はサポートしない
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
            return
        elif keys[pygame.K_s]:
            self.direction.y = 1
            return

        self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -1
            return
        elif keys[pygame.K_d]:
            self.direction.x = 1
            return
        else:
            self.direction.x = 0
    
    def move(self, dt: float) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt
        
        self.rect.centerx = math.floor(self.x)
        self.rect.centery = math.floor(self.y)