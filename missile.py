from __future__ import annotations

import pygame

from dataclasses import dataclass

from entity import Entity

from utils import load_image


class Missile(Entity):
    def __init__(
        self,
        prototype: MissilePrototype,
        position: tuple[float, float],
        team: str,
        screen_size: tuple[int, int]
        ) -> None:
        position = int(position[0]), int(position[1])
        super().__init__("", prototype.image_size, position, image=prototype.image)
        self.team = team
        self.direction = pygame.Vector2(0, -1) if team == "player" else pygame.Vector2(0, 1)
        self.speed = prototype.speed
        self.screen_size = screen_size
    
    def update(self, dt: float) -> None:
        self.rect.y += self.direction.y * self.speed * dt
        if self.rect.bottom < 0 or self.rect.top > self.screen_size[1]:
            self.kill()


@dataclass
class MissilePrototype:
    image_path: str
    image_size: tuple[int, int]
    speed: int
    
    def __post_init__(self) -> None:
        self.image = load_image(self.image_path)

