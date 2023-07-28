import math

import pygame

from entity import Entity
from constants import *


class Player(Entity):
    def __init__(self, image_path: str, image_size: tuple[int, int], position: tuple[int, int]) -> None:
        super().__init__(image_path, image_size, position)
        self.speed = 100
        self.direction = pygame.math.Vector2(0, 0)
        self.missile_cooldown = 0.5
    
    def update(self, dt: float) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt
        
        self.rect.centerx = math.floor(self.x)
        self.rect.centery = math.floor(self.y)

        self.missile_cooldown -= dt

    def can_shoot(self) -> bool:
        return self.missile_cooldown <= 0