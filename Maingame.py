import pygame
import random
import math
import os
import time 
import copy 
from player import Player, Tear
from enemy import Enemy
from camera import Camera
from room_generation import generate_boss_room, generate_room , Wall ,  Gate , Floor ,Floor_Hallway , Room 
from UI_components import draw_health_bar , Menu_option , DustParticle , draw_reload_bar , draw_minimap
from stopmenu import pause_menu , draw_button , draw_slider
from Main_Menu import Main_menu
from interactive_objects import  DestructibleObject , SpikeTrap , ExplosiveBarrel
from game_over import GameOver , game_over_screen ,  Restart
from boss import Boss

from setting_menu import SettingsMenu

from grenade import Grenade, ExplosionEffect
pygame.init()


explosions = pygame.sprite.Group()
interactive_objects = pygame.sprite.Group()
wall = DestructibleObject(x=5, y=5, width=32, height=32, hp=100, k=2)
spike = SpikeTrap(x=10, y=5, width=32, height=10, damage=15, k=2)
barrel = ExplosiveBarrel(x=15, y=5, width=32, height=32, hp=50, explosion_radius=64, explosion_damage=30, k=2)
interactive_objects.add(wall, spike, barrel)

screen_width = 800 
screen_height = 600
os.environ['SDL_VIDEO_CENTERED'] = "1"
BASE_WIDTH = 800 
BASE_HEIGHT = 600
# 1350 x 800
SELECTED_WIDTH = 800
SELECTED_HEIGHT = 600   

scale_x = SELECTED_WIDTH / BASE_WIDTH
scale_y = SELECTED_HEIGHT / BASE_HEIGHT

current_settings = {
    'resolution': (800, 600),
    'music_volume': 50,
    'sfx_volume': 50,
    'difficulty': 'medium'
}

    


screen = pygame.display.set_mode((800 * scale_x, 600 * scale_y))


clock = pygame.time.Clock()



BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
data = [ 0 , (800,600) ]
# data = 
# SELECTED_WIDTH,SELECTED_HEIGHT = data[1] 
current_settings = Main_menu(SELECTED_WIDTH , SELECTED_HEIGHT , current_settings)

scale_x = current_settings["resolution"][0] / BASE_WIDTH
scale_y = current_settings["resolution"][1] / BASE_HEIGHT
FIRE_MODES = {
            1: {"speed": 7, "damage": 10, "fire_rate": 0.6 ,"url": "images/pistol.png","bullets" : 10 , "ammo" :9  , "full" : 10 , "reload_time" :2 },
            2: {"speed": 12, "damage": 5, "fire_rate": 0.3 , "url": "images/shotgun.png" ,"bullets" : 10 , "ammo" : 2 , "full": 30 , "reload_time" :1.5 }, 
            3: {"speed": 20, "damage": 20, "fire_rate": 1 , "url": "images/sniper.png" , "bullets" : 10 ,   "ammo" : 3, "full":10 , "reload_time" : 2.5 },
            4: {"type": "grenade", "speed": 15, "damage": 100, "radius": 200, "fire_rate": 1.2, "url": "images/grenade.png", "bullets": None, "ammo": 3, "full": None, "reload_time": 0}
        }
FIRE_MODES_COPY = copy.deepcopy(FIRE_MODES)

ROOM_WIDTH, ROOM_HEIGHT = 700 * scale_x, 500 * scale_y
CELL_SIZE = 40



level_1data = [
    {"x": 50, "y": 50, "form": 2, "type": 1, "enemies_counter": 3},
    {"x": 700 + 50 + 240 + 100, "y": 50, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 50, "form": 3, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 50 - (500 + 260), "form": 8, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": -50 + 500 + 260, "form": 10, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 3, "y": 50 - (500 + 260), "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 4, "y": 50 - (500 + 260), "form": 6, "type": 1, "enemies_counter": 3},
    {"x": 50, "y": 500 + 50 + 260, "form": 5, "type": 1, "enemies_counter": 3},
    {"x": 50, "y": 30 + (500 + 260) * 2, "form": 11, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100), "y": 30 + (500 + 260) * 2, "form": 2, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 30 + (500 + 260) * 2, "form": 6, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100), "y": 10 + (500 + 260) * 4, "form": 11, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100), "y": 30 + (500 + 260) * 3, "form": 5, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 10 + (500 + 260) * 4, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 3, "y": 10 + (500 + 260) * 4, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 4, "y": 10 + (500 + 260) * 4, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": (50 + (700 + 240 + 100) * 5) - 60, "y": (10 + (500 + 260) * 4) - 110, "form": "boss", "type": 1, "enemies_counter": 0}
]




