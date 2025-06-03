import pygame
import random
import math
import os
import time 
import copy 

from portal import Portal
from player import Player, Tear
from enemy import Enemy
from camera import Camera
from room_generation import generate_boss_room, generate_room , Wall ,  Gate , Floor ,Floor_Hallway , Room 
from UI_components import draw_health_bar , Menu_option , DustParticle , draw_reload_bar , draw_minimap , StopButton

import json
import asyncio
import sys 

from collections import deque
from player import Player
from enemy import Enemy
from camera import Camera

from stopmenu import pause_menu , draw_button , draw_slider
from Main_Menu import Main_menu

from interactive_objects import  DestructibleObject , SpikeTrap , ExplosiveBarrel
from game_over import GameOver , game_over_screen ,  Restart

from boss import Boss


from loading_screen import LoadingScreen

from setting_menu import SettingsMenu

from grenade import Grenade, ExplosionEffect
pygame.init()



explosions = pygame.sprite.Group()

interactive_objects = pygame.sprite.Group()
 # wall = DestructibleObject(x=450, y=450, width=32, height=32, hp=100 ,scale_x=1 , scale_y=1)
 # spike = SpikeTrap(x=450, y=500, width=50, height=40, damage=1 , scale_x=1 , scale_y=1)
 # barrel = ExplosiveBarrel(x=1150, y=450, width=32, height=32, hp=50, explosion_radius=640, explosion_damage=50, scale_x=1 , scale_y=1)
 # interactive_objects.add(wall, barrel)
Spikes = pygame.sprite.Group()
 # Spikes.add(spike)


os.environ['SDL_VIDEO_CENTERED'] = "1"
BASE_WIDTH = 800 
BASE_HEIGHT = 600


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



frame_start_time = time.time() * 1000  # milliseconds

PERF_HISTORY_LENGTH = 120  # Keep 2 seconds of data at 60 FPS
frame_times = deque(maxlen=PERF_HISTORY_LENGTH)
perf_update_interval = 250  # Update display every 250ms
last_perf_update = 0
perf_metrics = {
    'current': 0,
    'avg': 0,
    'min': 0,
    'max': 0,
    '1%_low': 0,
    '0.1%_low': 0
}
PERFOMANCE_METRICS = False

        # Just before pygame.display.flip() (around line 830), add this performance tracking:
        # Calculate frame time
frame_time = time.time() * 1000 - frame_start_time

def load_settings():
    try:
        with open("settings.json", "r") as f:
            a = json.load(f)
            a["resolution"] = tuple(a["resolution"])
            return a
    except (FileNotFoundError, json.JSONDecodeError):
        return current_settings  # Fallback if something goes wrong
#print(load_settings())

current_settings = load_settings()
menu_result = Main_menu(SELECTED_WIDTH, SELECTED_HEIGHT, current_settings)
current_settings = menu_result

camera = Camera(screen_width=current_settings["resolution"][0], screen_height=current_settings["resolution"][1], world_width=30000, world_height=30000, scale_x=scale_x, scale_y=scale_y)


scale_x = current_settings["resolution"][0] / BASE_WIDTH
scale_y = current_settings["resolution"][1] / BASE_HEIGHT

player = Player(scale_x, scale_y, current_settings["difficulty"])


def apply_new_settings(player):
    global current_settings, scale_x, scale_y, screen, camera

    current_settings = load_settings()

    scale_x = current_settings["resolution"][0] / BASE_WIDTH
    scale_y = current_settings["resolution"][1] / BASE_HEIGHT

    screen = pygame.display.set_mode(current_settings["resolution"])

    camera = Camera(
        screen_width=current_settings["resolution"][0],
        screen_height=current_settings["resolution"][1],
        world_width=30000,
        world_height=30000,
        scale_x=scale_x,
        scale_y=scale_y
    )
    camera.update(player)


def fade_transition():
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 20):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)





BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

data = [ 0 , (800,600) ]


    
#print(load_settings())
    
    
    
scale_x = current_settings["resolution"][0] / BASE_WIDTH
scale_y = current_settings["resolution"][1] / BASE_HEIGHT

