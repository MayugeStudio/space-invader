import random

import pygame

INITIAL_SCREEN_SIZE = (800, 800)
MIN_SCREEN_SIZE = (400, 400)
FPS = 60
TITLE = "Space Invaders"

# Constants
MENU_SCENE = 0
GAME_SCENE = 1
TRANSITION_TO_GAME_OVER_SCENE = 2
GAME_OVER_SCENE = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)


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

class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen_rect = screen.get_rect()
        self.screen_size = INITIAL_SCREEN_SIZE
        self.font = pygame.Font("assets/fonts/PixelMplus12-Regular.ttf", size=36)
        self.scene = MENU_SCENE

class Entity:
    def __init__(
        self,
        image_path: str,
        image_size: tuple[int, int],
        position: tuple[int, int],
        image: pygame.Surface | None = None,
    ) -> None:
        if image is not None:
            self.image = scale_image_by_size(image, image_size)
        else:
            self.image = scale_image_by_size(load_image(image_path), image_size)
        self.image_size = image_size
        self.image = create_outline(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_frect(center=position)
        self.x, self.y = position

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update(self, dt: float) -> None:
        pass

    def collide_with(self, other: "Entity") -> bool:
        return (
            self.mask.overlap(
                other.mask, (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
            )
            is not None
        )

class PlayerShip(Entity):
    def __init__(
        self, image_path: str, image_size: tuple[int, int], position: tuple[int, int]
    ) -> None:
        super().__init__(image_path, image_size, position)
        self.speed = 200
        self.direction = pygame.math.Vector2(0, 0)
        self.missile_cooldown = 0.5

    def update(self, dt: float) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt

        self.rect.centerx = math.floor(self.x)
        self.rect.centery = math.floor(self.y)

        self.missile_cooldown -= dt

    def can_shoot(self) -> bool:
        return self.missile_cooldown <= 0

class Enemy(Entity):
    def __init__(
        self,
        position: tuple[int, int],
        screen_size: tuple[int, int],
    ) -> None:
        super().__init__("", prototype.image_size, position, prototype.image)
        self.speed = prototype.speed
        self.direction = 1
        self.screen_size = screen_size
        self.is_dead = False

    def update(self, dt: float) -> None:
        self.rect.y += dt * self.speed * self.direction

    def mark_as_dead(self) -> None:
        self.is_dead = True

class Missile(Entity):
    def __init__(
        self,
        position: tuple[float, float],
        team: str,
    ) -> None:
        position = int(position[0]), int(position[1])
        super().__init__("", prototype.image_size, position, image=prototype.image)
        self.team = team
        self.direction = (
            pygame.Vector2(0, -1) if team == "player" else pygame.Vector2(0, 1)
        )
        self.speed = prototype.speed

    def update(self, dt: float) -> None:
        self.rect.y += self.direction.y * self.speed * dt


class HomingMissile(Missile):
    def __init__(
        self,
        position: tuple[float, float],
        team: str,
        target: Enemy,
    ) -> None:
        super().__init__(prototype, position, team)
        self.target = target

    def update(self, dt: float) -> None:
        if self.target.is_dead:
            return super().update(dt)

        self.direction.x = self.target.x - self.rect.x
        self.direction.y = self.target.y - self.rect.y
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt


class DiagonalMissile(Missile):
    def __init__(
        self,
        position: tuple[float, float],
        team: str,
        angle: int,
    ) -> None:
        super().__init__(prototype, position, team)
        self.angle = math.radians(angle)
        self.direction.x = math.cos(self.angle)
        self.direction.y = math.sin(self.angle)
        self.direction = self.direction.normalize()
        self.image = pygame.transform.rotate(self.image, -angle + 90)

    def update(self, dt: float) -> None:
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

class Counter:
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

enemies_meta_data = {
        "basic_1": {
            "image": "assets/image/enemy/basic_alien_1.png",
            "size": (64, 64),
        },
        "basic_2": {
            "image": "assets/image/enemy/basic_alien_2.png",
            "size": (64, 64),
        },
        "basic_3": {
            "image": "assets/image/enemy/basic_alien_3.png",
            "size": (64, 64),
        },
}

missiles_meta_data = {
        "missile_1": {
            "image": "assets/image/missile/player_missile_1.png",
            "size":  (12, 16),
        },
        "missile_2": {
            "image": "assets/image/missile/player_missile_2.png",
            "size": (12, 16),
        },
}

# ---------- Initialize pygame and display ----------
pygame.init()
screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE)

# ---------- Load Images ----------
player_life_image = scale_image_by_size(
    load_image("assets/image/player/life.png"), (64, 64)
)

menu_scene_bg_list = [
    scale_image_by_size(
        load_image(f"assets/image/ui/menu_scene_bg_{n}.png"), INITIAL_SCREEN_SIZE
    )
    for n in range(1, 12 + 1)
]

menu_scene_alien_bg_list = [
    scale_image_by_size(
        load_image(f"assets/image/ui/menu_scene_alien_bg_{n}.png"), INITIAL_SCREEN_SIZE
    )
    for n in range(1, 12 + 1)
]

cursor_images = [
    scale_image_by_size(
        load_image(f"assets/image/ui/cursor_{n}.png"), (8 * 4, 9 * 4)
    )
    for n in range(1, 6 + 1)
]
cursor_image_rect = cursor_images[0].get_rect()

reversed_cursor_images = [
    pygame.transform.flip(surf, True, False) for surf in cursor_images
]
reversed_cursor_image_rect = reversed_cursor_images[0].get_rect()

# ---------- Initialize Text Surface ----------
#TODO Create new class which contains image-raw-data and image-rect
start_game_text = scale_image_by_size(
    load_image(f"assets/image/ui/start_game.png"), (70 * 4, 9 * 4)
)
start_game_text_rect = start_game_text.get_rect()

option_text_image = scale_image_by_size(
    load_image("assets/image/ui/option.png"), (7 * 6 * 4, 9 * 4)
)
option_text_rect = option_text_image.get_rect()

quit_text_image = scale_image_by_size(
    load_image("assets/image/ui/quit.png"), (7 * 4 * 4, 9 * 4)
)
quit_text_rect = quit_text_image.get_rect()

game_over_text = scale_image_by_size(
    load_image("assets/image/ui/game_over.png"), (56 * 8, 8 * 8)
)
game_over_text_rect = game_over_text.get_rect()

place_space_to_continue_text = scale_image_by_size(
    load_image("assets/image/ui/place_space_to_continue.png"), (161 * 4, 7 * 5)
)
place_space_to_continue_text_rect = place_space_to_continue_text.get_rect()

space_text_image = scale_image_by_size(
    load_image(f"assets/image/ui/space.png"), (49 * 4, 7 * 4)
)
space_text_rect = space_text_image.get_rect()

selection_rect_list = [start_game_text_rect, option_text_rect, quit_text_rect]

# ---------- Sounds ----------
sound_map = {
    "shoot": pygame.mixer.Sound("assets/sound/bullet_shoot.wav"),
    "hit": pygame.mixer.Sound("assets/sound/hit.wav"),
    "select": pygame.mixer.Sound("assets/sound/select.wav"),
}
sound_map["shoot"].set_volume(0.1)
sound_map["select"].set_volume(0.1)

# ---------- Counters ----------
menu_scene_counter = AnimationCounter(0.13, len(menu_scene_bg_list))
menu_scene_alien_counter = AnimationCounter(0.08, len(menu_scene_alien_bg_list))
cursor_animation_counter = AnimationCounter(0.09, len(cursor_images))
cursor_move_counter = Counter(0.2, len(selection_rect_list))

def draw_menu(game: Game, dt: float):
    screen.fill(LIGHT_GRAY)
    screen.blit(menu_scene_bg_list[menu_scene_counter.index], (0, 0))
    screen.blit(menu_scene_alien_bg_list[menu_scene_alien_counter.index], (0, 0))

    start_game_text_rect.centerx = game.screen_rect.centerx
    start_game_text_rect.centery = game.screen_rect.centery + 220
    option_text_rect.centerx = game.screen_rect.centerx
    option_text_rect.centery = start_game_text_rect.centery + 50
    quit_text_rect.centerx = game.screen_rect.centerx
    quit_text_rect.centery = option_text_rect.centery + 50

    screen.blit(start_game_text, start_game_text_rect)
    screen.blit(option_text_image, option_text_rect)
    screen.blit(quit_text_image, quit_text_rect)

    cursor_image_rect.centerx = (
        game.screen_rect.centerx
        - selection_rect_list[cursor_move_counter.index].width // 2
        - 50
    )
    reversed_cursor_image_rect.centerx = (
        game.screen_rect.centerx
        + selection_rect_list[cursor_move_counter.index].width // 2
        + 50
    )
    cursor_image_rect.centery = reversed_cursor_image_rect.centery = (
        selection_rect_list[cursor_move_counter.index].centery
    )

    screen.blit(
        cursor_images[cursor_animation_counter.index], cursor_image_rect
    )
    screen.blit(
        reversed_cursor_images[cursor_animation_counter.index],
        reversed_cursor_image_rect,
    )

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
            game.scene = GAME_SCENE
        elif cursor_move_counter.index == 1:
            # TODO: MOVE TO OPTION MENU
            pass
        elif cursor_move_counter.index == 2:
            running = False

def game_loop(game, dt):
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
        game.scene = TRANSITION_TO_GAME_OVER_SCENE

    current_missile_text_surface = font.render(missile_factory_list[missile_factory_cursor.index].name, False, WHITE)
    current_missile_text_rect = current_missile_text_surface.get_rect()

    current_missile_text_rect.left = screen_rect.left + 30
    current_missile_text_rect.bottom = screen_rect.bottom - 30

    screen.blit(current_missile_text_surface, current_missile_text_rect)

    player_ship.update(dt)
    player_ship.draw(screen)

    if show_increase_difficulty_text:
        current_difficulty_surface = font.render(f"Current Diffuculty: {current_difficulty}", False, WHITE)
        current_difficulty_rect = current_difficulty_surface.get_rect()

        increase_difficulty_text_rect.center = screen_rect.center
        current_difficulty_rect.centerx = screen_rect.centerx
        current_difficulty_rect.centery = (increase_difficulty_text_rect.centery + 100)
        screen.blit(increase_difficulty_text_surface, increase_difficulty_text_rect)
        screen.blit(current_difficulty_surface, current_difficulty_rect)
        show_increase_difficulty_counter += dt
        if (show_increase_difficulty_counter > show_increase_difficulty_hidden_count):
            show_increase_difficulty_counter = 0
            show_increase_difficulty_text = False

    for i in range(player_life):
        screen.blit(player_life_image, (i * (player_life_image.get_width() + 5) + 5, 16))

def main():
    game = Game(screen)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    enemy_spawn_timer = 0
    next_enemy = 4
    appeared_enemy_number = 0
    current_difficulty = 1

    background = AnimatedBackground(
        "assets/image/background/background_1_{INDEX}.png", screen.get_size()
    )
    star_background = MovedBackground(
        "assets/image/background/background_2.png", screen.get_size()
    )
    fixed_background = FixedBackground(
        "assets/image/background/background_3.png", screen.get_size()
    )
    player_ship = PlayerShip(
        "assets/image/player/player.png",
        (64, 64),
        (INITIAL_SCREEN_SIZE[0] // 2, INITIAL_SCREEN_SIZE[1] - 50),
    )

    player_life = 3

    missile_container: list[Missile] = []
    enemy_container: list[Enemy] = []

    missile_factory_cursor = Counter(0.2, 3)

    increase_difficulty_text_surface = game.font.render("Game difficulty has been increased.", False, WHITE)
    increase_difficulty_text_rect = increase_difficulty_text_surface.get_rect()
    show_increase_difficulty_text = False
    show_increase_difficulty_counter = 0
    show_increase_difficulty_hidden_count = 2

    increase_difficulty_enemy_number = 5

    overlap_surface = pygame.Surface(INITIAL_SCREEN_SIZE)
    alpha = 0
    overlap_surface.fill((0, 0, 0))
    overlap_surface.set_alpha(alpha)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        dt = clock.tick(FPS) / 1000

        if game.scene == MENU_SCENE:
            draw_menu(game, dt)
        elif game.scene == GAME_SCENE:
            game_loop(game, dt)
        elif game.scene == TRANSITION_TO_GAME_OVER_SCENE:
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
                game.scene = GAME_OVER_SCENE
            overlap_surface.set_alpha(alpha)

        elif game.scene == GAME_OVER_SCENE:
            screen.fill(BLACK)

            game_over_text_rect.centerx = screen_rect.centerx
            game_over_text_rect.centery = screen_rect.centery - 150

            place_space_to_continue_text_rect.centerx = screen_rect.centerx
            place_space_to_continue_text_rect.centery = screen_rect.centery

            space_text_rect.centerx = screen_rect.centerx
            space_text_rect.centery = screen_rect.centery + 200

            cursor_image_rect.centerx = (
                screen_rect.centerx - space_text_rect.width // 2 - 50
            )
            reversed_cursor_image_rect.centerx = (
                screen_rect.centerx + space_text_rect.width // 2 + 50
            )
            cursor_image_rect.centery = reversed_cursor_image_rect.centery = (
                space_text_rect.centery
            )

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
                game.scene = MENU_SCENE

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