Rooms = pygame.sprite.Group()
floors = pygame.sprite.Group()
kills = 0

camera = Camera(800 * scale_x,600 * scale_y , 12000 * scale_x,12000 * scale_y, scale_x , scale_y)

# technical debt
floors.add(Floor(50 * scale_x,50 * scale_y))
def Room_Create ( x , y  , form , type , enemies_counter ):
    walls.add(generate_room(int(x ),int(y ),form,type , scale_x , scale_y))
    floors.add(Floor(x *  scale_x, y * scale_y,scale_x , scale_y))
    
    
    Rooms.add(Room(x  * scale_x,(y+50) * scale_y , enemies_counter,scale_x , scale_y))
    if form == 1 or form == 2 or form ==9 or form == 8 or form == 11 or form ==7 :   # right corridor  
         floors.add(Floor_Hallway((x + 677) * scale_x , (y + 195)* scale_y , 300  , 90  ,scale_x,scale_y))
    if form == 1 or form == 2 or form == 3 or form == 4 or form == 5 or form ==8 : # bottom corridor 
        floors.add(Floor_Hallway( (x + 250)*scale_x , (y + 480)*scale_y , 210  , 260 , scale_x ,  scale_y ))
    if form ==1 or form == 2 or form == 3 or form == 4 or form ==6 or form == 9  : # left corrior 
        floors.add(Floor_Hallway( (x  - 300) * scale_x , (y + 195)*scale_y , 300  ,  90  , scale_x , scale_y))	
    if form == 1 or form == 3 or form ==4 or form == 5  or form == 7 : # top corridor , 
        floors.add(Floor_Hallway( (x + 250) *  scale_x , (y -  230)* scale_y   , 210 , 255  ,scale_x ,scale_y ))

    

    
    return 0
    
OFFSET3 = 353
OFFSET2 = 1000
OFFSET = 700    
OFFSETY = (scale_y-1) * 2
player = Player (scale_x,scale_y , current_settings["difficulty"])  
#############################



walls = generate_room(int((-300 - ROOM_WIDTH) + int(OFFSET) * ( scale_x -1 ) )  ,int( 50 ), 7, 1, scale_x ,scale_y )  # initiate first room
floors.add(Floor((-300 - 700) - int(OFFSET2) * (scale_x -1 ),  50 * scale_y  , scale_x , scale_y)) 
floors.add(Floor_Hallway((-300) -  int(OFFSET3) *(scale_x -1), (50 + 195) * scale_y, 400 , 90  , scale_x , scale_y))



#############################



for room_data in level_1data:
    Room_Create(room_data["x"], room_data["y"], room_data["form"], room_data["type"], room_data["enemies_counter"])

last_room_x = level_1data[-2]["x"]
last_room_y = level_1data[-2]["y"]

boss_room_x = last_room_x + 700 + 240 
boss_room_y = last_room_y 

for wall in walls.copy():
    if wall.rect.x in range(last_room_x + 680, last_room_x + 710) and wall.rect.y in range(last_room_y + 180, last_room_y + 220):
        walls.remove(wall)

# Boss hallway and floor cringe generation (I'm tired)
hallway_x = last_room_x + 680
hallway_y = last_room_y + 195 - 30
hallway_width = 320
hallway_height = 135
walls.add(Wall(hallway_x, hallway_y, hallway_width, 20, scale_x, scale_y))
walls.add(Wall(hallway_x, hallway_y + hallway_height - 20, hallway_width, 20, scale_x, scale_y))
floors.add(Floor_Hallway(hallway_x * scale_x, hallway_y * scale_y, hallway_width, hallway_height, scale_x, scale_y))
floors.add(Floor((boss_room_x + 40) * scale_x, (boss_room_y - 110) * scale_y, 900 / ROOM_WIDTH, 700 / ROOM_HEIGHT))


