import pygame

from entity import Entity
from constants import *


class Player(Entity):
    def __init__(self, image: pygame.Surface, position: tuple[int, int]) -> None:
        super().__init__(image, position)
        self.speed = 5
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.y += self.speed * dt
        if keys[pygame.K_a]:
            self.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.x += self.speed * dt
        
        self.rect.center = tuple([round(i) for i in (self.x, self.y)])

