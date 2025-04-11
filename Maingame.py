import pygame
import random
import math
from player import Player
from enemy import Enemy
from camera import Camera
from room_generation import generate_room , Wall ,  Gate , Floor
from UI_components import draw_health_bar


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


ROOM_WIDTH, ROOM_HEIGHT = 700, 500
CELL_SIZE = 40

floors = pygame.sprite.Group()
kills = 0
camera = Camera(800,600 , 2000,2000)

floors.add(Floor(50,50))
player = Player()
walls = generate_room()
enemies = pygame.sprite.Group()
enemies_counter = 0
copy = walls.copy()
spawn_delay = 5000 
last_spawn_time = 0

running = True
stop = False 
# ... (keep all your previous code until the main loop)

running = True
stop = False

def draw_health_bar(surface, current_hp, max_hp):
    bg_rect = pygame.Rect(20, 20, 200 , 20)
    pygame.draw.rect(surface, WHITE, bg_rect)

    health_width = int((current_hp / max_hp) * 200)
    health_rect = pygame.Rect(20, 20, health_width, 20 )
    
    pygame.draw.rect(surface, RED, health_rect)
    pygame.draw.rect(surface, BLACK, bg_rect, 2) 
while running:
    if stop == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Game logic updates
        if enemies_counter > 0:
            for wall in walls:
                if isinstance(wall, Gate) and wall.is_open:
                    wall.toogle(walls)
        
        if enemies_counter <= 0: 
            for wall in walls:
                if isinstance(wall, Gate) and not wall.is_open:
                    wall.toogle(walls)

        if enemies_counter <= 0 and pygame.time.get_ticks() - last_spawn_time > spawn_delay:
            enemies_counter = random.randint(1, 6)
            enemies_to_spawn = enemies_counter
            last_spawn_time = pygame.time.get_ticks()
            
            while enemies_to_spawn > 0:
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                enemy = Enemy(x, y)
                
                if not any(enemy.rect.colliderect(wall.rect) for wall in walls):
                    enemies.add(enemy)
                    enemies_to_spawn -= 1

        # Player input and updates
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click
    # Get mouse position in WORLD coordinates
          mouse_world_x = pygame.mouse.get_pos()[0] - camera.camera.x
          mouse_world_y = pygame.mouse.get_pos()[1] - camera.camera.y
    
    # Calculate direction relative to player's WORLD position
          dx = mouse_world_x - player.rect.centerx
          dy = mouse_world_y - player.rect.centery
          dist = max(1, math.sqrt(dx*dx + dy*dy))
          player.shoot((dx/dist, dy/dist))
        player.update(walls)
        camera.update(player)

       
        screen.fill(BLACK)
        for tear in player.tears[:]:
         if tear.update():
            if tear in player.tears:
                player.tears.remove(tear)
         else:
            for enemy in enemies:
                if tear.rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if tear in player.tears:
                        player.tears.remove(tear)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        kills +=1 
                        enemies_counter -=1
                    break
        
        for floor in floors:
            screen.blit(floor.image, camera.apply(floor))
        for wall in walls:
            screen.blit(wall.image, camera.apply(wall))
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy))        
        screen.blit(player.image, camera.apply(player))
        # Draw tears with camera offset
        for tear in player.tears:
            adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
            screen.blit(tear.image, adjusted_pos)
        enemies.update(player, walls)
        
        for tear in player.tears[:]:
            tear.update()
            for wall in walls:
                if tear.rect.colliderect(wall.rect):
                    player.tears.remove(tear)
                    break
        for enemy in enemies:
          if player.rect.colliderect(enemy.rect):
            player.health -= 0.1 

        # Health and UI elements (drawn without camera offset)
        font = pygame.font.SysFont(None, 36)
        health_text = font.render(f"Hearts: {int(player.health)}", True, WHITE)
        coordinates  = font.render(f"Player coordinates: X  {int(player.rect.x)} Y  {int(player.rect.y)}", True, WHITE)
        
        draw_health_bar(screen,player.health, player.max_health)
        screen.blit(coordinates, (20, 50))
        if player.health <= 1:
            pygame.quit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