boss_gates = []

gateboss= Gate(boss_room_x + 40, boss_room_y + 185, 20, 100, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)

gateboss.toogle(walls)

walls.add(gateboss)
boss_gates.extend([gateboss])

center_x = boss_room_x + 450
center_y = boss_room_y + 350

walls.add(Wall(center_x - 200, center_y - 100, 50, 50, scale_x, scale_y))

walls.add(Wall(center_x + 200, center_y, 50, 50, scale_x, scale_y))



walls.add(Wall(last_room_x + 680, last_room_y, 20, 190 - last_room_y, scale_x, scale_y))
walls.add(Wall(last_room_x + 680, last_room_y + 310, 20, (500 - 310), scale_x, scale_y))


boss_room_x = last_room_x + (700 + 240)
boss_room_y = last_room_y



for wall in walls:
    if wall.rect.collidepoint(boss_room_x, boss_room_y + 200):
        walls.remove(wall)
        break

boss_spawned = False
boss_room_entered = False
boss = None




enemies = pygame.sprite.Group()
enemies_counter = 0
copy1 = walls.copy()
spawn_delay = 5000 
last_spawn_time = 0

paused = False
running = False
stop = False
drops = pygame.sprite.Group()
running = True  
OFFSET = 700
OFFSETY = (scale_y-1) * 200    
    
# player.rect.center = ( -500 +(1-scale_x) * OFFSET ,50 + ( 700 / 2 )* scale_y - OFFSETY  )  # - move the player to the room 
player.rect.center = (boss_room_x + -10 * scale_x, boss_room_y + 250 * scale_y)






pygame.mouse.set_visible(True)

start_time = pygame.time.get_ticks()  # Record the start time

