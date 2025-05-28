import pygame
import random
from UI_components import Menu_option 
from UI_components import DustParticle
import os 
from setting_menu import SettingsMenu
import json 
from player import Player

pygame.init()

def Main_menu (actual_screen_width = 1300, actual_screen_height = 800 , settings_data =  None  ):
   
    
    os.environ['SDL_VIDEO_CENTERED'] = "1"
    
    default_settings = {
        'resolution': (800, 600),
        'music_volume': 50,
        'sfx_volume': 50,
        'difficulty': 'medium'
    }
    
    current_settings = settings_data if settings_data else default_settings
   
    pygame.mixer.init()
    pygame.mixer.music.load("sound/music.mp3")  # Relative path
   
    screen_width = 800 
    screen_height = 600
    
    
    
    scale_x = current_settings['resolution'][0] / screen_width
    scale_y = current_settings['resolution'][1]/ screen_height
    


    screen = pygame.display.set_mode((800 * scale_x, 600 * scale_y))
    clock = pygame.time.Clock()
    
    
    
    Main_Menu = True 
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)

    continue_available = os.path.exists("has_save.flag")

    Option_continue = Menu_option(80 * scale_x, (230 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Continue")
    Option_play = Menu_option(80 * scale_x, (300 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Play")
    Option_settings = Menu_option(80 * scale_x, (370 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Settings")
    Option_exit = Menu_option(80 * scale_x, (440 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Exit")

    Options = [Option_play, Option_settings, Option_exit]
    if continue_available:
        Options.insert(0, Option_continue)

        
    background = pygame.image.load('images/Background1.png').convert_alpha()
    background = pygame.transform.scale(background,( screen_width * scale_x,screen_height * scale_y))

    # Option1 = Menu_option(80 * scale_x, (300 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Play")
    # Option2 = Menu_option(80 * scale_x, (370 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Settings")
    # Option3 = Menu_option(80 * scale_x, (440 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Exit")

    # Options = [Option1, Option2, Option3]
    active = 0
    Options[active].toogle()
    dust_particles = []
    def draw_arrow(screen, x, y ,text = ">>" , color = WHITE):
        font = pygame.font.SysFont("Bauhaus 93", int(42 ))  # Adjust font size as needed
        arrow_surface = font.render(text, True, color)
        screen.blit(arrow_surface, ( (x - 30) ,( y - 27) ))

    blink_interval = 500  # Time in milliseconds for each blink (on/off)
    last_blink_time = 0   # Track the last time the arrow blinked
    arrow_visible = True 
    pygame.mixer.music.play(-1)  # Loop forever
    while Main_Menu :
        screen.blit(background, (0, 0)) 
        current_time = pygame.time.get_ticks()
        pygame.mixer.music.set_volume(current_settings["music_volume"]/100) # volume: 0.0 (mute) to 1.0 (full)
        
    

        # Handle blinking logic
        if current_time - last_blink_time > blink_interval:
            arrow_visible = not arrow_visible  # Toggle visibility
            last_blink_time = current_time     # Reset the timer

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    Main_Menu = False
                    pygame.mixer.music.stop()
                    pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if continue_available:
                    if active == 0:  # Continue
                        try:
                            with open("save.json", "r") as f:
                                save = json.load(f)
                            os.remove("has_save.flag")
                            pygame.mixer.music.stop()
                            return {"load_save": save, "level": 2, **current_settings}
                        except FileNotFoundError:
                            continue_available = False
                            continue

                    elif active == 1:  # Play
                        pygame.mixer.music.stop()
                        return "new_game"


                    elif active == 2:  # Settings
                        pygame.mixer.music.stop()
                        settings_menu = SettingsMenu(actual_screen_width, actual_screen_height, current_settings)
                        settings_menu.update()
                        new_settings = settings_menu.run(screen, Main_menu)
                        if new_settings:
                            current_settings.update(new_settings)
                            with open("settings.json", "w") as f:
                                json.dump(current_settings, f)
                            return Main_menu(
                                new_settings['resolution'][0],
                                new_settings['resolution'][1],
                                settings_data=current_settings
                            )

                    elif active == 3:  # Exit
                        pygame.quit()
                        exit()

                else:  # no Continue button
                    if active == 0:  # Play
                        pygame.mixer.music.stop()
                        return "new_game"

                    elif active == 1:  # Settings
                        pygame.mixer.music.stop()
                        settings_menu = SettingsMenu(actual_screen_width, actual_screen_height, current_settings)
                        settings_menu.update()
                        new_settings = settings_menu.run(screen, Main_menu)
                        if new_settings:
                            current_settings.update(new_settings)
                            with open("settings.json", "w") as f:
                                json.dump(current_settings, f)
                            return Main_menu(
                                new_settings['resolution'][0],
                                new_settings['resolution'][1],
                                settings_data=current_settings
                            )

                    elif active == 2:  # Exit
                        pygame.quit()
                        exit()

            keys = pygame.key.get_pressed()
            previous_active = active
            if keys[pygame.K_LEFT]:
                active -= 1
            if keys[pygame.K_RIGHT]: 
                active += 1
            if keys[pygame.K_UP]: 
                active -= 1
            if keys[pygame.K_DOWN]:
                active += 1        
                
        if random.random() < 0.75:  # adjust spawn rate
            x = random.randint(int(0* scale_x),int(800 * scale_x))
            y = random.randint(int(400 * scale_y), int (600 * scale_y))  # near bottom
            dust_particles.append(DustParticle(x, y))



        for particle in dust_particles:
            particle.update()
            particle.draw(screen)

        # Remove dead particles
        dust_particles = [p for p in dust_particles if not p.is_dead()]
            
    
        if active < 0: 
            active = len(Options) - 1
        if active >= len(Options): 
            active = 0

        for option in range(len(Options)):
            if option != active and Options[option].active == True   :
                Options[option].toogle()
            if option == active and Options[option].active == False :
                Options[option].toogle()
    
        title_font = pygame.font.SysFont("Bauhaus 93", int(72* scale_x))
    
        tittle = title_font.render(" Bullet  ", RED, WHITE)
        tittle_shadow = title_font.render(" Bullet  ", RED, WHITE)
        tittle_shadow.set_alpha(40,40)
        
        tittle2 = title_font.render("  Born ", RED, BLACK)
        tittle2_shadow = title_font.render("  Born ", RED, BLACK)
        tittle2_shadow.set_alpha(40,40)
    
        
        
        screen.blit(tittle_shadow, ((240) * scale_x, (50 + 10) * scale_y))
        screen.blit(tittle, ((240) * scale_x, 50 * scale_y))
        
        screen.blit(tittle2, ((450) * scale_x, 50 * scale_y))
        screen.blit(tittle2_shadow, ((450) * scale_x, (50 + 10) * scale_y))
        
        for i, option in enumerate(Options):
            y_offset = (230 + i * 70 - 100) * scale_y
            option.update(80 * scale_x, y_offset, screen)

        
        arrow_x = 60 * scale_x # X position of the arrow
        if arrow_visible:
            arrow_y = (230 + active * 70 - 75) * scale_y
            draw_arrow(screen, arrow_x, arrow_y)

        
        
            
        pygame.display.flip()
        clock.tick(60)
        pygame.mouse.set_visible(False)
        
    return current_settings