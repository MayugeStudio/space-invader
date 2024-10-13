from __future__ import annotations
import pygame

from utils import load_image, scale_image_by_size, create_outline


class Entity:
    def __init__(
        self,
        image_path: str,
        image_size: tuple[int, int],
        position: tuple[int, int],
        image: pygame.Surface | None = None,
    ) -> None:
        if image is not None:
            self.image = scale_image_by_size(image, image_size)
        else:
            self.image = scale_image_by_size(load_image(image_path), image_size)
        self.image_size = image_size
        self.image = create_outline(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center=position)
        self.x, self.y = position

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update(self, dt: float) -> None:
        pass

    def collide_with(self, other: "Entity") -> bool:
        return (
            self.mask.overlap(
                other.mask, (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
            )
            is not None
        )
