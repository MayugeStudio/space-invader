import pygame

from constants import *
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    
    # Game setup
    player = Player("assets/image/player/player.png", (64, 64), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 50))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        dt = clock.tick(FPS) / 1000

        screen.fill(BLACK)
        
        player.update(dt)
        player.draw(screen)
    
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
