import pygame
import math
import random
import time
from player import Tear
from enemy import Enemy

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, player, scale_x=1, scale_y=1, drops=None, difficulty="medium"):
        super().__init__()
        self.image_orig = pygame.image.load('images/Boss1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (120 * scale_x, 120 * scale_y))
        self.rect = self.image.get_rect(center=(x, y))
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.health = 1000
        self.max_health = 1000
        self.speed = 2 * scale_x
        self.player = player
        self.shoot_cooldown = 0.1
        self.last_shot_time = 0
        self.tears = []
        self.attack_distance = 300 * scale_x
        self.safe_distance = 400 * scale_x
        self.drops = drops if drops else pygame.sprite.Group()
        self.roll_cooldown = 5
        self.last_roll_time = time.time()
        self.dashing = False
        self.dash_direction = pygame.Vector2(0, 0)
        self.dash_start_time = 0
        self.dash_duration = 0.2
        self.dash_speed = 14 * self.scale_x
        self.phase = 1
        self.phase_2_spawned = False
        self.reloading = False
        self.reload_time = 3
        self.reload_start_time = 0
        self.shots_fired = 0
        self.difficulty = difficulty


    def update(self, player=None, walls=None):
        current_time = time.time()
        if self.dashing:
            if time.time() - self.dash_start_time < self.dash_duration:
                move = self.dash_direction * self.dash_speed

                new_rect = self.rect.move(move.x, 0)
                if not any(new_rect.colliderect(w.rect) for w in walls):
                    self.rect.x += move.x

                new_rect = self.rect.move(0, move.y)
                if not any(new_rect.colliderect(w.rect) for w in walls):
                    self.rect.y += move.y
                return
            else:
                self.dashing = False


        if self.phase == 1:
            self.rect.center = (self.rect.centerx, self.rect.centery)
            self.shoot_cooldown = 0.05
            self.reload_time = 4
            self.speed = 0
            self.roll_cooldown = 9999
        elif self.phase == 2:
            self.shoot_cooldown = 0.1
            self.reload_time = 3
            self.speed = 2 * self.scale_x
            self.roll_cooldown = 5
        elif self.phase == 3:
            self.shoot_cooldown = 0.1
            self.reload_time = 3
            self.speed = 2 * self.scale_x
            self.roll_cooldown = 1.5



        # roll
        if current_time - self.last_roll_time >= self.roll_cooldown:
            self.dodge()
            self.last_roll_time = current_time

        # ai movement
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance

        move_x, move_y = 0, 0

        if distance < self.attack_distance:
            move_x = -dx * self.speed
            move_y = -dy * self.speed
        elif distance > self.safe_distance:
            move_x = dx * self.speed
            move_y = dy * self.speed

        new_rect = self.rect.copy()
        new_rect.x += move_x
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect.x += move_x

        new_rect = self.rect.copy()
        new_rect.y += move_y
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect.y += move_y

        # Shooting and reloading mechanics
        if not self.reloading and current_time - self.last_shot_time >= self.shoot_cooldown:
            self.shoot()
            self.shots_fired += 1
            self.last_shot_time = current_time

            if self.shots_fired >= 30:
                self.reloading = True
                self.reload_start_time = current_time
                self.shots_fired = 0

        if self.reloading and current_time - self.reload_start_time >= self.reload_time:
            self.reloading = False

        # Bullet update
        for tear in self.tears[:]:
            if tear.update():
                self.tears.remove(tear)
                continue

            if walls and any(tear.rect.colliderect(wall.rect) for wall in walls):
                self.tears.remove(tear)

        health_ratio = self.health / self.max_health
        if health_ratio > 2 / 3:
            self.phase = 1
        elif health_ratio > 1 / 3:
            if self.phase != 2:
                self.phase = 2
                if not self.phase_2_spawned:
                    self.spawn_minions()
                    self.phase_2_spawned = True
        else:
            self.phase = 3


    def shoot(self):
        # Shooting ai
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            direction = (dx / distance, dy / distance)
            bullet = Tear(self.rect.centerx, self.rect.centery, direction, speed=10, damage=80, scale_x=self.scale_x, scale_y=self.scale_y)
            angle = math.degrees(math.atan2(-direction[1], direction[0]))
            bullet.image = pygame.transform.rotate(bullet.image, angle)
            self.tears.append(bullet)

    def draw_health_bar(self, surface, scale_x, scale_y):
        # Health bar
        bar_width = 400 * scale_x
        bar_height = 25 * scale_y
        bar_x = (surface.get_width() - bar_width) / 2
        bar_y = 540 * scale_y
        health_ratio = self.health / self.max_health

        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            self.drop_loot()

    def drop_loot(self):
        
        pass

    def dodge(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        player_dir = pygame.Vector2(dx / distance, dy / distance)
        while True:
            angle = random.uniform(0, 2 * math.pi)
            dodge_dir = pygame.Vector2(math.cos(angle), math.sin(angle))

            if player_dir.dot(dodge_dir) < 0:
                break

        self.dash_direction = dodge_dir
        self.dashing = True
        self.dash_start_time = time.time()
    from enemy import Enemy

    def spawn_minions(self):
        for _ in range(4):
            for _ in range(10):
                offset_x = random.randint(-150, 150)
                offset_y = random.randint(-150, 150)
                spawn_x = self.rect.centerx + offset_x
                spawn_y = self.rect.centery + offset_y
                enemy = Enemy(spawn_x, spawn_y, self.drops, self.scale_x, self.scale_y, self.difficulty)

                if not any(enemy.rect.colliderect(w.rect) for w in self.groups()[0] if isinstance(w, pygame.sprite.Sprite)):
                    self.groups()[0].add(enemy) 
                    break


