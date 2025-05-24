import pygame
import random
import math
from drop import Drop
from player import Tear


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, drops, scale_x=1, scale_y=1, difficulty="medium"):
        super().__init__()

        if difficulty == "easy":
            self.multiplier = 0.5
            self.shoot_cooldown = 900
        elif difficulty == "medium":
            self.multiplier = 1
            self.shoot_cooldown = 600
        elif difficulty == "hard":
            self.multiplier = 1.75
            self.shoot_cooldown = 200

        self.scale_x = scale_x
        self.scale_y = scale_y
        self.drops = drops

        self.orig = pygame.image.load('images/player.png').convert_alpha()
        self.orig2 = pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        self.image = self.orig2
        self.rect = self.image.get_rect(center=(x, y))

        base_speed = random.uniform(1, 2)
        self.speed = base_speed * 0.7 * max(scale_x, scale_y)


        self.health = 30 * self.multiplier

        self.tears = []
        # self.shoot_cooldown = 600
        self.last_shot_time = 0
        self.can_shoot = True

        self.flag_X1 = 1
        self.flag_Y1 = 1
        self.flag_X = 1
        self.flag_Y = 1

    def update(self, player, walls):
        self.flag_X = True
        self.flag_Y = True

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        dx, dy = dx / dist, dy / dist

        angle = math.degrees(math.atan2(dx, dy)) % 360 + 270
        self.image = pygame.transform.rotate(self.orig2, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        for tear in self.tears:
            if tear.update():
                self.tears.remove(tear)

        # Collision with walls
        new_rect = self.rect.copy()
        new_rect.x += dx * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dx = 0
                self.flag_X = False
                break

        new_rect = self.rect.copy()
        new_rect.y += dy * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dy = 0
                self.flag_Y = False
                break

        if not self.flag_X:
            dy = -1 if player.rect.centery < self.rect.centery else 1

        if not self.flag_Y and self.flag_X:
            dx = 1 if player.rect.centerx < self.rect.centerx else -1

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def shoot(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        dx, dy = dx / dist, dy / dist

        tear_speed = 1 * self.scale_x
        tear = Tear(self.rect.centerx, self.rect.centery, (dx, dy), speed=tear_speed, damage=10 * self.multiplier, scale_x=self.scale_x, scale_y=self.scale_y)
        angle = math.degrees(math.atan2(-dy, dx))
        tear.image = pygame.transform.rotate(tear.image, angle)
        self.tears.append(tear)
        return tear

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.drop_item()
            self.kill()
            return "kill"

    def drop_item(self):
        drop_chance = random.random()
        x, y = self.rect.center
        if drop_chance < 0.2:
            self.drops.add(Drop(x, y, "hp"))
        elif drop_chance < 0.4:
            self.drops.add(Drop(x, y, "ammo"))