FIRE_MODES = {
            1: {"speed": 7, "damage": 10, "fire_rate": 0.6 ,"url": "images/pistol.png","bullets" : 10 , "ammo" :80  , "full" : 10 , "reload_time" :2 },
            2: {"speed": 12, "damage": 70, "fire_rate": 0.2 , "url": "images/shotgun.png" , "bullets" : 3000 , "ammo" : 30 , "full": 30 , "reload_time" :1.5 }, 
            3: {"speed": 20, "damage": 30, "fire_rate": 1 , "url": "images/sniper.png" , "bullets" : 10 ,   "ammo" : 5, "full":10 , "reload_time" : 2.5 },
            4: {"type": "grenade", "speed": 15, "damage": 100, "radius": 200, "fire_rate": 1.2, "url": "images/grenade.png", "bullets": None, "ammo": 3, "full": None, "reload_time": 0}
        }
FIRE_MODES_COPY = copy.deepcopy(FIRE_MODES)

ROOM_WIDTH, ROOM_HEIGHT = 700 * scale_x, 500 * scale_y
CELL_SIZE = 40





level_1data = [
    {"x": 50, "y": 50, "form": 8, "type": 1, "enemies_counter": 0},
    {"x": 700 + 50 + 240 + 100, "y": 50, "form": 9, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 50, "form": 3, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 50 - (500 + 260), "form": 8, "type": 1, "enemies_counter": 6},
    {"x": 50 + (700 + 240 + 100) * 2, "y": -50 + 500 + 260, "form": 10, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100) * 3, "y": 50 - (500 + 260), "form": 9, "type": 1, "enemies_counter": 4},
    {"x": 50 + (700 + 240 + 100) * 4, "y": 50 - (500 + 260), "form": 6, "type": 1, "enemies_counter": 5},
    {"x": 50, "y": 500 + 50 + 260, "form": 5, "type": 1, "enemies_counter": 4},
    {"x": 50, "y": 30 + (500 + 260) * 2, "form": 11, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100), "y": 30 + (500 + 260) * 2, "form": 2, "type": 1, "enemies_counter": 4},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 30 + (500 + 260) * 2, "form": 6, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100), "y": 10 + (500 + 260) * 4, "form": 11, "type": 1, "enemies_counter": 4},
    {"x": 50 + (700 + 240 + 100), "y": 30 + (500 + 260) * 3, "form": 5, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 10 + (500 + 260) * 4, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 3, "y": 10 + (500 + 260) * 4, "form": 9, "type": 1, "enemies_counter": 4},
    {"x": 50 + (700 + 240 + 100) * 4, "y": 10 + (500 + 260) * 4, "form": 9, "type": 1, "enemies_counter": 6},
    {"x": (50 + (700 + 240 + 100) * 5) - 180, "y": (10 + (500 + 260) * 4) - 110, "form": "boss", "type": 1, "enemies_counter": 0}
]


level_2data = [
    {"x": 50, "y": 50, "form": 7, "type": 1, "enemies_counter": 0},
    {"x": 50 + (700 + 240 + 100), "y": 50, "form": 2, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100) * 2 , "y": 50, "form": 9, "type": 1, "enemies_counter": 7},
    {"x": 50 + (700 + 240 + 100) * 3,  "y": 50, "form": 2, "type": 1, "enemies_counter": 6},
    {"x": 50 + (700 + 240 + 100) * 4 , "y": 50, "form": 6, "type": 1, "enemies_counter": 4},
    {"x": 50 + (700 + 240 + 100) * 3 , "y": 50 + (500+240), "form": 11, "type": 1, "enemies_counter": 7},
    {"x": 50 + (700 + 240 + 100) * 4 , "y": 50 + (500+240), "form": 4, "type": 1, "enemies_counter": 6},
    {"x": 50 + (700 + 240 + 100) * 4,  "y": 50 + (500+240) * 2 , "form": 10, "type": 1, "enemies_counter": 7},
    
    {"x": 50 + (700 + 240 + 100) , "y": 50+(500 + 240), "form": 5, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100) , "y": 50+(500 + 240) * 2, "form": 5, "type": 1, "enemies_counter": 4},
    {"x": 50 + (700 + 240 + 100), "y": 50+(500 + 240) * 3, "form": 11, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 50+(500 + 240) * 3, "form": 2, "type": 1, "enemies_counter": 3},
    
    {"x": 50 + (700 + 240 + 100) * 3 ,"y": 50+(500 + 240) * 3, "form": 6, "type": 1, "enemies_counter": 5},
    {"x": 50 + (700 + 240 + 100) * 2, "y": 50+(500 + 240) * 4, "form": 11, "type": 1, "enemies_counter": 7},
    {"x": 50 + (700 + 240 + 100) * 3, "y": 50+(500 + 240) * 4, "form": 9, "type": 1, "enemies_counter": 3},
    {"x": 50 + (700 + 240 + 100) * 4, "y": 50+(500 + 240) * 4, "form": 6, "type": 1, "enemies_counter": 4},
]

