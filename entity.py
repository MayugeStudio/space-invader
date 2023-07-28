import pygame

from utils import load_image, scale_image_by_size


class Entity:
    def __init__(self, image_path: str, image_size: tuple[int, int], position: tuple[int, int]) -> None:
        self.image = scale_image_by_size(load_image(image_path), image_size)
        self.image_size = image_size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center=position)
        self.x, self.y = position
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
    
    def update(self, dt: float) -> None:
        pass

    def collide_with(self, other: "Entity") -> bool:
        return self.mask.overlap(other.mask, (other.rect.x - self.rect.x, other.rect.y - self.rect.y)) is not None


class EntityContainer:
    def __init__(self) -> None:
        self._enities: list[Entity] = []
    
    def add(self, entity: Entity) -> None:
        self._enities.append(entity)
    
    def remove(self, entity: Entity) -> None:
        self._enities.remove(entity)
    
    def draw(self, surface: pygame.Surface) -> None:
        for entity in self._enities:
            entity.draw(surface)
    
    def update(self, dt: float) -> None:
        for entity in self._enities:
            entity.update(dt)
    
    def collide_with(self, other: Entity) -> list[Entity]:
        return [entity for entity in self._enities if entity.collide_with(other)]
    