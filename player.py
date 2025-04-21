import pygame
import random
import math


class Tear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction , scale_x =1 ,scale_y = 1):
        super().__init__()
        self.orig = pygame.image.load('images/bullet.png').convert_alpha()
        
        self.image = pygame.transform.scale(self.orig,(20 * scale_x,20 * scale_y)) 
        
        self.rect = self.image.get_rect(center=(x , y ))
        
        self.speed = 7 
        self.direction = direction
        self.lifetime = 50 * scale_x
        
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
    def __init__(self,scale_x = 1 ,scale_y = 1):
        super().__init__()
        self.orig = pygame.image.load('images/player.png').convert_alpha()
        self.scale_x = scale_x
        self.scale_y = scale_y
        
        self.image = pygame.transform.scale(self.orig,(50 * scale_x,50 * scale_y))
        self.original_image = self.image 
        self.rect = self.image.get_rect(center=(400, 300))
        self.speed = 5 
        self.health = 30
        self.max_health = 30
        self.shot_cooldown = 0
        self.tears = []  # Projectiles
        self.angle = 0
    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]: dx -= self.speed  * self.scale_x
        if keys[pygame.K_RIGHT]: dx += self.speed * self.scale_x
        if keys[pygame.K_UP]: dy -= self.speed *  self.scale_y
        if keys[pygame.K_DOWN]: dy += self.speed * self.scale_y
        
        # Diagonal movement normalization
        if dx != 0 and dy != 0:
            dx *= 0.7071    # 1/sqrt(2)
            dy *= 0.7071
        
        # Wall collision
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
        
        # Shooting cooldown
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            
    def shoot(self, direction):
        if self.shot_cooldown == 0:
            tear = Tear(self.rect.centerx, self.rect.centery, direction,self.scale_x ,self.scale_y)
            angle = math.degrees(math.atan2(-direction[1], direction[0]))
            tear.image = pygame.transform.rotate(tear.image, angle)
            self.tears.append(tear)
            self.shot_cooldown = 15
