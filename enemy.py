import pygame
import random
import math

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)




class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.orig = pygame.image.load('images/Soldier1.png').convert_alpha()
        self.image = pygame.transform.scale(self.orig, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = (random.uniform(1,2))
        self.health = 3
        
    def update(self, player, walls):
        # moving towards player 
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        dx, dy = dx/dist, dy/dist
        
        # Wall collision
        new_rect = self.rect.copy()
        new_rect.x += dx * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dx = 0
                break
                
        new_rect = self.rect.copy()
        new_rect.y += dy * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dy = 0
                break
                
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed