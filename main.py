import pygame

from constants import *
from player import Player
from background import AnimatedBackground, MovedBackground, FixedBackground


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    
    # Game setup
    background = AnimatedBackground("assets/image/background/background_1_{INDEX}.png", screen.get_size())
    star_background = MovedBackground("assets/image/background/background_2.png", screen.get_size())
    fixed_background = FixedBackground("assets/image/background/background_3.png", screen.get_size())
    player = Player("assets/image/player/player.png", (64, 64), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 50))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        dt = clock.tick(FPS) / 1000

        screen.fill(LIGHT_GRAY)
        fixed_background.draw(screen)
        star_background.draw(screen)
        background.draw(screen)
        background.update(dt)
        star_background.update(dt)
        
        player.update(dt)
        player.draw(screen)
    
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
