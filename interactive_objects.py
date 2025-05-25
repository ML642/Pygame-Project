import random
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
    def __init__(self, x, y, width, height, damage=10, scale_x = 1 , scale_y = 1):
        super().__init__()
        self.damage = damage
        self.image = pygame.image.load('images/spikes.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width * scale_x, height * scale_y))
        self.rect = self.image.get_rect(topleft=(x * scale_x, y * scale_y))

    def update(self, player=None):
        if self.rect.colliderect(player.rect) and not player.invincible:
            player.health -= self.damage
            self.apply_damage(player)

    def apply_damage(self, target):
        if hasattr(target, "take_damage"):
            target.take_damage(self.damage)


class ExplosiveBarrel(DestructibleObject):
    def __init__(self, x, y, width, height, hp=40, explosion_radius=100, explosion_damage=25, scale_x = 1 ,scale_y = 1, explosion_group=None):
        super().__init__(x, y, width, height, hp, color=(255, 100, 0), scale_x  = scale_x,scale_y=scale_y)
        self.explosion_radius = explosion_radius * scale_x
        self.explosion_damage = explosion_damage
        self.image = pygame.image.load('images/explosive.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width * scale_x, height * scale_y))
        self.explosion_group = explosion_group
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.explosion_effects = []

    def take_damage(self, amount, enemies_group=None,player=None , objects = None,enemies_counter = 0):
        print("ouch")
        self.hp -= amount
        if self.hp <= 0:
            enemies_counter = self.explode(enemies_group, player, objects,enemies_counter)

            self.kill()
        return enemies_counter

    def explode(self, enemies_group = None, player=None, objects=None,enemies_counter = 0):
        print("BOOM!")

        if enemies_group :
            for enemy in enemies_group:
                distance = math.hypot(self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery)
                if hasattr(enemy, "take_damage"):
                    if distance <= self.explosion_radius:
                        if enemy.take_damage(self.explosion_damage) == "kill":
                            enemies_counter -= 1
                else :
                    distance = math.hypot(self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery)
                    if distance <= self.explosion_radius:
                        enemy.health -= self.explosion_damage
        if player:
            distance = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if distance <= self.explosion_radius:
                        player.health -= self.explosion_damage
        if objects:
            for object in objects:
                distance = math.hypot(self.rect.centerx - object.rect.centerx, self.rect.centery - object.rect.centery)
                if hasattr(object, "take_damage"):
                 if distance <= self.explosion_radius:
                    object.take_damage(self.explosion_damage)
        if hasattr(self, "explosion_group") and self.explosion_group:
            explosion = ExplosionEffect(self.rect.center)
            self.explosion_group.add(explosion)
        return enemies_counter

class BreakableWall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, hp, scale_x=1, scale_y=1, on_destroy=None):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((139, 69, 19))  # коричневый цвет, или используй свой спрайт
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp
        self.on_destroy = on_destroy

    def take_damage(self, damage):
        self.hp -= damage
        print(f"[DEBUG] Стена получила урон: {damage}, осталось HP: {self.hp}")
        if self.hp <= 0:
            print("[DEBUG] Стена разрушена, вызываем on_destroy")
            if self.on_destroy:
                self.on_destroy()
            self.kill()


class Chest(pygame.sprite.Sprite):
    _closed_image_original = None

    def __init__(self, x, y, ROOM_HEIGHT, width=50, height=50, content_type=None, scale_x=1, scale_y=1):
        super().__init__()
        self.scale_x = scale_x
        self.scale_y = scale_y

        if Chest._closed_image_original is None:
            Chest._closed_image_original = pygame.image.load("images/chest_closed.png").convert_alpha()

        self.image_closed = pygame.transform.scale(
            Chest._closed_image_original,
            (int(width * scale_x), int(height * scale_y))
        )
        self.image = self.image_closed
        self.rect = self.image.get_rect(midbottom=(x, y + ROOM_HEIGHT * 0.95 * scale_y))
        self.is_open = False
        self.content_type = content_type or random.choice(['health', 'speed', 'strength', 'debuff'])
        self.potion_image = None

    def open(self):
        if not self.is_open:
            self.is_open = True
            self.potion_image = pygame.transform.scale(
                pygame.image.load(f"images/potion_{self.content_type}.png").convert_alpha(),
                (int(self.rect.width * 0.8), int(self.rect.height * 1.2))
            )
            self.image = self.potion_image
            self.rect = self.image.get_rect(center=self.rect.center)
        return self

    def update(self, player):
        if self.is_open and self.rect.colliderect(player.rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.apply_effect(player)
                self.kill()

    def apply_effect(self, player):
        if self.content_type == 'health':
            player.heal(20)
        elif self.content_type == 'speed':
            player.add_buff('speed', 5)
        elif self.content_type == 'strength':
            player.add_buff('strength', 5)
        elif self.content_type == 'debuff':
            player.add_debuff('random', 5)

