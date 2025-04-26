
import pygame
import math

class DestructibleObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, color=(150, 150, 150), k=1):
        super().__init__()
        self.hp = hp
        self.max_hp = hp
        self.image = pygame.Surface((width * k, height * k))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x * k, y * k))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Отрисовка полоски жизни
        hp_ratio = max(self.hp / self.max_hp, 0)
        bar_width = self.rect.width
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 5, bar_width, 5))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 5, bar_width * hp_ratio, 5))

class SpikeTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, damage=10, k=1):
        super().__init__()
        self.damage = damage
        self.image = pygame.Surface((width * k, height * k))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect(topleft=(x * k, y * k))

    def apply_damage(self, target):
        if hasattr(target, "take_damage"):
            target.take_damage(self.damage)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class ExplosiveBarrel(DestructibleObject):
    def __init__(self, x, y, width, height, hp=40, explosion_radius=100, explosion_damage=25, k=1):
        super().__init__(x, y, width, height, hp, color=(255, 100, 0), k=k)
        self.explosion_radius = explosion_radius * k
        self.explosion_damage = explosion_damage

    def take_damage(self, amount, enemies_group=None):
        self.hp -= amount
        if self.hp <= 0:
            if enemies_group:
                self.explode(enemies_group)
            self.kill()

    def explode(self, enemies_group):
        for enemy in enemies_group:
            if hasattr(enemy, "take_damage"):
                distance = math.hypot(self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery)
                if distance <= self.explosion_radius:
                    enemy.take_damage(self.explosion_damage)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
