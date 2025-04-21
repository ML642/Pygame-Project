import pygame
import random
import math
from drop import Drop

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, drops , scale_x = 1, scale_y = 1): 
        super().__init__()
        self.orig = pygame.image.load('images/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = (random.uniform(1,2)) * scale_x
        self.health = 3
        self.drops = drops
        
        
        
        self.flag_X1 = 1
        self.flag_Y1 = 1
         
        self.flag_X = 1
        self.flag_Y = 1
        
    def update(self, player, walls):
        self.flag_X = True  
        self.flag_Y = True 
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
                self.flag_X = False
                break
            
        
                
        new_rect = self.rect.copy()
        new_rect.y += dy * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dy = 0
                self.flag_Y = False
                break
            
        if self.flag_X == False :
            if self.flag_X1 == 1  :   
                if  self.flag_X == False :
                    if player.rect.centery < self.rect.centery:
                        dy = -1
                        self.flag_X1 = True 
                    if player.rect.centery > self.rect.centery:
                        dy = +1
                        self.flag_X1 = False
            else :
                   if self.flag_X1 == True  :
                       dy = -1
                   else : 
                       dy = 1
        else :
            self.flag_X1 = 1    
            
        if self.flag_Y == False and self.flag_X == True :
            if self.flag_Y1 == 1  :   
                if  self.flag_Y == False :
                    if player.rect.centerx < self.rect.centerx:
                        dx = +1
                        self.flag_Y1 = True 
                    if player.rect.centerx > self.rect.centerx:
                        dx = -1
                        self.flag_Y1 = False
            else :
                   if self.flag_Y1 == True  :
                       dx = +1
                   else : 
                       dx = -1
        else :
            self.flag_Y1 = 1   
        
        
                
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Minor stuff cheking if enemy is done. Needed for droping items.
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.drop_item()
            self.kill()
    
    

    def drop_item(self):
        drop_chance = random.random()
        if drop_chance < 0.2:
            x, y = self.rect.center
            health_drop = Drop(x, y, "hp") # "ammo" is a hollow type, because this system is not finished yet. Done just in case.
            self.drops.add(health_drop)
        elif drop_chance < 0.4:
            x, y = self.rect.center
            ammo_drop = Drop(x, y, "ammo")
            self.drops.add(ammo_drop)