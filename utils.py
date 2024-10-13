import pygame


def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def scale_image_by_size(image: pygame.Surface, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(image, size)


def create_outline(surface: pygame.Surface) -> pygame.Surface:
    result = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    s = surface.copy()
    mask = pygame.mask.from_surface(s)
    mask_surface = mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))

    result.blit(mask_surface, [0, -4])
    result.blit(mask_surface, [0, 4])
    result.blit(mask_surface, [-4, 0])
    result.blit(mask_surface, [4, 0])
    result.blit(surface, [0, 0])

    return result