enemy_projectiles = pygame.sprite.Group()
portals = pygame.sprite.Group()
Rooms = pygame.sprite.Group()
floors = pygame.sprite.Group()
kills = 0




# technical debt
def Room_Create(x, y, form, type, enemies_counter):
    if form == "boss":
        global boss_center, boss_gates
        boss_walls, boss_floors, boss_center, gate = generate_boss_room(int(x), int(y), scale_x, scale_y)
        globals()['boss_center'] = boss_center
        walls.add(boss_walls)
        floors.add(boss_floors)
        boss_gates.append(gate)
    else:
        room_walls = generate_room(int(x), int(y), form, type, scale_x, scale_y)
        floors.add(Floor(x * scale_x, y * scale_y, scale_x, scale_y))
        walls.add(room_walls)
        

    Rooms.add(Room(x * scale_x, (y + 50) * scale_y, enemies_counter, scale_x, scale_y))

    if form == 1 or form == 2 or form ==9 or form == 8 or form == 11 or form ==7 :   # right corridor  
         floors.add(Floor_Hallway((x + 677) * scale_x , (y + 195)* scale_y , 300  , 90  ,scale_x,scale_y))
    if form == 1 or form == 2 or form == 3 or form == 4 or form == 5 or form ==8 : # bottom corridor 
        floors.add(Floor_Hallway( (x + 250)*scale_x , (y + 480)*scale_y , 210  , 260 , scale_x ,  scale_y ))
    if form ==1 or form == 2 or form == 3 or form == 4 or form ==6 or form == 9  : # left corrior 
        floors.add(Floor_Hallway( (x  - 300) * scale_x , (y + 195)*scale_y , 300  ,  90  , scale_x , scale_y))	
    if form == 1 or form == 3  or form == 5  : # top corridor , 
        floors.add(Floor_Hallway( (x + 250) *  scale_x , (y -  230)* scale_y   , 210 , 255  ,scale_x ,scale_y ))

    return 0

  

# player = Player (scale_x,scale_y , current_settings["difficulty"])  

walls = pygame.sprite.Group()
boss_gates = [] 


# alternative loading screen
# for room_data in level_1data:
#     loading_screen = LoadingScreen(screen, len(level_1data))
#
#     Room_Create(room_data["x"], room_data["y"], room_data["form"], room_data["type"], room_data["enemies_counter"])
#
#
#     loading_screen.update(1)
#     loading_screen.draw()
#     pygame.display.flip()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
    


async def loader(progress, loading_screen):
    total = len(level_1data)
    for i, room_data in enumerate(level_1data, start=1):
        Room_Create(
            room_data["x"],
            room_data["y"],
            room_data["form"],
            room_data["type"],
            room_data["enemies_counter"],
        )
        progress['loaded'] = i
        
        loading_screen.update()
        
        loading_screen.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        await asyncio.sleep(0)  # Yield control to the event loop

    progress['done'] = True

async def main():
    loading_screen = LoadingScreen(screen, len(level_1data))
    progress = {'loaded': 0, 'total': len(level_1data), 'done': False}
    
    # Initial draw of 0% progress
    loading_screen.draw()
    
    await loader(progress, loading_screen)
    
    # Final draw of 100% progress
    loading_screen.update(len(level_1data))
    loading_screen.draw()
    await asyncio.sleep(0.5)  

