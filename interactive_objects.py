
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
        self.image = pygame.image.load('images/spikes.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width * scale_x, height * scale_y))
        self.rect = self.image.get_rect(topleft=(x * scale_x, y * scale_y))

    def apply_damage(self, target):
        if hasattr(target, "take_damage"):
            target.take_damage(self.damage)


class ExplosiveBarrel(DestructibleObject):
    def __init__(self, x, y, width, height, hp=40, explosion_radius=100, explosion_damage=25, scale_x = 1 ,scale_y = 1):
        super().__init__(x, y, width, height, hp, color=(255, 100, 0), scale_x  = scale_x,scale_y=scale_y)
        self.explosion_radius = explosion_radius * scale_x
        self.explosion_damage = explosion_damage
        self.image = pygame.image.load('images/explosive.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width * scale_x, height * scale_y))
    def take_damage(self, amount, enemies_group=None,player=None , objects = None):
        print("ouch")
        self.hp -= amount
        if self.hp <= 0:
            
            self.explode(enemies_group, player, objects)
            self.kill()

    def explode(self, enemies_group = None, player=None, objects=None):
        print("BOOM!")
        
        if enemies_group :
            for enemy in enemies_group:
                distance = math.hypot(self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery)
                if hasattr(enemy, "take_damage"):
                    if distance <= self.explosion_radius:
                        enemy.take_damage(self.explosion_damage)
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