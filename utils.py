import pygame


def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def scale_image_by_size(image: pygame.Surface, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(image, size)
