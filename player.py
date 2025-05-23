import pygame
import random
import math
from grenade import Grenade



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
        self.trail_positions = []  # Store positions for trail
        self.max_trail_length = 5 
    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.lifetime -= 1
        self.trail_positions.append((self.rect.centerx, self.rect.centery))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        return self.lifetime <= 0
    



BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self,scale_x = 1 ,scale_y = 1 , difficulty = "medium"):
        super().__init__()
        if difficulty == "easy": 
            self.multiplier = 1.5
        elif difficulty == "medium":
            self.multiplier = 1
        elif difficulty == "hard":
            self.multiplier = 0.75
        self.orig = pygame.image.load('images/player.png').convert_alpha()
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.image = pygame.transform.scale(self.orig, (50 * scale_x, 50 * scale_y))
        self.original_image = self.image 
        self.rect = self.image.get_rect(center=(400 * self.scale_x, 300 * self.scale_y))
        self.speed = 5 *  self.multiplier
        self.health = 30 * self.multiplier
        self.max_health = 30 * self.multiplier
        self.shot_cooldown = 0
        self.tears = []  # Projectiles
        self.angle = 180
        
        #dash mechanics
        self.dash_speed_multiplier = 3
        self.dash_duration = 10  # frames
        self.dash_cooldown = 60  # frames
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.is_dashing = False
        self.dash_direction = (0, 0)
        self.invincible = False
        
        self.dash_trail = []
        self.max_trail_points = 8
        
        self.speed = 5 
        self.health = 300
        self.max_health = 300
        self.tears = []  
        self.angle = 0

        self.last_shot_time = 0
        self.current_mode = 1  # режим стрельбы по умолчанию
        
        self.is_reloading = False
        self.reload_start_time = 0

        

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1
            
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.invincible = False
        if not self.is_dashing:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= self.speed  * self.scale_x
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += self.speed * self.scale_x
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy -= self.speed *  self.scale_y
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += self.speed * self.scale_y
            
        # Diagonal movement normalization
            if dx != 0 and dy != 0:
                dx *= 0.7071    # 1/sqrt(2)
                dy *= 0.7071
        else:
            # Dash movement
            dx = self.dash_direction[0] * self.speed * self.dash_speed_multiplier * self.scale_x
            dy = self.dash_direction[1] * self.speed * self.dash_speed_multiplier * self.scale_y    
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
        if self.is_dashing:
            self.dash_trail.append((self.rect.centerx, self.rect.centery))
            if len(self.dash_trail) > self.max_trail_points:
                self.dash_trail.pop(0)        
        self.rect.x += dx 
        self.rect.y += dy
        
    def shoot(self, direction, Fire_mode):
        import time
        
        FIRE_MODES = Fire_mode 
        if self.is_reloading:
          return Fire_mode
        mode = FIRE_MODES[self.current_mode]
        current_time = time.time()

        if current_time - self.last_shot_time >= mode["fire_rate"]:
            if mode.get("type") == "grenade":
                if mode["ammo"] <= 0:
                    return FIRE_MODES  # нет гранат

                FIRE_MODES[self.current_mode]["ammo"] -= 1
                grenade = Grenade(self.rect.centerx, self.rect.centery, direction,
                                  mode["speed"],
                                  mode["damage"],
                                  mode["radius"],
                                  self.scale_x, self.scale_y)
                self.tears.append(grenade)
                self.last_shot_time = current_time
                return FIRE_MODES
            else:
                if mode["bullets"] <= 0:
                    return FIRE_MODES

                FIRE_MODES[self.current_mode]["bullets"] -= 1
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
                return FIRE_MODES

            tear = Tear(
                self.rect.centerx,
                self.rect.centery,
                direction,
                speed = mode["speed"],
                damage = mode["damage"],
                scale_x=self.scale_x,
                scale_y=self.scale_y
            )
            angle = math.degrees(math.atan2(-direction[1], direction[0])) + 180
            tear.image = pygame.transform.rotate(tear.image, angle)
            self.tears.append(tear)
            self.last_shot_time = current_time            
        return Fire_mode
    def dash(self):
        if self.dash_cooldown_timer <= 0 and not self.is_dashing:
            # Get movement direction
            dx, dy = 0, 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy -= 1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += 1

            if dx == 0 and dy == 0:  # No movement input
                return
            
            # Normalize direction
            length = math.hypot(dx, dy)
            self.dash_direction = (dx/length, dy/length)
            
            # Activate dash
            self.is_dashing = True
            self.invincible = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown_timer = self.dash_cooldown
            self.dash_trail = []
    def take_damage(self, amount):
        self.health -= amount

            
