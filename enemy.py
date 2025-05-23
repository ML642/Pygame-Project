import pygame
import random
import math
from drop import Drop
from player import Tear


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, drops , scale_x = 1, scale_y = 1,difficulty = 1): 
        super().__init__()
        if difficulty == "easy": 
          self.multiplier = 0.5 
        elif difficulty == "medium":
            self.multiplier = 1
        elif difficulty == "hard":
            self.multiplier = 1.75
        
        self.orig = pygame.image.load('images/player.png').convert_alpha()
        self.orig2 =pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        self.image = pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = (random.uniform(1,2)) * scale_x * self.multiplier
        self.health = 30* self.multiplier
        self.drops = drops
        
        self.scale_x = scale_x
        self.scale_y = scale_y
        
        self.tears = []
        
        self.last_shot_time = 0
        self.can_shoot = True
        
        self.shoot_cooldown = 600
        
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
        
        raw_angle = math.degrees(math.atan2(dx, dy)) % 360
        angle = raw_angle + 270

        # 3) Rotate the original, then update image & rect
        rotated = pygame.transform.rotate(self.orig2, angle)
        self.image = rotated
        # Re-center so the sprite doesn’t “jump” around
        self.rect = self.image.get_rect(center=self.rect.center)
        
        for tear in self.tears:
            if tear.update():
                self.tears.remove(tear)
        
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
    def shoot(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        dx, dy = dx/dist, dy/dist
        
        
        
        tear = Tear(self.rect.centerx, self.rect.centery,(dx, dy),7,10,self.scale_x, self.scale_y)
        
        angle = math.degrees(math.atan2(dx, dy))  + 90
        tear.image = pygame.transform.rotate(tear.image, angle)
        self.tears.append(tear)
        
    def take_damage(self , amount ):
        self.health -=  amount 
        if self.health <= 0:
            self.drop_item()
            self.kill()
            return "kill"
    

    def drop_item(self):
        drop_chance = random.random()
        if drop_chance < 0.2:
            x, y = self.rect.center
            health_drop = Drop(x, y, "hp") # "ammo" is a hollow type, because this system is not finished yet.
            self.drops.add(health_drop)
        elif drop_chance < 0.4:
            x, y = self.rect.center
            ammo_drop = Drop(x, y, "ammo")
            self.drops.add(ammo_drop)