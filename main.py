import random

import pygame

from constants import *
from player import PlayerShip
from missile import Missile, MissilePrototype, MissileFactory, HomingMissileFactory, WayMissileFactory
from enemy import Enemy, EnemyPrototype
from background import AnimatedBackground, MovedBackground, FixedBackground

from utils import load_image, scale_image_by_size


class Cursor:
    def __init__(self, interval: float, max_index: int) -> None:
        self.counter = 0
        self.interval = interval
        self.index = 0
        self.max_index = max_index
    
    def add_counter(self, dt: float) -> None:
        self.counter += dt
    
    def add_index(self) -> None:
        self.index += 1
        self.index %= self.max_index
    
    def sub_index(self) -> None:
        self.index -= 1
        self.index %= self.max_index

    def is_active(self) -> bool:
        return self.counter >= self.interval

    def reset_counter(self) -> None:
        self.counter = 0


class AnimationCounter:
    def __init__(self, change: float, max_index: int) -> None:
        self.change = change
        self.counter = 0
        self.index = 0
        self.max_index = max_index
    
    def add_counter(self, dt: float) -> None:
        self.counter += dt
    
    def add_index(self) -> None:
        self.index += 1
        self.index %= self.max_index
    
    def sub_index(self) -> None:
        self.index -= 1
        self.index %= self.max_index
    
    def is_change(self) -> bool:
        return self.counter >= self.change

    def reset_counter(self) -> None:
        self.counter = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen_size = SCREEN_SIZE
    screen_rect = screen.get_rect()
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    
    enemy_spawn_timer = 0
    next_enemy = 4
    appeared_enemy_number = 0
    current_difficulty = 1
    
    # Game setup
    
    font = pygame.Font("assets/fonts/PixelMplus12-Regular.ttf", size=36)
    
    sound_map = {
        "shoot": pygame.mixer.Sound("assets/sound/bullet_shoot.wav"),
        "hit": pygame.mixer.Sound("assets/sound/hit.wav"),
        "select": pygame.mixer.Sound("assets/sound/select.wav")
    }
    sound_map["shoot"].set_volume(0.1)
    sound_map["select"].set_volume(0.1)
    
    
    background = AnimatedBackground("assets/image/background/background_1_{INDEX}.png", screen.get_size())
    star_background = MovedBackground("assets/image/background/background_2.png", screen.get_size())
    fixed_background = FixedBackground("assets/image/background/background_3.png", screen.get_size())
    player_ship = PlayerShip("assets/image/player/player.png", (64, 64), (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 50))
    
    player_life_image = scale_image_by_size(load_image("assets/image/player/life.png"), (64, 64))
    player_life = 3
    
    player_missile_1 = MissilePrototype("assets/image/missile/player_missile_1.png", (12, 16), 300)
    player_missile_2 = MissilePrototype("assets/image/missile/player_missile_1.png", (12, 16), 300)
    basic_enemy_1 = EnemyPrototype("assets/image/enemy/basic_alien_1.png", (64, 64), 100)
    basic_enemy_2 = EnemyPrototype("assets/image/enemy/basic_alien_2.png", (64, 64), 150)
    basic_enemy_3 = EnemyPrototype("assets/image/enemy/basic_alien_3.png", (64, 64), 120)
    
    enemy_prototypes = [basic_enemy_1, basic_enemy_2, basic_enemy_3]
    
    missile_container: list[Missile] = []
    enemy_container: list[Enemy] = []
    
    normal_missile_factory = MissileFactory(player_missile_1, player_ship, "普通のミサイル")
    homing_missile_factory = HomingMissileFactory(player_missile_2, player_ship, enemy_container, "ホーミング")
    five_way_missile_factory = WayMissileFactory(player_missile_1, player_ship, 5, "5wayミサイル")
    
    missile_factory_list = [normal_missile_factory, homing_missile_factory, five_way_missile_factory]
    missile_factory_cursor = Cursor(0.2, len(missile_factory_list))
    
    MENU_SCENE = "MENU"
    GAME_SCENE = "GAME"
    MOVE_TO_GAME_OVER_SCENE = "MOVE_GAME_OVER"
    GAME_OVER_SCENE = "GAME_OVER"
    
    increase_difficulty_text_surface = font.render("難易度が上昇した", False, WHITE)
    increase_difficulty_text_rect = increase_difficulty_text_surface.get_rect()
    show_increase_difficulty_text = False
    show_increase_difficulty_counter = 0
    show_increase_difficulty_hidden_count = 2
    increase_difficulty_enemy_number = 5
    
    game_over_text = scale_image_by_size(load_image("assets/image/ui/game_over.png"), (56 * 8, 8 * 8))
    game_over_text_rect = game_over_text.get_rect()
    
    place_space_to_continue_text = scale_image_by_size(load_image("assets/image/ui/place_space_to_continue.png"), (161 * 4, 7 * 5))
    place_space_to_continue_text_rect = place_space_to_continue_text.get_rect()
    
    space_text_image = scale_image_by_size(load_image(f"assets/image/ui/space.png"), (49 * 4, 7 * 4))
    space_text_rect = space_text_image.get_rect()
    
    menu_scene_bg_list = [scale_image_by_size(load_image(f"assets/image/ui/menu_scene_bg_{n}.png"), screen_size) for n in range(1, 12 + 1)]
    menu_scene_counter = AnimationCounter(0.13, len(menu_scene_bg_list))
    
    menu_scene_alien_bg_list = [scale_image_by_size(load_image(f"assets/image/ui/menu_scene_alien_bg_{n}.png"), screen_size) for n in range(1, 12 + 1)]
    menu_scene_alien_counter = AnimationCounter(0.08, len(menu_scene_alien_bg_list))

    start_game_text = scale_image_by_size(load_image(f"assets/image/ui/start_game.png"), (70 * 4, 9 * 4))
    start_game_text_rect = start_game_text.get_rect()
    option_text_image = scale_image_by_size(load_image("assets/image/ui/option.png"), (7 * 6 * 4, 9 * 4))
    option_text_rect = option_text_image.get_rect()
    quit_text_image = scale_image_by_size(load_image("assets/image/ui/quit.png"), (7 * 4 * 4, 9 * 4))
    quit_text_rect = quit_text_image.get_rect()
    
    selection_rect_list = [start_game_text_rect, option_text_rect, quit_text_rect]
    
    cursor_move_counter = Cursor(0.2, len(selection_rect_list))
    
    cursor_images = [scale_image_by_size(load_image(f"assets/image/ui/cursor_{n}.png"), (8 * 4, 9 * 4)) for n in range(1, 6 + 1)]
    reversed_cursor_images = [pygame.transform.flip(surf, True, False) for surf in cursor_images]
    
    cursor_image_rect = cursor_images[0].get_rect()
    reversed_cursor_image_rect = reversed_cursor_images[0].get_rect()
    
    cursor_animation_counter = AnimationCounter(0.09, len(cursor_images))
    
    overlap_surface = pygame.Surface(screen_size)
    alpha = 0
    overlap_surface.fill((0, 0, 0))
    overlap_surface.set_alpha(alpha)
    
    current_scene = MENU_SCENE
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        dt = clock.tick(FPS) / 1000
        
        if current_scene == MENU_SCENE:
            screen.fill(LIGHT_GRAY)
            screen.blit(menu_scene_bg_list[menu_scene_counter.index], (0, 0))
            screen.blit(menu_scene_alien_bg_list[menu_scene_alien_counter.index], (0, 0))

            start_game_text_rect.centerx = screen_rect.centerx
            start_game_text_rect.centery = screen_rect.centery + 220
            option_text_rect.centerx = screen_rect.centerx
            option_text_rect.centery = start_game_text_rect.centery + 50
            quit_text_rect.centerx = screen_rect.centerx
            quit_text_rect.centery = option_text_rect.centery + 50
            
            screen.blit(start_game_text, start_game_text_rect)
            screen.blit(option_text_image, option_text_rect)
            screen.blit(quit_text_image, quit_text_rect)
            
            cursor_image_rect.centerx = screen_rect.centerx - selection_rect_list[cursor_move_counter.index].width//2 - 50
            reversed_cursor_image_rect.centerx = screen_rect.centerx + selection_rect_list[cursor_move_counter.index].width//2 + 50
            cursor_image_rect.centery = reversed_cursor_image_rect.centery = selection_rect_list[cursor_move_counter.index].centery
            
            screen.blit(cursor_images[cursor_animation_counter.index], cursor_image_rect)
            screen.blit(reversed_cursor_images[cursor_animation_counter.index], reversed_cursor_image_rect)
            
            
            menu_scene_counter.add_counter(dt)
            if menu_scene_counter.is_change():
                menu_scene_counter.add_index()
                menu_scene_counter.reset_counter()

            menu_scene_alien_counter.add_counter(dt)
            if menu_scene_alien_counter.is_change():
                menu_scene_alien_counter.add_index()
                menu_scene_alien_counter.reset_counter()
                        
            cursor_animation_counter.add_counter(dt)
            if cursor_animation_counter.is_change():
                cursor_animation_counter.add_index()
                cursor_animation_counter.reset_counter()
            
            keys = pygame.key.get_pressed()
            
            cursor_move_counter.add_counter(dt)
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and cursor_move_counter.is_active():
                cursor_move_counter.add_index()
                cursor_move_counter.reset_counter()
                sound_map["select"].play()
            
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and cursor_move_counter.is_active():
                cursor_move_counter.sub_index()
                cursor_move_counter.reset_counter()
                sound_map["select"].play()

            if keys[pygame.K_SPACE] and cursor_move_counter.is_active():
                cursor_move_counter.reset_counter()
                sound_map["select"].play()
                if cursor_move_counter.index == 0:
                    current_scene = GAME_SCENE
                elif cursor_move_counter.index == 1:
                    # TODO: MOVE TO OPTION MENU
                    pass
                elif cursor_move_counter.index == 2:
                    running = False
                
        elif current_scene == GAME_SCENE:
            enemy_spawn_timer += dt
            if enemy_spawn_timer >= next_enemy:
                enemy_spawn_timer = 0
                e_pos = (random.randint(200, SCREEN_SIZE[0] - 200), (random.randint(-100, -50)))
                e_prototype = random.choice(enemy_prototypes)
                enemy_container.append(Enemy(e_prototype, e_pos, screen.get_size()))
                appeared_enemy_number += 1
                if appeared_enemy_number >= increase_difficulty_enemy_number:
                    appeared_enemy_number = 0
                    if next_enemy > 0.3:
                        next_enemy -= 0.3
                        current_difficulty += 1
                        increase_difficulty_enemy_number *= 1.2
                        increase_difficulty_enemy_number = int(increase_difficulty_enemy_number)
                        show_increase_difficulty_text = True
                        
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
            
            missile_factory_cursor.add_counter(dt)
            if keys[pygame.K_LEFT] and missile_factory_cursor.is_active():
                missile_factory_cursor.sub_index()
                missile_factory_cursor.reset_counter()
            if keys[pygame.K_RIGHT] and missile_factory_cursor.is_active():
                missile_factory_cursor.add_index()
                missile_factory_cursor.reset_counter()
            
            if keys[pygame.K_SPACE] and player_ship.can_shoot():
                missile_factory_list[missile_factory_cursor.index].shoot(missile_container)
                player_ship.missile_cooldown = 0.5
                sound_map["shoot"].play()
            
            for enemy in enemy_container:
                enemy.update(dt)
                enemy.draw(screen)
                if enemy.rect.top > screen_size[1]:
                    enemy_container.remove(enemy)
                    enemy.mark_as_dead()
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
                        enemy.mark_as_dead()

            if player_life <= 0:
                current_scene = MOVE_TO_GAME_OVER_SCENE
            
            current_missile_text_surface = font.render(missile_factory_list[missile_factory_cursor.index].name, False, WHITE)
            current_missile_text_rect = current_missile_text_surface.get_rect()
            
            current_missile_text_rect.left = screen_rect.left + 30
            current_missile_text_rect.bottom = screen_rect.bottom - 30
            
            screen.blit(current_missile_text_surface, current_missile_text_rect)
            
            
            player_ship.update(dt)
            player_ship.draw(screen)
            
            if show_increase_difficulty_text:
                current_difficulty_surface = font.render(f"現在の難易度 {current_difficulty}", False, WHITE)
                current_difficulty_rect = current_difficulty_surface.get_rect()
                
                increase_difficulty_text_rect.center = screen_rect.center
                current_difficulty_rect.centerx = screen_rect.centerx
                current_difficulty_rect.centery = increase_difficulty_text_rect.centery + 100
                screen.blit(increase_difficulty_text_surface, increase_difficulty_text_rect)
                screen.blit(current_difficulty_surface, current_difficulty_rect)
                show_increase_difficulty_counter += dt
                if show_increase_difficulty_counter > show_increase_difficulty_hidden_count:
                    show_increase_difficulty_counter = 0
                    show_increase_difficulty_text = False
            
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
            screen.blit(cursor_images[cursor_animation_counter.index], cursor_image_rect)
            screen.blit(reversed_cursor_images[cursor_animation_counter.index], reversed_cursor_image_rect)
            
            cursor_animation_counter.add_counter(dt)
            if cursor_animation_counter.is_change():
                cursor_animation_counter.add_index()
                cursor_animation_counter.reset_counter()
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                sound_map["select"].play()
                current_scene = MENU_SCENE
        
        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
