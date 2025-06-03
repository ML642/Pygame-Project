
import random
import pygame
import math


class DestructibleObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, hp, color=(150, 150, 150), scale_x = 1, scale_y = 1):
        super().__init__()
        self.hp = hp
        self.max_hp = hp
        self.image = pygame.image.load('images/destructable_object.png').convert_alpha()
        
        self.image = pygame.transform.scale(self.image, (width * scale_x, height * scale_y))
       
    
        self.rect = self.image.get_rect(topleft=(x * scale_x, y *  scale_y))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        hp_ratio = max(self.hp / self.max_hp, 0)
        bar_width = self.rect.width
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 5, bar_width, 5))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 5, bar_width * hp_ratio, 5))


class SpikeTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, damage=10, scale_x = 1 , scale_y = 1):
        super().__init__()
        self.damage = damage

        try:
            image = pygame.image.load('images/spikes.jpg').convert_alpha()
        except:
            image = pygame.Surface((width, height))
            image.fill((200, 0, 0)) 

        scaled_width = int(width * scale_x)
        scaled_height = int(height * scale_y)

        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(topleft=(x * scale_x, y * scale_y))

    def update(self, player=None, enemies=None):
        if self.rect.colliderect(player.rect) and not player.invincible:
            player.health -= self.damage
            self.apply_damage(player)
        if enemies:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.apply_damage(enemy)

    def apply_damage(self, target):
        if hasattr(target, "take_damage"):
            return target.take_damage(self.damage)
        return None


class ExplosiveBarrel(DestructibleObject):
    def __init__(self, x, y, width, height, hp=40, explosion_radius=100, explosion_damage=25,
                 scale_x=1, scale_y=1, explosion_group=None):
        super().__init__(x, y, width, height, hp, color=(255, 100, 0), scale_x=scale_x, scale_y=scale_y)
        self.explosion_radius = explosion_radius * scale_x
        self.explosion_damage = explosion_damage
        self.explosion_group = explosion_group

        self.default_color = (255, 100, 0)
        self.flash_color = (255, 255, 0)

        try:
            self.original_image = pygame.image.load('images/explosive.png').convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (int(width * scale_x), int(height * scale_y)))
        except:
            self.original_image = pygame.Surface((int(width * scale_x), int(height * scale_y)))
            self.original_image.fill(self.default_color)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x * scale_x, y * scale_y))

        self.exploded = False
        self.flash_time = 200 
        self.explosion_start_time = None

    def take_damage(self, amount, enemies=None, player=None, objects=None, enemies_counter=0):
        self.hp -= amount
        if self.hp <= 0 and not self.exploded:
            self.exploded = True
            self.explosion_start_time = pygame.time.get_ticks()
            self.image.fill(self.flash_color) 
            enemies_counter = self.explode(enemies, player, objects, enemies_counter)
        return enemies_counter

    def explode(self, enemies=None, player=None, objects=None, enemies_counter=0):
        print("BOOM!")

        if enemies:
            for enemy in enemies:
                distance = math.hypot(self.rect.centerx - enemy.rect.centerx,
                                      self.rect.centery - enemy.rect.centery)
                if distance <= self.explosion_radius:
                    if hasattr(enemy, "take_damage") and enemy.take_damage(self.explosion_damage) == "kill":
                        enemies_counter -= 1

        if player:
            distance = math.hypot(self.rect.centerx - player.rect.centerx,
                                  self.rect.centery - player.rect.centery)
            if distance <= self.explosion_radius:
                player.health -= self.explosion_damage
                print(f"Player took {self.explosion_damage} damage! Health now {player.health}")

        if objects:
            for obj in objects:
                distance = math.hypot(self.rect.centerx - obj.rect.centerx,
                                      self.rect.centery - obj.rect.centery)
                if hasattr(obj, "take_damage") and distance <= self.explosion_radius:
                    obj.take_damage(self.explosion_damage)

        return enemies_counter

    def update(self):
        if self.exploded and self.explosion_start_time:
            current_time = pygame.time.get_ticks()
            if current_time - self.explosion_start_time >= self.flash_time:
                self.kill()


class BreakableWall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, hp=1, scale_x=1, scale_y=1, on_destroy=None):
        super().__init__()

        self.width = int(w * scale_x)
        self.height = int(h * scale_y)
        self.image = pygame.image.load("images/Wall.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


        self.rect = self.image.get_rect()
        self.rect.topleft = (int(x * scale_x), int(y * scale_y))

        self.hp = hp
        self.on_destroy = on_destroy

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            if self.on_destroy:
                self.on_destroy()
            self.kill()



class Chest(pygame.sprite.Sprite):
    _closed_image_original = None

    def __init__(self, x, y, width=50, height=50, content_type=None, scale_x=1, scale_y=1):
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
        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_open = False
        self.content_type = content_type or random.choice(['health', 'speed', 'strength', 'debuff'])
        self.potion_image = None

    def open(self):
        if not self.is_open:
            self.is_open = True
            self.potion_image = pygame.transform.scale(
                pygame.image.load(f"images/potion.png").convert_alpha(),
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
