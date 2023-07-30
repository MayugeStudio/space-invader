from __future__ import annotations

import math

import pygame

from dataclasses import dataclass
from enemy import Enemy

from entity import Entity

from utils import load_image


class Missile(Entity):
    def __init__(
        self,
        prototype: MissilePrototype,
        position: tuple[float, float],
        team: str,
        ) -> None:
        position = int(position[0]), int(position[1])
        super().__init__("", prototype.image_size, position, image=prototype.image)
        self.team = team
        self.direction = pygame.Vector2(0, -1) if team == "player" else pygame.Vector2(0, 1)
        self.speed = prototype.speed
    
    def update(self, dt: float) -> None:
        self.rect.y += self.direction.y * self.speed * dt


class HomingMissile(Missile):
    def __init__(self, prototype: MissilePrototype, position: tuple[float, float], team: str, target: Enemy) -> None:
        super().__init__(prototype, position, team)
        self.target = target
    
    def update(self, dt: float) -> None:
        if self.target.is_dead:
            return super().update(dt)

        self.direction.x = self.target.x - self.rect.x
        self.direction.y = self.target.y - self.rect.y
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt


class DiagonalMissile(Missile):
    def __init__(self, prototype: MissilePrototype, position: tuple[float, float], team: str, angle: int) -> None:
        super().__init__(prototype, position, team)
        self.angle = math.radians(angle)
        self.direction.x = math.cos(self.angle)
        self.direction.y = math.sin(self.angle)
        self.direction = self.direction.normalize()
        self.image = pygame.transform.rotate(self.image, -angle + 90)
        print(angle + 90)
    
    def update(self, dt: float) -> None:
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
        
        
@dataclass
class MissilePrototype:
    image_path: str
    image_size: tuple[int, int]
    speed: int
    
    def __post_init__(self) -> None:
        self.image = load_image(self.image_path)