while running:
    # print(scale_x ,scale_y)
        current_time = pygame.time.get_ticks()  # Record the start time
    #print(enemies_counter)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    pause_menu(scale_x , scale_y)
                elif event.key == pygame.K_e: # Added "E" hotkey to pick up items.
                    for drop in drops:
                        if player.rect.colliderect(drop.rect):
                            FIRE_MODES =  drop.pickup(player , FIRE_MODES )
                if event.key == pygame.K_SPACE:
                    player.dash()
                elif event.key == pygame.K_1:
                     player.is_reloading = False 
                     player.current_mode = 1
                elif event.key == pygame.K_2:
                    player.current_mode = 2
                    player.is_reloading = False 
                elif event.key == pygame.K_3:
                    player.current_mode = 3
                    player.is_reloading = False 
                elif event.key == pygame.K_g:
                    player.current_mode = 4
                    player.is_reloading = False
                elif event.key == pygame.K_r:
                     if player.current_mode != 4:
                         if not player.is_reloading and FIRE_MODES[player.current_mode]["ammo"] > 0 and FIRE_MODES[player.current_mode]["full"] != FIRE_MODES[player.current_mode]["bullets"]:
                                player.is_reloading = True
                                player.reload_start_time = time.time()
                elif event.key == pygame.K_TAB:
                     Restart(Rooms,player, enemies ,drops,scale_x, scale_y, OFFSET, OFFSETY)
                     enemies_counter = 0 
                     FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
                
        if player.is_reloading and FIRE_MODES[player.current_mode]["full"] != FIRE_MODES[player.current_mode]["bullets"]: 
            current_time = time.time()
            reload_duration = FIRE_MODES[player.current_mode]["reload_time"]
            
            if current_time - player.reload_start_time >= reload_duration:
                # Complete reload
                max_reload = FIRE_MODES[player.current_mode]["full"] - FIRE_MODES[player.current_mode]["bullets"]
                reload_amount = min(FIRE_MODES[player.current_mode]["ammo"], max_reload)
                
                FIRE_MODES[player.current_mode]["bullets"] += reload_amount
                FIRE_MODES[player.current_mode]["ammo"] -= reload_amount
                player.is_reloading = False
        for room in Rooms :
            if player.rect.colliderect(room.rect) and room.active == False:
                room.active = True
                #enemies_counter = room.enemies_counter
        #boss room check
        if (boss_room_x + 100 <= player.rect.centerx <= boss_room_x + 900 and
            boss_room_y <= player.rect.centery <= boss_room_y + 700 and
            not boss_spawned):

            boss = Boss(boss_room_x + 450 * scale_x, boss_room_y + 350 * scale_y, player, scale_x, scale_y, drops, current_settings["difficulty"])
            enemies.add(boss)
            boss_spawned = True
            enemies_counter = 5
            if enemies_counter > 0:
                for wall in walls:
                    if isinstance(wall, Gate) and wall.is_open:
                        wall.toogle(walls)













        # Game logic updates
        if boss and boss.health <= 0:
            for gate in boss_gates:
                if not gate.is_open:
                    gate.toogle(walls)

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
                x = random.randint(room.rect.x, room.rect.x  + int(ROOM_WIDTH - 160 * scale_x))
                
                y = random.randint(room.rect.y, room.rect.y  + int(ROOM_HEIGHT - (160)*scale_y))
                enemy = Enemy(x, y,drops,scale_x , scale_y, current_settings ["difficulty"])
                
                if not any(enemy.rect.colliderect(wall.rect) for wall in walls):
                    enemies.add(enemy)
                    enemies_to_spawn -= 1
                

        # Player input and updates
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click
            # Get mouse position in WORLD coordinates
            mouse_world_x = pygame.mouse.get_pos()[0]  - camera.camera.x # i am sceptical about this resolution fix 
            mouse_world_y = pygame.mouse.get_pos()[1] - camera.camera.y
    
            # Calculate direction relative to player's WORLD position
            dx = mouse_world_x - player.rect.centerx 
            dy = mouse_world_y - player.rect.centery 
            dist = max(1, math.sqrt(dx*dx + dy*dy))
            if FIRE_MODES[player.current_mode].get("type") == "grenade":
                if FIRE_MODES[player.current_mode]["ammo"] > 0:
                    FIRE_MODES = player.shoot((dx / dist, dy / dist), FIRE_MODES)
            else:
                if FIRE_MODES[player.current_mode]["bullets"] > 0:
                    FIRE_MODES = player.shoot((dx / dist, dy / dist), FIRE_MODES)
                elif not player.is_reloading and FIRE_MODES[player.current_mode]["ammo"] > 0:
                    player.is_reloading = True
                    player.reload_start_time = time.time()

            
        player.update(walls)    
        camera.update(player)
  
        mouse_world_x = pygame.mouse.get_pos()[0] - camera.camera.x
        mouse_world_y = pygame.mouse.get_pos()[1] - camera.camera.y
        dx = mouse_world_x - player.rect.centerx
        dy = mouse_world_y - player.rect.centery
        player_angle = math.degrees(math.atan2(-dx, -dy)) % 360 + 90
        original_image = player.original_image  # Store the original unrotated image in the Player class
        player.angle = player_angle
        
        rotated_image = pygame.transform.rotate(player.original_image, player_angle)
        rotated_rect = rotated_image.get_rect(center=player.rect.center)

        for tear in player.tears[:]:
            if isinstance(tear, Grenade):
                exploded = tear.update(walls)
                adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
                screen.blit(tear.image, adjusted_pos)

                if exploded:
                    for enemy in enemies:
                        dist = math.hypot(enemy.rect.centerx - tear.rect.centerx,
                                          enemy.rect.centery - tear.rect.centery)
                        if dist <= tear.radius:
                            enemy.take_damage(tear.damage)
                            if enemy.health <= 0:
                                enemies.remove(enemy)
                                kills += 1
                                enemies_counter -= 1

                    dist_to_player = math.hypot(player.rect.centerx - tear.rect.centerx,
                                                player.rect.centery - tear.rect.centery)
                    if dist_to_player <= tear.radius and not player.invincible:
                        player.take_damage(tear.damage)
                    explosions.add(ExplosionEffect(x=tear.rect.centerx, y=tear.rect.centery, radius=tear.radius))

                    player.tears.remove(tear)

            else:
                if tear.update():
                    if tear in player.tears:
                        player.tears.remove(tear)
                else:
                    for enemy in enemies:
                        if tear.rect.colliderect(enemy.rect):
                            enemy.take_damage(FIRE_MODES[player.current_mode]["damage"])
                            if tear in player.tears:
                                player.tears.remove(tear)

                            if enemy.health <= 0:
                                enemies.remove(enemy)
                                kills += 1
                                enemies_counter -= 1
                            break

        
        for floor in floors:
            screen.blit(floor.image, camera.apply(floor))
        for wall in walls:
            screen.blit(wall.image, camera.apply(wall))
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy))        
        screen.blit(rotated_image, rotated_rect.topleft + pygame.math.Vector2(camera.camera.topleft))
        if player.is_dashing and len(player.dash_trail) > 1:
            num_points = len(player.dash_trail)
            
            for i in range(1, num_points):
                alpha = int(255 * (1 - i/num_points))
                # Apply camera offset to trail positions
                start_pos = (player.dash_trail[i-1][0] + camera.camera.x,
                            player.dash_trail[i-1][1] + camera.camera.y)
                end_pos = (player.dash_trail[i][0] + camera.camera.x,
                        player.dash_trail[i][1] + camera.camera.y)
                
                trail_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                pygame.draw.line(trail_surface, (0, 0, 0, alpha), 
                                start_pos, end_pos, 
                                width=int(14 * player.scale_x))
                screen.blit(trail_surface, (0, 0))
        # Calculate the angle to rotate the player image    
        
        # test1 = DestructibleObject(250,250,50,50,23)
        # test1.draw(screen)
        
        for tear in player.tears:
            adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
            screen.blit(tear.image, adjusted_pos)
            
            if player.current_mode == 3 and isinstance(tear, Tear):
                if len(tear.trail_positions) > 1: # Convert positions to screen coordinates
                    trail_points = [
                        (x + camera.camera.x, y + camera.camera.y)
                        for (x, y) in tear.trail_positions
                    ]
                    pygame.draw.lines(screen, (255, 200, 100), False, trail_points, 2)

        for tear in player.tears[:]:
            if isinstance(tear, Grenade):
                exploded = tear.update(walls)
                adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
                screen.blit(tear.image, adjusted_pos)

                if exploded:
                    for enemy in enemies:
                        dist = math.hypot(enemy.rect.centerx - tear.rect.centerx,
                                          enemy.rect.centery - tear.rect.centery)
                        if dist <= tear.radius:
                            enemy.take_damage(tear.damage)
                    player.tears.remove(tear)
            else:
                adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
                screen.blit(tear.image, adjusted_pos)



        if boss and boss.alive():
            for tear in boss.tears:
                adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
                screen.blit(tear.image, adjusted_pos)
                if player.rect.colliderect(tear.rect) and not player.invincible:
                    player.take_damage(tear.damage)
                    if tear in boss.tears:
                        boss.tears.remove(tear)

        # if boss and not boss.alive():
        #     for gate in boss_gates:
        #         if not gate.is_open:
        #             gate.toogle(walls)

        if boss and boss.alive():
            boss.draw_health_bar(screen, scale_x, scale_y)

        enemies.update(player, walls)
        
        for tear in player.tears[:]:
            if isinstance(tear, Grenade):
                exploded = tear.update(walls)
                if exploded and tear in player.tears:
                    player.tears.remove(tear)
            else:
                tear.update()
                for wall in walls:
                    if tear.rect.colliderect(wall.rect):
                        if tear in player.tears:
                            player.tears.remove(tear)
                        break

        for enemy in enemies:
          if player.rect.colliderect(enemy.rect) and not player.invincible:
            player.health -= 1
        for drop in drops:
            screen.blit(drop.image, camera.apply(drop))
        for obj in interactive_objects:
                if hasattr(obj, "draw"):
                    obj.draw(screen)
                else:
                    screen.blit(obj.image, camera.apply(obj))
        
        # Health and UI elements (drawn without camera offset)
        font = pygame.font.SysFont(None, int(36 * scale_x))
        health_text = font.render(f"Hearts: {int(player.health)}", True, WHITE)
        # coordinates  = font.render(f"Player coordinates: X  {int(player.rect.x)} Y  {int(player.rect.y)}", True, WHITE)
        
        draw_health_bar(screen,player.health, player.max_health,scale_x , scale_y)
        #screen.blit(coordinates, (20 * scale_x, 50 * scale_y))
        if player.health <= 1:
            result =   game_over_screen(screen,kills , time , 1  , current_time - start_time)
            if result == "restart":
                Restart(Rooms,player, enemies ,drops,scale_x, scale_y, OFFSET, OFFSETY)
                enemies_counter = 0
                kills = 0
                FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
                start_time = current_time
            elif result == "menu":
                Restart(Rooms,player, enemies ,drops,scale_x, scale_y, OFFSET, OFFSETY)
                enemies_counter = 0
                kills = 0
                start_time = 0
                FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
                Main_menu(SELECTED_WIDTH , SELECTED_HEIGHT)
                pygame.mouse.set_visible(True)
        # Debugging information
        # font_debug = pygame.font.SysFont(None, int(24 * scale_x))  # Smaller font for debugging
        # mouse_world_text = font_debug.render(f"Mouse World: ({int(mouse_world_x)}, {int(mouse_world_y)})", True, WHITE)
        # player_position_text = font_debug.render(f"Player Position: ({int(player.rect.centerx)}, {int(player.rect.centery)})", True, WHITE)
        # direction_text = font_debug.render(f"Direction: ({round(dx, 2)}, {round(dy, 2)})", True, WHITE)
        
        # screen.blit(mouse_world_text, (20 * scale_x, 100 * scale_y))
        # screen.blit(player_position_text, (20 * scale_x, 130 * scale_y))
        # screen.blit(direction_text, (20 * scale_x, 160 * scale_y))
        
        pygame.draw.circle(screen, (192,192,192), (0, 0) , 150 , 0)
        weapon_image = pygame.image.load(FIRE_MODES[player.current_mode]["url"]).convert_alpha()
        weapon_image = pygame.transform.scale(weapon_image, (100 * scale_x, 100 * scale_y))
        
        weapon_rect = weapon_image.get_rect(center=(0, 0))
        if player.is_reloading:
    # Calculate progress
               reload_progress = (time.time() - player.reload_start_time) / FIRE_MODES[player.current_mode]["reload_time"]
               draw_reload_bar(
                    screen=screen,
                    x=130 , # base X position (before scaling)
                    y=37, # base Y position (before scaling)
                    scale_x=scale_x,
                    scale_y=scale_y,
                    reload_progress=min(reload_progress, 1.0)  # ensure never exceeds 1.0
    )
        pygame.draw.circle(screen, (192,192,192), (0, 0) , 150 * scale_x , 0)
        screen.blit(weapon_image, (0, 0))
        font = pygame.font.SysFont(None, int(24 * scale_x))
        if FIRE_MODES[player.current_mode].get("type") == "grenade":
            ammo_text = font.render(f"{FIRE_MODES[player.current_mode]['ammo']}", True, BLACK)
        else:
            ammo_text = font.render(f"{FIRE_MODES[player.current_mode]['bullets']}/{FIRE_MODES[player.current_mode]['ammo']}", True, BLACK)

        ammo_rect = ammo_text.get_rect(center=(0, 0))
        screen.blit(ammo_text, ( 10 * scale_x , 100 * scale_y ) )     
        # boss_room_rect = pygame.Rect(
        #     boss_room_x,
        #     boss_room_y,
        #     900 * scale_x,
        #     700 * scale_y
        # )
        # draw_minimap(screen, player, Rooms, boss_room_rect=pygame.Rect(boss_room_x, boss_room_y, 900 * scale_x, 700 * scale_y))
        draw_minimap(screen, player, Rooms)
        for effect in explosions.copy():
            if effect.update():
                explosions.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
