import random

import pygame

from constants import *
from player import PlayerShip
from missile import Missile, MissilePrototype
from enemy import Enemy, EnemyPrototype
from background import AnimatedBackground, MovedBackground, FixedBackground

from utils import load_image, scale_image_by_size


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen_size = SCREEN_SIZE
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    
    enemy_spawn_timer = 0
    next_enemy = 4
    
    # Game setup
    background = AnimatedBackground("assets/image/background/background_1_{INDEX}.png", screen.get_size())
    star_background = MovedBackground("assets/image/background/background_2.png", screen.get_size())
    fixed_background = FixedBackground("assets/image/background/background_3.png", screen.get_size())
    player_ship = PlayerShip("assets/image/player/player.png", (64, 64), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 50))
    
    player_life_image = scale_image_by_size(load_image("assets/image/player/life.png"), (64, 64))
    player_life = 3
    
    player_missile_1 = MissilePrototype("assets/image/missile/player_missile_1.png", (12, 16), 300)
    
    basic_enemy = EnemyPrototype("assets/image/enemy/basic_alien_1.png", (64, 64), 100)
    
    missile_container: list[Missile] = []
    enemy_container: list[Enemy] = []
    
    
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
            enemy_container.append(Enemy(basic_enemy, e_pos, screen.get_size()))

        screen.fill(LIGHT_GRAY)
        
        fixed_background.draw(screen)
        star_background.draw(screen)
        background.draw(screen)
        background.update(dt)
        star_background.update(dt)
        
        # 斜め移動はサポートしない
        player_ship.direction.x = 0
        player_ship.direction.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_ship.direction.y = -1
        elif keys[pygame.K_s]:
            player_ship.direction.y = 1
        
        if keys[pygame.K_a]:
            player_ship.direction.x = -1
        elif keys[pygame.K_d]:
            player_ship.direction.x = 1
        
        if keys[pygame.K_SPACE] and player_ship.can_shoot():
            missile = Missile(player_missile_1, (player_ship.rect.centerx, player_ship.rect.centery - 5), "player", screen.get_size())
            missile_container.append(missile)
            player_ship.missile_cooldown = 0.5
        
        
        for enemy in enemy_container:
            enemy.update(dt)
            enemy.draw(screen)
            if enemy.rect.top > screen_size[1]:
                enemy_container.remove(enemy)
                player_life -= 1
                continue
        
        for missile in missile_container[:]:
            missile.update(dt)
            if missile.rect.bottom < 0 or missile.rect.top > screen_size[1]:
                missile_container.remove(missile)
                continue
            missile.draw(screen)
        
        for missile in missile_container[:]:
            for enemy in enemy_container[:]:
                if missile.collide_with(enemy):
                    missile_container.remove(missile)
                    enemy_container.remove(enemy)

        player_ship.update(dt)
        player_ship.draw(screen)
        for i in range(player_life):
            screen.blit(player_life_image, (i * (player_life_image.get_width() + 5) + 5, 16))

        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
