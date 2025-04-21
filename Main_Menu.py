import pygame
import random
from UI_components import Menu_option 
from UI_components import DustParticle
import os 
from setting_menu import SettingsMenu
pygame.init()

def Main_menu (actual_screen_width = 1300, actual_screen_height =800):
    os.environ['SDL_VIDEO_CENTERED'] = "1"
  
    screen_width = 800 
    screen_height = 600
 
    scale_x = actual_screen_width / screen_width
    scale_y = actual_screen_height / screen_height
        
    screen = pygame.display.set_mode((800 * scale_x, 600 * scale_y))
    clock = pygame.time.Clock()
    
     
    Main_Menu = True 
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)

    
        
    background = pygame.image.load('images/Background1.png').convert_alpha()
    background = pygame.transform.scale(background,( screen_width * scale_x,screen_height * scale_y))

    Option1 = Menu_option(80 * scale_x, (300 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Play")
    Option2 = Menu_option(80 * scale_x, (370 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Settings")
    Option3 = Menu_option(80 * scale_x, (440 - 100) * scale_y, 200 * scale_x, 50 * scale_y, WHITE, BLUE, "Exit")

    Options = [Option1, Option2, Option3]
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
     
    while Main_Menu :
        screen.blit(background, (0, 0)) 
        current_time = pygame.time.get_ticks()

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
                    pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if active == 0:
                    Main_Menu = False
                    running = True
                    pygame.mouse.set_visible(True)
                elif active == 1:
                    print("Opening settings...")
                    settings_menu = SettingsMenu(actual_screen_width, actual_screen_height) 
                    data = settings_menu.run(screen, Main_menu)  
                    if data :
                        resolution_data = data[1]
                        screen = pygame.display.set_mode(resolution_data)
                        width_x = resolution_data[0]
                        width_y = resolution_data[1]
                        
                        Main_Menu = False 
                        Main_menu(width_x,width_y)
                elif active == 2:
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
        
        Option1.update(80 * scale_x, (300 - 100) * scale_y, screen)
        
        Option2.update(80 * scale_x, (370 - 100) * scale_y, screen)
        
        Option3.update(80 * scale_x, (440 - 100) * scale_y, screen)
        
        arrow_x = 60 * scale_x # X position of the arrow
        if arrow_visible == True:
                if active == 0:
                    draw_arrow(screen, arrow_x, (300 - 75) * scale_y)  # Adjust Y position for Option1
                elif active == 1:
                    draw_arrow(screen, arrow_x, (370 - 75) * scale_y)  # Adjust Y position for Option2
                elif active == 2:
                    draw_arrow(screen, arrow_x, (440 - 75)* scale_y) 
        
        
            
        pygame.display.flip()
        clock.tick(60)
        pygame.mouse.set_visible(False)
        
