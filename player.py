import pygame
import random
import math

class Tear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=7, damage=10, scale_x=1, scale_y=1):
        super().__init__()
        self.orig = pygame.image.load('images/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.orig, (20 * scale_x, 20 * scale_y))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = direction
        self.lifetime = 50
        self.damage = damage

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.lifetime -= 1
        return self.lifetime <= 0
    



BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, scale_x=1, scale_y=1):
        super().__init__()
        self.orig = pygame.image.load('images/player.png').convert_alpha()
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        self.original_image = self.image 
        self.rect = self.image.get_rect(center=(400, 300))
        self.speed = 5 
        self.health = 300
        self.max_health = 300
        self.tears = []  
        self.angle = 0

        self.last_shot_time = 0
        self.current_mode = 1  # режим стрельбы по умолчанию

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]: dx -= self.speed * self.scale_x
        if keys[pygame.K_RIGHT]: dx += self.speed * self.scale_x
        if keys[pygame.K_UP]: dy -= self.speed * self.scale_y
        if keys[pygame.K_DOWN]: dy += self.speed * self.scale_y
        
        # Нормализация по диагонали
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        
        # Столкновения со стенами
        new_rect = self.rect.copy()
        new_rect.x += dx
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dx = 0
                break
                
        new_rect = self.rect.copy()
        new_rect.y += dy
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dy = 0
                break
                
        self.rect.x += dx 
        self.rect.y += dy

    def shoot(self, direction):
        import time
        FIRE_MODES = {
            1: {"speed": 7, "damage": 10, "fire_rate": 0.6},
            2: {"speed": 12, "damage": 5, "fire_rate": 0.3},
            3: {"speed": 5, "damage": 20, "fire_rate": 1},
        }

        mode = FIRE_MODES[self.current_mode]
        current_time = time.time()

        if current_time - self.last_shot_time >= mode["fire_rate"]:
            tear = Tear(
                self.rect.centerx,
                self.rect.centery,
                direction,
                speed=mode["speed"],
                damage=mode["damage"],
                scale_x=self.scale_x,
                scale_y=self.scale_y
            )
            angle = math.degrees(math.atan2(-direction[1], direction[0]))
            tear.image = pygame.transform.rotate(tear.image, angle)
            self.tears.append(tear)
            self.last_shot_time = current_time