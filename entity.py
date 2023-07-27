import pygame


class Entity:
    def __init__(self, image: pygame.Surface, position: tuple[int, int]) -> None:
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=position)
        self.x, self.y = position
    
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
    
    def update(self, dt: float) -> None:
        pass

    def collide_with(self, other: "Entity") -> bool:
        return self.mask.overlap(other.mask, (other.rect.x - self.rect.x, other.rect.y - self.rect.y)) is not None
