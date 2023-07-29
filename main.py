import random

import pygame

from constants import *
from player import Player
from entity import EntityContainer
from missile import Missile, MissilePrototype
from enemy import Enemy, EnemyPrototype
from background import AnimatedBackground, MovedBackground, FixedBackground

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    
    enemy_spawn_timer = 0
    next_enemy = 4
    
    # Game setup
    background = AnimatedBackground("assets/image/background/background_1_{INDEX}.png", screen.get_size())
    star_background = MovedBackground("assets/image/background/background_2.png", screen.get_size())
    fixed_background = FixedBackground("assets/image/background/background_3.png", screen.get_size())
    player = Player("assets/image/player/player.png", (64, 64), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 50))
    
    player_missile_1 = MissilePrototype("assets/image/missile/player_missile_1.png", (12, 16), 300)
    
    basic_enemy = EnemyPrototype("assets/image/enemy/basic_alien_1.png", (64, 64), 100)
    
    missile_container = EntityContainer()
    enemy_container = EntityContainer()
    
    
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        
        dt = clock.tick(FPS) / 1000
        enemy_spawn_timer += dt
        
        if enemy_spawn_timer >= next_enemy:
            enemy_spawn_timer = 0
            e_pos = (random.randint(200, SCREEN_SIZE[0] - 200), (random.randint(-100, -50)))
            enemy_container.add(Enemy(basic_enemy, e_pos, screen.get_size()))

        screen.fill(LIGHT_GRAY)
        
        fixed_background.draw(screen)
        star_background.draw(screen)
        background.draw(screen)
        background.update(dt)
        star_background.update(dt)
        
        # 斜め移動はサポートしない
        player.direction.x = 0
        player.direction.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.direction.y = -1
        elif keys[pygame.K_s]:
            player.direction.y = 1
        
        if keys[pygame.K_a]:
            player.direction.x = -1
        elif keys[pygame.K_d]:
            player.direction.x = 1
        
        if keys[pygame.K_SPACE] and player.can_shoot():
            missile_container.add(
                Missile(player_missile_1, player.rect.center, "player", screen.get_size())
            )
            player.missile_cooldown = 0.5
        
        player.update(dt)
        enemy_container.update(dt)
        missile_container.update(dt)

        missile_container.draw(screen)
        player.draw(screen)
        enemy_container.draw(screen)

        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
