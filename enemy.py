from __future__ import annotations

from dataclasses import dataclass

from entity import Entity

from utils import load_image


class Enemy(Entity):
    def __init__(self, prototype: EnemyPrototype, position: tuple[int, int], screen_size: tuple[int, int]) -> None:
        super().__init__("", prototype.image_size, position, prototype.image)
        self.speed = prototype.speed
        self.direction = 1
        self.screen_size = screen_size
        self.is_dead = False
        
    def update(self, dt: float) -> None:
        self.rect.y += dt * self.speed * self.direction
    
    def mark_as_dead(self) -> None:
        self.is_dead = True        

@dataclass
class EnemyPrototype:
    image_path: str
    image_size: tuple[int, int]
    speed: int
    
    def __post_init__(self) -> None:
        self.image = load_image(self.image_path)
