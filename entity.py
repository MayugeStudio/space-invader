from __future__ import annotations
import pygame

from utils import load_image, scale_image_by_size


class Entity:
    def __init__(self, image_path: str, image_size: tuple[int, int], position: tuple[int, int], image: pygame.Surface | None = None) -> None:
        if image is not None:
            self.image = scale_image_by_size(image, image_size)
        else:
            self.image = scale_image_by_size(load_image(image_path), image_size)
        self.image_size = image_size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center=position)
        self.x, self.y = position
        self.parent: EntityContainer | None = None
    
    def set_parent(self, parent: EntityContainer | None) -> None:
        self.parent = parent
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
    
    def update(self, dt: float) -> None:
        pass

    def collide_with(self, other: "Entity") -> bool:
        return self.mask.overlap(other.mask, (other.rect.x - self.rect.x, other.rect.y - self.rect.y)) is not None

    def kill(self) -> None:
        if self.parent is not None:
            self.parent.remove(self)
            self.parent = None
    
    def alive(self) -> bool:
        return self.parent is not None


class EntityContainer:
    def __init__(self) -> None:
        self._entities: list[Entity] = []
    
    def add(self, entity: Entity) -> None:
        entity.set_parent(self)
        self._entities.append(entity)
    
    def remove(self, entity: Entity) -> None:
        self._entities.remove(entity)
        entity.set_parent(None)
    
    def draw(self, surface: pygame.Surface) -> None:
        for entity in self._entities:
            entity.draw(surface)
    
    def update(self, dt: float) -> None:
        for entity in self._entities:
            entity.update(dt)
    
    def get_all(self) -> list[Entity]:
        return self._entities
