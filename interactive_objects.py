import random 
import pygame
import math

class ExplosionEffect:
    def __init__(self, x, y, scale=1):
        self.particles = []
        self.x = x
        self.y = y
        self.scale = scale
        # Create explosion particles
        for _ in range(40):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(1, 5) * scale
            self.particles.append([
                x, y,  # Position
                math.cos(angle) * speed,  # dx
                math.sin(angle) * speed,  # dy
                random.uniform(2, 5) * scale,  # Size
                random.choice([(255, 165, 0), (255, 69, 0), (255, 255, 0)]),  # Color
                random.randint(20, 30)  # Lifetime
            ])

    def update(self):
        for p in self.particles:
            # Update position
            p[0] += p[2]
            p[1] += p[3]
            # Reduce size and lifetime
            p[4] = max(0, p[4] - 0.1)
            p[5] = (min(255, p[5][0]+2), min(255, p[5][1]+2), p[5][2])  # Fade to white
            p[6] -= 1

    def draw(self, screen):
        for p in self.particles:
            if p[6] > 0:
                pygame.draw.circle(screen, p[5], (int(p[0]), int(p[1])), int(p[4]))



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
       
        return enemies_counter