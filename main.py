import pygame

from constants import *


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)
    
        clock.tick(FPS)
        pygame.display.update()


    pygame.quit()