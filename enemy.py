import pygame
import random
import math
from drop import Drop
from player import Tear


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, drops, scale_x=1, scale_y=1, difficulty="medium", type="ranged"):
        super().__init__()
        self.type = type  # "ranged", "sniper", "melee"
        self.drops = drops
        self.scale_x = scale_x
        self.scale_y = scale_y

        # Load and scale image
        # self.orig = pygame.image.load('images/player.png').convert_alpha()
        # self.orig2 = pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        # self.image = self.orig2
        # self.rect = self.image.get_rect(center=(x, y))

        # Movement speed base
        base_speed = 1.5
        self.speed = base_speed * max(scale_x, scale_y)

        # Difficulty multiplier
        if difficulty == "easy":
            self.multiplier = 0.75
        elif difficulty == "hard":
            self.multiplier = 1.5
        else:
            self.multiplier = 1

        # Shared attributes
        self.tears = pygame.sprite.Group()
        self.last_shot_time = 0
        self.can_shoot = True

        # Behavior-specific configuration
        if self.type == "ranged":
            self.orig = pygame.image.load('images/enemy_ranged.png').convert_alpha()
            self.orig2 = pygame.transform.scale(self.orig, (int(50 * scale_x), int(50 * scale_y)))
            self.health = 60 * self.multiplier
            self.shoot_cooldown = 500
            self.attack_range = 350
            self.burst_count = 15
            self.burst_delay = 10
            self.bursting = False
            self.burst_timer = 0
            self.burst_shots_fired = 0
            self.damage = 5
            self.speed = 2 * max(scale_x, scale_y)

        elif self.type == "sniper":
            self.orig = pygame.image.load('images/enemy_sniper.png').convert_alpha()
            self.orig2 = pygame.transform.scale(self.orig, (int(50 * scale_x), int(50 * scale_y)))
            self.health = 20 * self.multiplier
            self.shoot_cooldown = 3000
            self.attack_range = 600
            self.damage = 15
            self.speed = 1 * max(scale_x, scale_y)

        elif self.type == "melee":
            self.orig = pygame.image.load('images/enemy_melee.png').convert_alpha()
            self.orig2 = pygame.transform.scale(self.orig, (int(60 * scale_x), int(60 * scale_y)))
            self.health = 40 * self.multiplier
            self.speed = 1.7 * max(scale_x, scale_y)
            self.attack_range = 30
            self.damage = 15
            self.attack_cooldown = 1000
            self.last_attack_time = 0
        self.image = self.orig2
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player, walls):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(dx, dy)) % 360 + 270
        self.image = pygame.transform.rotate(self.orig2, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.type == "ranged":
            self.update_ranged(player, walls)
        elif self.type == "sniper":
            self.update_sniper(player, walls)
        elif self.type == "melee":
            self.update_melee(player, walls)

        # Update projectiles
        for tear in self.tears.copy():
            if tear.update(walls):
                self.tears.remove(tear)

    def update_ranged(self, player, walls):
        distance = self.get_distance_to_player(player)
        self.move_to_range(player, self.attack_range, walls)

        now = pygame.time.get_ticks()
        if distance <= self.attack_range:
            if not self.bursting and now - self.last_shot_time >= self.shoot_cooldown:
                self.bursting = True
                self.burst_timer = now
                self.burst_shots_fired = 0

            if self.bursting and now - self.burst_timer >= self.burst_delay:
                tear = self.shoot(player)
                if tear:
                    self.tears.add(tear)
                self.burst_shots_fired += 1
                self.burst_timer = now

                if self.burst_shots_fired >= self.burst_count:
                    self.bursting = False
                    self.last_shot_time = now

    def update_sniper(self, player, walls):
        distance = self.get_distance_to_player(player)
        self.move_to_range(player, self.attack_range, walls)

        now = pygame.time.get_ticks()
        if distance <= self.attack_range and now - self.last_shot_time >= self.shoot_cooldown:
            tear = self.shoot(player)
            if tear:
                self.tears.add(tear)
            self.last_shot_time = now

    def update_melee(self, player, walls):
        self.move_towards(player, walls)
        now = pygame.time.get_ticks()
        if self.rect.colliderect(player.rect) and now - self.last_attack_time >= self.attack_cooldown:
            player.take_damage(self.damage)
            self.last_attack_time = now

    def move_towards(self, player, walls):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))

        move_x = int(self.speed * dx / dist)
        move_y = int(self.speed * dy / dist)

        original_pos = self.rect.topleft

        self.rect.x += move_x
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = original_pos[0]
            self.rect.y += int(self.speed)
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y = original_pos[1]
            else:
                return


        self.rect.y += move_y
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y = original_pos[1]
            self.rect.x += int(self.speed)
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x = original_pos[0]



    def move_to_range(self, player, target_range, walls):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > target_range + 20:
            self.move_towards(player, walls)
        elif distance < target_range - 20:
            self.move_away_from(player, walls)


    def get_distance_to_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return math.hypot(dx, dy)

    def move_away_from(self, player, walls):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        dist = max(1, math.hypot(dx, dy))
        move_x = int(self.speed * dx / dist)
        move_y = int(self.speed * dy / dist)

        original_pos = self.rect.topleft

        self.rect.x += move_x
        if any(self.rect.colliderect(w.rect) for w in walls):
            self.rect.x = original_pos[0]

        self.rect.y += move_y
        if any(self.rect.colliderect(w.rect) for w in walls):
            self.rect.y = original_pos[1]




    def shoot(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        dx, dy = dx / dist, dy / dist

        if self.type == "ranged":
            tear_speed = 6 * self.scale_x
        elif self.type == "sniper":
            tear_speed = 10 * self.scale_x
        else:
            return None
        damage = self.damage
        tear = Tear(
            self.rect.centerx,
            self.rect.centery,
            (dx, dy),
            speed=tear_speed,
            damage=damage,
            scale_x=self.scale_x,
            scale_y=self.scale_y
        )
        # print(f"[{self.type}] Shoot dmg {damage}")

        angle = math.degrees(math.atan2(-dy, dx)) + 180
        tear.image = pygame.transform.rotate(tear.image, angle)
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
