import pygame

from utils import load_image, scale_image_by_size


class FixedBackground:
    def __init__(self, image_path: str, screen_size: tuple[int, int]) -> None:
        self.image = load_image(image_path)
        self.image = scale_image_by_size(self.image, screen_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)


class AnimatedBackground:
    def __init__(self, image_path: str, screen_size: tuple[int, int]) -> None:
        self.images = [load_image(image_path.format(INDEX=i)) for i in range(1, 12 + 1)]
        self.images = [scale_image_by_size(image, screen_size) for image in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.frame = 0
        self.frame_counter = 0
        self.frame_change = 0.4

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self, dt: float) -> None:
        self.frame_counter += dt
        if self.frame_counter >= self.frame_change:
            self.frame_counter = 0
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]


class MovedBackground:
    def __init__(self, image_path: str, screen_size: tuple[int, int]) -> None:
        self.image = load_image(image_path)
        self.image = scale_image_by_size(self.image, screen_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.y = 0
        self.screen_height = screen_size[1]

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.image, (self.rect.left, self.rect.top - self.screen_height))

    def update(self, dt: float) -> None:
        self.y += 100 * dt
        self.rect.top = round(self.y)
        if self.rect.top > self.screen_height:
            self.rect.top = 0
            self.y = 0
