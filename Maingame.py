import pygame
import random
import math
from player import Player
from enemy import Enemy
from camera import Camera
from room_generation import generate_room , Wall ,  Gate , Floor ,Floor_Hallway , Room 
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
level_1data = [
    {"x": 50, "y": 50, "form": 2, "type": 1, "enemies_counter": 3},
    {"x": ROOM_WIDTH + 50 + 240 + 100, "y": 50, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 2, "y": 50, "form": 3, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 2, "y": 50 - (ROOM_HEIGHT + 260), "form": 8, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 2, "y": -50 + ROOM_HEIGHT + 260, "form": 10, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 3, "y": 50 - (ROOM_HEIGHT + 260), "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 4, "y": 50 - (ROOM_HEIGHT + 260), "form": 6, "type": 1, "enemies_counter": 3},
    {"x": 50, "y": ROOM_HEIGHT + 50 + 260, "form": 5, "type": 1, "enemies_counter": 3},
    {"x": 50, "y": 30 + (ROOM_HEIGHT + 260) * 2, "form": 11, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100), "y": 30 + (ROOM_HEIGHT + 260) * 2, "form": 2, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 2, "y": 30 + (ROOM_HEIGHT + 260) * 2, "form": 6, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100), "y": 10 + (ROOM_HEIGHT + 260) * 4, "form": 11, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) , "y": 30 + (ROOM_HEIGHT + 260) * 3, "form": 5, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 2, "y": 10 + (ROOM_HEIGHT + 260) * 4, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (ROOM_WIDTH + 240 + 100) * 3, "y": 10 + (ROOM_HEIGHT + 260) * 4, "form": 6, "type": 1, "enemies_counter": 3}
]



Rooms = pygame.sprite.Group()
floors = pygame.sprite.Group()
kills = 0
camera = Camera(800,600 , 12000,12000)

floors.add(Floor(50,50))
def Room_Create ( x , y  , form , type , enemies_counter):
    walls.add(generate_room(x,y,form,type))
    floors.add(Floor(x,y))
    
    
    Rooms.add(Room(x,y+50,enemies_counter))
    if form == 1 or form == 2 or form ==9 or form == 8 or form == 11 or form ==7 :   # right corridor  
         floors.add(Floor_Hallway(x + 677 , y + 195 , 300 , 90))
    if form == 1 or form == 2 or form == 3 or form == 4 or form == 5 or form ==8 : # bottom corridor 
        floors.add(Floor_Hallway( x + 250 , y + 480 , 210 , 260 ))
    if form ==1 or form == 2 or form == 3 or form == 4 or form ==6 or form == 9  : # left corrior 
        floors.add(Floor_Hallway( x  - 300 , y + 195 , 300 ,  90 ))	
    if form == 1 or form == 3 or form ==4 or form == 5  or form == 7 : # top corridor , 
        floors.add(Floor_Hallway( x + 250 , y -  230   , 210 , 255 ))

    
player = Player()
#############################
walls = generate_room(-300- ROOM_WIDTH , 50 , 7 ,1) # initiate first room 
floors.add(Floor(-300- ROOM_WIDTH , 50))
floors.add(Floor_Hallway(-250- ROOM_WIDTH - 30 + 677 , 50 + 195 , 400 , 90))
#############################

for room_data in level_1data:
    Room_Create(room_data["x"], room_data["y"], room_data["form"], room_data["type"], room_data["enemies_counter"])


enemies = pygame.sprite.Group()
enemies_counter = 0
copy = walls.copy()
spawn_delay = 5000 
last_spawn_time = 0


running = True
stop = False


    
player.rect.center = ( -250 , 50 + ROOM_HEIGHT/2 )  # - move the player to the room 

# Main game loop  

   
while running:
    #print(enemies_counter)
    if stop == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        for room in Rooms :
            if player.rect.colliderect(room.rect) and room.active == False:
                room.active = True
                #enemies_counter = room.enemies_counter
        
        # Game logic updates
        if enemies_counter > 0:
            for wall in walls:
                if isinstance(wall, Gate) and wall.is_open:
                    wall.toogle(walls)
        
        if enemies_counter <= 0: 
            for wall in walls:
                if isinstance(wall, Gate) and not wall.is_open:
                    wall.toogle(walls)
        for room in Rooms :
          if  room.active == True  and enemies_counter <= 0 and room.clear == False :
            enemies_counter = room.enemies_counter
            enemies_to_spawn = enemies_counter
            last_spawn_time = pygame.time.get_ticks()
            room.clear = True 
            while enemies_to_spawn > 0:
                x = random.randint(room.rect.x, room.rect.x  + ROOM_WIDTH - 160)
                
                y = random.randint(room.rect.y, room.rect.y  + ROOM_HEIGHT - 160)
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
        mouse_world_x = pygame.mouse.get_pos()[0] - camera.camera.x
        mouse_world_y = pygame.mouse.get_pos()[1] - camera.camera.y
        dx = mouse_world_x - player.rect.centerx
        dy = mouse_world_y - player.rect.centery
        player_angle = math.degrees(math.atan2(-dx, -dy)) % 360 + 90
        original_image = player.original_image  # Store the original unrotated image in the Player class
        rotated_image = pygame.transform.rotate(player.original_image, player_angle)
        rotated_rect = rotated_image.get_rect(center=player.rect.center)

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
        screen.blit(rotated_image, rotated_rect.topleft + pygame.math.Vector2(camera.camera.topleft))
        
        
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
