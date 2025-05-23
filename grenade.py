import pygame
import math

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, damage, radius, scale_x=1, scale_y=1):
        super().__init__()
        self.image = pygame.image.load("images/grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30 * scale_x, 30 * scale_y))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = speed * scale_x
        self.damage = damage
        self.radius = radius * ((scale_x + scale_y) / 2)
        self.distance_travelled = 0
        self.max_distance = 1000 * scale_x
        self.bounce_count = 3
        self.explode_timer_started = False
        self.explode_start_time = 0
        self.explode_delay = 1000

        self.scale_x = scale_x
        self.scale_y = scale_y

    def update(self, walls):
        if self.explode_timer_started:
            if pygame.time.get_ticks() - self.explode_start_time >= self.explode_delay:
                return True
            return False

        move = self.direction * self.speed
        self.rect.x += move.x
        self.rect.y += move.y
        self.distance_travelled += self.speed

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if abs(move.x) > abs(move.y):
                    self.direction.x *= -1
                else:
                    self.direction.y *= -1
                self.bounce_count -= 1
                break

        self.speed *= 0.96

        if self.speed < 0.5 or self.bounce_count <= 0 or self.distance_travelled >= self.max_distance:
            self.explode_timer_started = True
            self.explode_start_time = pygame.time.get_ticks()

        return False

class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, scale_x=1, scale_y=1, duration=100):
        super().__init__()
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.radius = radius * ((scale_x + scale_y) / 2)
        size = int(self.radius * 2)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 100, 0, 120), (size // 2, size // 2), int(self.radius))
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration
