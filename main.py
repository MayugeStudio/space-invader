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
    screen_rect = screen.get_rect()
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
    player_life = 1
    
    player_missile_1 = MissilePrototype("assets/image/missile/player_missile_1.png", (12, 16), 300)
    basic_enemy = EnemyPrototype("assets/image/enemy/basic_alien_1.png", (64, 64), 100)
    
    missile_container: list[Missile] = []
    enemy_container: list[Enemy] = []
    
    MENU_SCENE = "MENU"
    GAME_SCENE = "GAME"
    MOVE_TO_GAME_OVER_SCENE = "MOVE_GAME_OVER"
    GAME_OVER_SCENE = "GAME_OVER"
    
    game_over_text = scale_image_by_size(load_image("assets/image/ui/game_over.png"), (56 * 8, 8 * 8))
    game_over_text_rect = game_over_text.get_rect()
    
    place_space_to_continue_text = scale_image_by_size(load_image("assets/image/ui/place_space_to_continue.png"), (161 * 4, 7 * 5))
    place_space_to_continue_text_rect = place_space_to_continue_text.get_rect()
    
    space_text_image = scale_image_by_size(load_image(f"assets/image/ui/space.png"), (49 * 4, 7 * 4))
    space_text_rect = space_text_image.get_rect()
    
    menu_scene_bg_list = [scale_image_by_size(load_image(f"assets/image/ui/menu_scene_bg_{n}.png"), screen_size) for n in range(1, 12 + 1)]
    menu_scene_index = 0
    menu_scene_counter = 0
    menu_scene_change = 0.13
    
    menu_scene_alien_bg_list = [scale_image_by_size(load_image(f"assets/image/ui/menu_scene_alien_bg_{n}.png"), screen_size) for n in range(1, 12 + 1)]
    menu_scene_alien_index = 0
    menu_scene_alien_counter = 0
    menu_scene_alien_change = 0.08
    
    start_game_text = scale_image_by_size(load_image(f"assets/image/ui/start_game.png"), (70 * 4, 9 * 4))
    start_game_text_rect = start_game_text.get_rect()
    option_text_image = scale_image_by_size(load_image("assets/image/ui/option.png"), (7 * 6 * 4, 9 * 4))
    option_text_rect = option_text_image.get_rect()
    quit_text_image = scale_image_by_size(load_image("assets/image/ui/quit.png"), (7 * 4 * 4, 9 * 4))
    quit_text_rect = quit_text_image.get_rect()
    
    selection_rect_list = [start_game_text_rect, option_text_rect, quit_text_rect]
    
    selected_rect = start_game_text_rect
    
    cursor_images = [scale_image_by_size(load_image(f"assets/image/ui/cursor_{n}.png"), (8 * 4, 9 * 4)) for n in range(1, 6 + 1)]
    reversed_cursor_images = [pygame.transform.flip(surf, True, False) for surf in cursor_images]
    
    cursor_image_rect = cursor_images[0].get_rect()
    reversed_cursor_image_rect = reversed_cursor_images[0].get_rect()
    
    cursor_animation_index = 0
    cursor_animation_counter = 0
    cursor_animation_change = 0.09
    
    cursor_move_counter = 0
    cursor_move_interval = 0.2
    cursor_row = 0
    cursor_max_row = len(selection_rect_list)
    
    overlap_surface = pygame.Surface(screen_size)
    alpha = 0
    overlap_surface.fill((0, 0, 0))
    overlap_surface.set_alpha(alpha)
    
    current_scene = GAME_OVER_SCENE
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        
        dt = clock.tick(FPS) / 1000
        
        if current_scene == MENU_SCENE:
            screen.fill(LIGHT_GRAY)
            screen.blit(menu_scene_bg_list[menu_scene_index], (0, 0))
            screen.blit(menu_scene_alien_bg_list[menu_scene_alien_index], (0, 0))

            start_game_text_rect.centerx = screen_rect.centerx
            start_game_text_rect.centery = screen_rect.centery + 220
            option_text_rect.centerx = screen_rect.centerx
            option_text_rect.centery = start_game_text_rect.centery + 50
            quit_text_rect.centerx = screen_rect.centerx
            quit_text_rect.centery = option_text_rect.centery + 50
            
            screen.blit(start_game_text, start_game_text_rect)
            screen.blit(option_text_image, option_text_rect)
            screen.blit(quit_text_image, quit_text_rect)
            
            cursor_image_rect.centerx = screen_rect.centerx - selected_rect.width//2 - 50
            reversed_cursor_image_rect.centerx = screen_rect.centerx + selected_rect.width//2 + 50
            cursor_image_rect.centery = reversed_cursor_image_rect.centery = selected_rect.centery
            
            screen.blit(cursor_images[cursor_animation_index], cursor_image_rect)
            screen.blit(reversed_cursor_images[cursor_animation_index], reversed_cursor_image_rect)
            
            
            menu_scene_counter += dt
            if menu_scene_counter >= menu_scene_change:
                menu_scene_index += 1
                menu_scene_index %= len(menu_scene_bg_list)
                menu_scene_counter = 0
            
            menu_scene_alien_counter += dt
            if menu_scene_alien_counter >= menu_scene_alien_change:
                menu_scene_alien_index += 1
                menu_scene_alien_index %= len(menu_scene_alien_bg_list)
                menu_scene_alien_counter = 0
            
            cursor_animation_counter += dt
            if cursor_animation_counter > cursor_animation_change:
                cursor_animation_index += 1
                cursor_animation_index %= len(cursor_images)
                cursor_animation_counter = 0
            
            keys = pygame.key.get_pressed()
            
            cursor_move_counter += dt
            
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and cursor_move_counter >= cursor_move_interval:
                cursor_move_counter = 0
                cursor_row += 1
                cursor_row %= cursor_max_row
                selected_rect = selection_rect_list[cursor_row]
            
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and cursor_move_counter >= cursor_move_interval:
                cursor_move_counter = 0
                cursor_row -= 1
                cursor_row %= cursor_max_row
                selected_rect = selection_rect_list[cursor_row]

            if keys[pygame.K_SPACE] and cursor_move_counter >= cursor_move_interval:
                cursor_move_counter = 0
                if cursor_row == 0:
                    current_scene = GAME_SCENE
                elif cursor_row == 1:
                    # TODO: MOVE TO OPTION MENU
                    pass
                elif cursor_row == 2:
                    running = False
                
        elif current_scene == GAME_SCENE:
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

            if player_life <= 0:
                current_scene = MOVE_TO_GAME_OVER_SCENE
            
            player_ship.update(dt)
            player_ship.draw(screen)
            for i in range(player_life):
                screen.blit(player_life_image, (i * (player_life_image.get_width() + 5) + 5, 16))

        elif current_scene == MOVE_TO_GAME_OVER_SCENE:
            screen.fill(LIGHT_GRAY)
            
            fixed_background.draw(screen)
            star_background.draw(screen)
            background.draw(screen)
            background.update(dt)
            star_background.update(dt)
            
            player_ship.draw(screen)
            
            screen.blit(overlap_surface, (0, 0))
            alpha += 2
            
            if alpha >= 255:
                current_scene = GAME_OVER_SCENE
            overlap_surface.set_alpha(alpha)

        elif current_scene == GAME_OVER_SCENE:
            screen.fill(BLACK)

            game_over_text_rect.centerx = screen_rect.centerx
            game_over_text_rect.centery = screen_rect.centery - 150
            
            place_space_to_continue_text_rect.centerx = screen_rect.centerx
            place_space_to_continue_text_rect.centery = screen_rect.centery
            
            space_text_rect.centerx = screen_rect.centerx
            space_text_rect.centery = screen_rect.centery + 200
            
            cursor_image_rect.centerx = screen_rect.centerx - space_text_rect.width // 2 - 50
            reversed_cursor_image_rect.centerx = screen_rect.centerx + space_text_rect.width // 2 + 50
            cursor_image_rect.centery = reversed_cursor_image_rect.centery = space_text_rect.centery

            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(place_space_to_continue_text, place_space_to_continue_text_rect)
            screen.blit(space_text_image, space_text_rect)
            screen.blit(cursor_images[cursor_animation_index], cursor_image_rect)
            screen.blit(reversed_cursor_images[cursor_animation_index], reversed_cursor_image_rect)
            
            cursor_animation_counter += dt
            if cursor_animation_counter >= cursor_animation_change:
                cursor_animation_index += 1
                cursor_animation_index %= len(cursor_images)
                cursor_animation_counter = 0
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                current_scene = MENU_SCENE
        
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