async def load_next_level(screen, player, scale_x, scale_y, new_level_data):
    def save_player_state(player, filename="save.json"):
        data = {
            "health": player.health,
            "max_health": player.max_health,
            "position": player.rect.center,
            "current_mode": player.current_mode,
            "fire_modes": {}
        }

        for k in player.fire_modes:
            mode = player.fire_modes[k]
            data["fire_modes"][str(k)] = {
                "bullets": mode.get("bullets"),
                "ammo": mode.get("ammo"),
                "full": mode.get("full")
            }

        with open(filename, "w") as f:
            json.dump(data, f)

    def saved_screen(screen, scale_x, scale_y):
        font = pygame.font.SysFont("Bauhaus 93", int(60 * scale_x))
        message = font.render("Game has been saved.", True, (255, 255, 255))
        screen_width, screen_height = screen.get_size()
        button_width = 300 * scale_x
        button_height = 60 * scale_y
        center_x = (screen_width - button_width) / 2

        options = [
            Menu_option(center_x, 300 * scale_y, button_width, button_height, (255, 255, 255), (0, 200, 0), "Continue"),
            Menu_option(center_x, 400 * scale_y, button_width, button_height, (255, 255, 255), (200, 0, 0), "Quit")
        ]
        active = 0
        options[active].toogle()

        clock = pygame.time.Clock()
        while True:
            screen.fill((0, 0, 0))
            screen.blit(message, ((screen_width - message.get_width()) // 2, 150 * scale_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        active = (active - 1) % len(options)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        active = (active + 1) % len(options)
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        return "continue" if active == 0 else "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, option in enumerate(options):
                        if option.rect.collidepoint(pygame.mouse.get_pos()):
                            return "continue" if i == 0 else "quit"

            for i, option in enumerate(options):
                if i == active and not option.active:
                    option.toogle()
                elif i != active and option.active:
                    option.toogle()

                option.update(option.rect.x, option.rect.y, screen)

            pygame.display.flip()
            clock.tick(60)

    # Show save screen first
    action = saved_screen(screen, scale_x, scale_y)
    if action == "quit":
        player.fire_modes = copy.deepcopy(FIRE_MODES)
        save_player_state(player)
        with open("has_save.flag", "w") as f:
            f.write("1")
        pygame.quit()
        exit()

    # Load save after confirming "continue"
    try:
        with open("save.json", "r") as f:
            save = json.load(f)
            print("Save loaded:", save)
    except Exception as e:
        print("Failed to load save:", e)
        save = None
    # Clear all game state
    walls.empty()
    floors.empty()
    Rooms.empty()
    enemies.empty()
    interactive_objects.empty()
    portals.empty()
    drops.empty()
    player.tears.clear()

    # Apply save data to player
    if save:
        for k_str, mode_data in save.get("fire_modes", {}).items():
            k = int(k_str)
            if k in FIRE_MODES:
                FIRE_MODES[k].update(mode_data)
        global FIRE_MODES_COPY
        FIRE_MODES_COPY = copy.deepcopy(FIRE_MODES)

        player.fire_modes = copy.deepcopy(FIRE_MODES)
        player.health = save.get("health", player.health)
        player.max_health = save.get("max_health", player.max_health)
        player.current_mode = save.get("current_mode", 1)

    first_room = new_level_data[0]
    player.rect.topleft = (first_room["x"] * scale_x + 50 * scale_x, first_room["y"] * scale_y + 50 * scale_y)

    # Show loading screen and build map
    loading_screen = LoadingScreen(screen, len(new_level_data))
    progress = {'loaded': 0, 'total': len(new_level_data), 'done': False}
    loading_screen.draw()
    await asyncio.sleep(0.5)

    for i, room_data in enumerate(new_level_data, start=1):
        Room_Create(
            room_data["x"],
            room_data["y"],
            room_data["form"],
            room_data["type"],
            room_data["enemies_counter"]
        )
        progress['loaded'] = i
        loading_screen.update()
        loading_screen.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        await asyncio.sleep(0)

    # first_room = new_level_data[0]
    # player.rect.center = (first_room["x"] * scale_x + 50 * scale_x, first_room["y"] * scale_y + 50 * scale_y)
    progress['done'] = True
    await asyncio.sleep(0.5)
    player.fire_modes = copy.deepcopy(FIRE_MODES)
    save_player_state(player)


    



boss_room_x = level_1data[-1]["x"]
boss_room_y = level_1data[-1]["y"]

scaled_x = boss_room_x * scale_x
scaled_y = boss_room_y * scale_y

for wall in walls.copy():
    if isinstance(wall, Wall):
        is_left_wall = abs(wall.rect.left - int(boss_room_x * scale_x)) < 5
        is_boss_wall_height = wall.rect.height >= int(500 * scale_y)

        if is_left_wall and is_boss_wall_height:
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




# player.rect.center = (150 * scale_x ,  150 * scale_y) # - move the player to the room 

def rerender (data,walls,floors,Rooms,enemies,drops,interactive_objects,player):
    walls.empty()
    floors.empty()
    Rooms.empty()
    enemies.empty()
    interactive_objects.empty()
    player.tears.clear()
    drops.empty()
    portals.empty()
    enemies_counter = 0
    for room_data in data :
        Room_Create(room_data["x"], room_data["y"], room_data["form"], room_data["type"], room_data["enemies_counter"])




cursor = pygame.image.load("images/cursor.png").convert_alpha()
cursor = pygame.transform.scale(cursor, (50 * scale_x, 50 * scale_y))
pygame.mouse.set_visible(True)

start_time = pygame.time.get_ticks()  # Record the start time
show_save_screen = False



if isinstance(menu_result, dict) and menu_result.get("load_save"):
    try:
        with open("save.json", "r") as f:
            save = json.load(f)
    except Exception as e:
        print("ERR loadnig json", e)
        save = None

    current_settings = {k: v for k, v in menu_result.items() if k not in ("load_save", "level")}

    if save and "fire_modes" in save:
        for k_str, mode_data in save["fire_modes"].items():
            k = int(k_str)
            if k in FIRE_MODES:
                FIRE_MODES[k].update(mode_data)

    player = Player(scale_x, scale_y, current_settings["difficulty"])
    player.fire_modes = copy.deepcopy(FIRE_MODES)

    player.health = save.get("health", player.health)
    player.max_health = save.get("max_health", player.max_health)
    player.current_mode = save.get("current_mode", 1)
    first_room = level_2data[0] if menu_result.get("level") == 2 else level_1data[0]
    player.rect.topleft = (first_room["x"] * scale_x + 50 * scale_x, first_room["y"] * scale_y + 50 * scale_y)
    FIRE_MODES_COPY = copy.deepcopy(FIRE_MODES)

    if menu_result.get("level") == 2:
        rerender(level_2data, walls, floors, Rooms, enemies, drops, interactive_objects, player)
    else:
        rerender(level_1data, walls, floors, Rooms, enemies, drops, interactive_objects, player)




elif isinstance(menu_result, str) and menu_result == "new_game": # New Game
    current_settings = load_settings()
    player = Player(scale_x, scale_y, current_settings["difficulty"])
    player.fire_modes = FIRE_MODES 
    FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
    first_room = level_1data[0]
    player.rect.center = (first_room["x"] * scale_x + 50 * scale_x, first_room["y"] * scale_y + 50 * scale_y)
    asyncio.run(main())
    fade_transition()
    apply_new_settings(player)

elif isinstance(menu_result, dict):
    current_settings = menu_result
    asyncio.run(main())

player.rect.center =( 150 * scale_x , 150 * scale_y)
player.rect.center  = (boss_room_x * scale_x + 50 * scale_x, boss_room_y * scale_y + 50 * scale_y)  
while running:
    # print(scale_x ,scale_y)
        current_time = pygame.time.get_ticks()  # Record the start time
    #print(enemies_counter)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("save.json", "w") as f:
                    f.write("")
                running = False

                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    current_settings = load_settings()

                    window_width, window_height = screen.get_size()
                    # scale_x = window_width / 800
                    # scale_y = window_height / 600
                    current_settings = load_settings()

                    pause_menu(screen, current_settings)

                    fade_transition()
                    apply_new_settings(player)
                    for enemy in enemies:
                        if hasattr(enemy, 'rescale'):
                             enemy.rescale(scale_x, scale_y)
                elif event.key == pygame.K_e: # Added "E" hotkey to pick up items.
                    for drop in drops:
                        if player.rect.colliderect(drop.rect):
                            FIRE_MODES =  drop.pickup(player , FIRE_MODES )
                    for portal in portals: # Portal "E" event
                        if player.rect.colliderect(portal.rect) and not portal.used:
                            enemies_counter = 0
                            portal.used = True
                            asyncio.run(load_next_level(screen, player, scale_x, scale_y, level_2data))
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
                     Restart(Rooms,player, enemies ,drops,scale_x, scale_y )
                     enemies_counter = 0 
                     FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
                elif event.key == pygame.K_q:
                    rerender(level_2data,walls,floors,Rooms,enemies,drops,interactive_objects,player)
                    player.rect.center =( 150 * scale_x , 150 * scale_y)
                    enemies_counter = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                 if event.button == 1:
                     if Stopbutton.rect.collidepoint(event.pos):
                         paused = True
                         pause_menu(screen ,  current_settings)

                
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
        trigger_margin_x = 150 * scale_x
        trigger_margin_y = 50 * scale_y

        trigger_x_start = boss_room_x * scale_x + trigger_margin_x
        trigger_x_end = boss_room_x * scale_x + (900 - trigger_margin_x) * scale_x

        trigger_y_start = boss_room_y * scale_y + trigger_margin_y
        trigger_y_end = boss_room_y * scale_y + (700 - trigger_margin_y) * scale_y

        if (trigger_x_start <= player.rect.centerx <= trigger_x_end and
            trigger_y_start <= player.rect.centery <= trigger_y_end and
            not boss_spawned and 'boss_center' in globals()):




            boss = Boss(boss_center[0], boss_center[1], player, scale_x, scale_y, drops, current_settings["difficulty"])
            enemies.add(boss)
            boss_spawned = True
            enemies_counter = 5

            for gate in boss_gates:
                if gate.is_open:
                    gate.toogle(walls)












        # Game logic updates
        if boss and boss.health <= 0:
            for gate in boss_gates:
                if not gate.is_open:
                    gate.toogle(walls)

            if len(portals) == 0:
                new_portal = Portal(boss.rect.centerx, boss.rect.centery, scale_x, scale_y)
                portals.add(new_portal)

        if enemies_counter > 0:
            for wall in walls:
                if isinstance(wall, Gate) and wall.is_open:
                    wall.toogle(walls)
        
        if enemies_counter <= 0: 
            for wall in walls:
                if isinstance(wall, Gate) and not wall.is_open:
                    wall.toogle(walls)
                   
                
        #print("Enemies counter:", enemies_counter)
        for room in Rooms :
          if  room.active == True  and enemies_counter <= 0 and room.clear == False :
            enemies_counter = room.enemies_counter
            enemies_to_spawn = enemies_counter
            last_spawn_time = pygame.time.get_ticks()
            room.clear = True 
            enemies_to_spawn = room.enemies_counter

            while enemies_to_spawn > 0:
                x = random.randint(room.rect.x + 50, room.rect.x + int(ROOM_WIDTH - 150 * scale_x))
                y = random.randint(room.rect.y + 50, room.rect.y + int(ROOM_HEIGHT - 150 * scale_y))

                enemy_type = random.choice(["ranged", "sniper", "melee"])
                enemy = Enemy(x, y, drops, scale_x, scale_y, current_settings["difficulty"], type=enemy_type)

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

            

    # Calculate direction relative to player's WORLD position
    #      dx = mouse_world_x - player.rect.centerx 
    #      dy = mouse_world_y - player.rect.centery 
    #      dist = max(1, math.sqrt(dx*dx + dy*dy))
    #      if FIRE_MODES[player.current_mode]["bullets"] > 0:
    #        FIRE_MODES = player.shoot((dx/dist, dy/dist), FIRE_MODES)
    #        
    #        #print(FIRE_MODES[player.current_mode]["bullets"])
    #      elif not player.is_reloading and FIRE_MODES[player.current_mode]["ammo"] > 0:
    #                        player.is_reloading = True
    #                        player.reload_start_time = time.time()
    #    if mouse_buttons[0] and Stopbutton.rect.collidepoint(pygame.mouse.get_pos()):
    #        stop = True
    #        pause_menu(scale_x, scale_y, current_settings)
        
        

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
        rotated_rect = rotated_image.get_rect(center=camera.apply(player).center)

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
        for spike in Spikes :
            print(spike.rect.x , spike.rect.y)
            screen.blit(spike.image, camera.apply(spike))
            if player.rect.colliderect(spike.rect) and not player.invincible:
                player.health -= spike.damage
                spike.apply_damage(player)    
        
        screen.blit(rotated_image, rotated_rect.topleft)
        
        
        
        
        for enemy in enemies:
        
            # Check if cooldown has passed
            current_time = pygame.time.get_ticks()

            if isinstance(enemy, Enemy) and enemy.type in ("ranged", "sniper"):
                if current_time - enemy.last_shot_time >= enemy.shoot_cooldown:
                    enemy.can_shoot = True

                if enemy.can_shoot:
                    tear = enemy.shoot(player)
                    if tear:
                        enemy_projectiles.add(tear)
                    enemy.can_shoot = False
                    enemy.last_shot_time = current_time

        #     # Update enemy projectiles
        #     for tear in enemy.tears[:]:
        #         if tear.update(walls) :
        #             enemy.tears.remove(tear)
        #         elif tear.rect.colliderect(player.rect):
        #             player.health -= 1
        #             enemy.tears.remove(tear)
        # for enemy in enemies:
        #     for tear in enemy.tears[:]:
        #         if tear.update(walls):
        #             enemy.tears.remove(tear)
        #         else:
        #             for wall in walls:
        #                 if tear.rect.colliderect(wall.rect):
        #                     enemy.tears.remove(tear)
        #                     break
        # for enemy in enemies:
        #     for tear in enemy.tears[:]:
        #         screen.blit(tear.image, camera.apply(tear))
        for tear in enemy_projectiles:
            screen.blit(tear.image, camera.apply(tear))


        for tear in enemy_projectiles.copy(): 
            if tear.update(walls):
                enemy_projectiles.remove(tear)
            elif tear.rect.colliderect(player.rect):
                player.take_damage(tear.damage)
                enemy_projectiles.remove(tear)
                
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
            for tear in boss.tears.copy():
                adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
                screen.blit(tear.image, adjusted_pos)

                if player.rect.colliderect(tear.rect) and not player.invincible:
                    player.take_damage(tear.damage)
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


     #               pygame.draw.lines(screen, (255, 200, 100), False, trail_points, 2)  
     #   
     #   for tear in player.tears[:]:
     #       tear.update()
     #       for wall in walls:
     #           if tear.rect.colliderect(wall.rect):
     #               if  isinstance(wall , ExplosiveBarrel):
     #                   enemies_counter =  wall.take_damage(FIRE_MODES[player.current_mode]["damage"] , enemies , player,interactive_objects,enemies_counter)
                        
                        
     #               elif isinstance(wall, DestructibleObject):
     #                   wall.take_damage(FIRE_MODES[player.current_mode]["damage"])
     #               
     #               player.tears.remove(tear)
     #               break
        

        for enemy in enemies:
          if player.rect.colliderect(enemy.rect) and not player.invincible:
            player.health -= 1
        for drop in drops:
            screen.blit(drop.image, camera.apply(drop))
        for portal in portals:
            screen.blit(portal.image, camera.apply(portal))
        enemies.update(player, walls)
       
        for obj in interactive_objects:
             walls.add(obj)
             screen.blit(obj.image, camera.apply(obj))
       

        
        # Health and UI elements (drawn without camera offset)
        font = pygame.font.SysFont(None, int(36 * scale_x))
        health_text = font.render(f"Hearts: {int(player.health)}", True, WHITE)
        # coordinates  = font.render(f"Player coordinates: X  {int(player.rect.x)} Y  {int(player.rect.y)}", True, WHITE)
        
        draw_health_bar(screen,player.health, player.max_health,scale_x , scale_y)
        #screen.blit(coordinates, (20 * scale_x, 50 * scale_y))
        if player.health <= 1:
            result =   game_over_screen(screen, kills , time , 1  , current_time - start_time)
            if result == "restart":
                with open("save.json", "w") as f: # To erase save file
                    f.write("")

                Restart(Rooms,player, enemies ,drops,scale_x, scale_y)
                enemies_counter = 0
                kills = 0
                FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
                boss_spawned = False
                start_time = current_time
            elif result == "menu":
                Restart(Rooms,player, enemies ,drops,scale_x, scale_y)
                enemies_counter = 0
                boss_spawned = False
                kills = 0
                start_time = 0
                FIRE_MODES = copy.deepcopy(FIRE_MODES_COPY)
             
                current_settings = Main_menu(SELECTED_WIDTH , SELECTED_HEIGHT , current_settings)
              
                scale_x = current_settings["resolution"][0] / BASE_WIDTH
                scale_y = current_settings["resolution"][1] / BASE_HEIGHT
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

        # screen.blit(ammo_text, ( 10 * scale_x , 100 * scale_y ) )     
        # boss_room_rect = pygame.Rect(
        #     boss_room_x,
        #     boss_room_y,
        #     900 * scale_x,
        #     700 * scale_y
        # )
        # draw_minimap(screen, player, Rooms, boss_room_rect=pygame.Rect(boss_room_x, boss_room_y, 900 * scale_x, 700 * scale_y))
        draw_minimap(screen, player, Rooms, scale_x=scale_x, scale_y=scale_y)
        for effect in explosions.copy():
            if effect.update():
                explosions.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect))


        screen.blit(ammo_text, ( 10 * scale_x , 100 * scale_y ) )   
        
        Stopbutton = StopButton(screen, current_settings["resolution"][0] - 100*scale_x - 2, 2, 100 * scale_x, 50 * scale_y)
        Stopbutton.draw(screen)
             
        cursor_rect = cursor.get_rect(center=(mouse_world_x + camera.camera.x, mouse_world_y + camera.camera.y))
        screen.blit(cursor, cursor_rect.topleft)
        
        
        frame_time = clock.get_time()  # Time since last tick in milliseconds
        time_text = font.render(f"Frame time: {frame_time}ms", True, (255, 255, 255))
        screen.blit(time_text, (20 * scale_x, 20 * scale_y))
        
        if PERFOMANCE_METRICS:      
            # In your main game loop (around line 350), add this at the start:
        
            frame_times.append(frame_time)

            # Update metrics display periodically
            current_time = pygame.time.get_ticks()
            if current_time - last_perf_update > perf_update_interval:
                if frame_times:
                    sorted_times = sorted(frame_times)
                    perf_metrics = {
                        'current': frame_time,
                        'avg': sum(frame_times) / len(frame_times),
                        'min': min(frame_times),
                        'max': max(frame_times),
                        '1%_low': sorted_times[int(len(sorted_times) * 0.01)],
                        '0.1%_low': sorted_times[int(len(sorted_times) * 0.001)]
                    }
                last_perf_update = current_time
        
            # Render the performance metrics (add this where you want it displayed, perhaps near other UI)
            perf_font = pygame.font.SysFont(None, int(20 * scale_x))
            y_offset = 60 * scale_y
            for name, value in perf_metrics.items():
                if name in ['1%_low', '0.1%_low']:
                    text = perf_font.render(f"{name}: {value:.1f}ms (worst {name.split('_')[0]})", True, 
                                        RED if value > 33.3 else GREEN)
                else:
                    text = perf_font.render(f"{name}: {value:.1f}ms", True, 
                                        RED if value > 16.6 and name != 'max' else GREEN)
                screen.blit(text, (20 * scale_x, y_offset))
                y_offset += 20 * scale_y

            # Add a frame time graph visualization (optional but helpful)
            graph_width = 200 * scale_x
            graph_height = 60 * scale_y
            graph_surface = pygame.Surface((graph_width, graph_height), pygame.SRCALPHA)
            max_frame_time = max(50, max(frame_times) if frame_times else 50 )

            for i, ft in enumerate(frame_times):
                x = i * (graph_width / PERF_HISTORY_LENGTH)
                height = min(graph_height, (ft / max_frame_time) * graph_height)
                color = (255, 0, 0, 150) if ft > 16.6 else (0, 255, 0, 150)
                pygame.draw.line(graph_surface, color, (x, graph_height), (x, graph_height - height), 2)

            # Draw threshold lines
            pygame.draw.line(graph_surface, (255, 255, 0, 100), (0, graph_height * (16.6/max_frame_time)), 
                            (graph_width, graph_height * (16.6/max_frame_time)), 1)
            pygame.draw.line(graph_surface, (255, 0, 0, 100), (0, graph_height * (33.3/max_frame_time)), 
                            (graph_width, graph_height * (33.3/max_frame_time)), 1)

            screen.blit(graph_surface, (20 * scale_x, y_offset + 10 * scale_y))

            # Add explanatory text
            legend_font = pygame.font.SysFont(None, int(16 * scale_x))
            screen.blit(legend_font.render("Yellow: 60FPS (16.6ms)", True, (255, 255, 0)), 
                    (25 * scale_x, y_offset + graph_height + 15 * scale_y))
            screen.blit(legend_font.render("Red: 30FPS (33.3ms)", True, (255, 0, 0)), 
                    (25 * scale_x, y_offset + graph_height + 30 * scale_y))
        
        pygame.mouse.set_visible(False)     

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
