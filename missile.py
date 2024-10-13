from __future__ import annotations

import math

import pygame

from dataclasses import dataclass
from enemy import Enemy

from entity import Entity

from utils import load_image


class Missile(Entity):
    def __init__(
        self,
        prototype: MissilePrototype,
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
        prototype: MissilePrototype,
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
        prototype: MissilePrototype,
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


class MissileFactory:
    def __init__(self, prototype: MissilePrototype, player: Entity, name: str) -> None:
        self.prototype = prototype
        self.player = player
        self.name = name

    def shoot(self, missile_container: list[Missile]) -> None:
        missile = Missile(
            self.prototype,
            (self.player.rect.centerx, self.player.rect.centery - 5),
            "player",
        )
        missile_container.append(missile)


class HomingMissileFactory(MissileFactory):
    def __init__(
        self,
        prototype: MissilePrototype,
        player: Entity,
        enemy_container: list[Enemy],
        name: str,
    ) -> None:
        super().__init__(prototype, player, name)
        self.enemy_container = enemy_container

    def shoot(self, missile_container: list[Missile]) -> None:
        distance: float | None = None
        target = None
        for enemy in self.enemy_container:
            d = (enemy.rect.x - self.player.rect.x) ** 2 + (
                enemy.rect.y - self.player.rect.y
            ) ** 2
            if distance is None:
                distance = d
                target = enemy
                continue
            if d < distance:
                distance = d
                target = enemy

        if target is None:
            missile = Missile(
                self.prototype,
                (self.player.rect.centerx, self.player.rect.centery - 5),
                "player",
            )
        else:
            missile = HomingMissile(
                self.prototype,
                (self.player.rect.centerx, self.player.rect.centery - 5),
                "player",
                target,
            )

        missile_container.append(missile)


class WayMissileFactory(MissileFactory):
    def __init__(
        self, prototype: MissilePrototype, player: Entity, num: int, name: str
    ) -> None:
        super().__init__(prototype, player, name)
        if num % 2 == 0:
            raise ValueError("num は 奇数を指定してください")
        self.num = num
        self.space = 20
        self.side_space = (180 - self.num * self.space) // 2
        center_num = self.num // 2
        self.offset = -90 - center_num * self.space

    def shoot(self, missile_container: list[Missile]) -> None:
        for i in range(self.num):
            missile = DiagonalMissile(
                self.prototype,
                (self.player.rect.centerx, self.player.rect.centery - 5),
                "player",
                i * self.space + self.offset,
            )
            missile_container.append(missile)


@dataclass
class MissilePrototype:
    image_path: str
    image_size: tuple[int, int]
    speed: int

    def __post_init__(self) -> None:
        self.image = load_image(self.image_path)
