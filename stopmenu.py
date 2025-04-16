import pygame
import os
import random 
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pause Menu Test")
font = pygame.font.SysFont("Arial", 40)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

running = True
paused = False
volume = 0.5
music = 0.5

    
class DustParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(1, 3)
        self.speed_y = random.uniform(-0.2, -0.5)
        self.alpha = random.randint(50, 100)
        self.lifetime = random.randint(100, 200)
        self.surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)

    def update(self):
        self.y += self.speed_y
        self.alpha -= 0.2
        self.lifetime -= 1

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))  # Clear the surface with full transparency
        pygame.draw.circle(
            self.surface,
            (255, 255, 255, max(0, int(self.alpha))),
            (self.surface.get_width() // 2, self.surface.get_height() // 2),
            self.radius
        )
        screen.blit(self.surface, (self.x, self.y))

    def is_dead(self):
        return self.lifetime <= 0 or self.alpha <= 0


def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    button_rect = pygame.Rect(x, y, width, height,)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surface = font.render(text, True, WHITE)   
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    Border = pygame.Rect(x,y,width,height )
    pygame.draw.rect(screen, WHITE, Border, 2)

    return clicked

def draw_slider(x, y, width, height, value ):
    global volume
    pygame.draw.rect(screen, DARK_GRAY, (x, y + height // 2 - 5, width, 10))
    handle_x = x + int(width * value)
    handle_rect = pygame.Rect(handle_x - 10, y, 20, height)
    pygame.draw.rect(screen, GREEN, handle_rect)

    if pygame.mouse.get_pressed()[0]:
        if pygame.Rect(x, y, width, height).collidepoint(pygame.mouse.get_pos()):
            mouse_x = pygame.mouse.get_pos()[0]
            volume = min(1.0, max(0.0, (mouse_x - x) / width))
    return volume


def draw_slider_music (x, y, width, height, value  ):
    global music
    pygame.draw.rect(screen, DARK_GRAY, (x, y + height // 2 - 5, width, 10))
    handle_x = x + int(width * value)
    handle_rect = pygame.Rect(handle_x - 10, y, 20, height)
    pygame.draw.rect(screen, (125,124,13), handle_rect)

    if pygame.mouse.get_pressed()[0]:
        if pygame.Rect(x, y, width, height).collidepoint(pygame.mouse.get_pos()):
            mouse_x = pygame.mouse.get_pos()[0]
            music  = min(1.0, max(0.0, (mouse_x - x) / width))
    return music 

def pause_menu():
    global paused 
    dust_particles = []
    paused = True
    global running 
    # print("Paused")
    while paused:
        
        
        #print("In pause menu")
       
        screen.fill(BLACK)
        
        if random.random() < 0.85:  # adjust spawn rate
            x = random.randint(0, 800)
            y = random.randint(400, 600)  # near bottom
            dust_particles.append(DustParticle(x, y))



        for particle in dust_particles:
            particle.update()
            particle.draw(screen)

        # Remove dead particles
        dust_particles = [p for p in dust_particles if not p.is_dead()]
        
        
        React = pygame.Rect(220,140,360,400)
        
        
        
        pygame.draw.rect(screen, WHITE , React  , 10 )
        
        
        [X, Y ] = pygame.mouse.get_pos()
        
        font = pygame.font.SysFont("Bauhaus 93", 70)
        title = font.render(f" GAME PAUSED ", True, WHITE)
        screen.blit(title, (330 - 150, 50))
        
     
        # Buttons
        if draw_button("Resume" , 300, 350-70, 200, 50, BLACK, (0, 155, 0)):
            paused = False
        if draw_button("Settings" , 300, 350, 200, 50, BLACK, (255, 128, 0)):
            # settings logic here 
            {}
            
        
        if draw_button("Quit", 300, 420, 200, 50, BLACK, (255, 100, 100)):
            if confirm_quit():
                running = False
                pygame.quit()
                paused = False

        # Volume slider
        
        image_sound = pygame.image.load('images/volume.png').convert_alpha()
        sound_icon = pygame.transform.scale(image_sound , (50, 50))
        
        screen.blit(sound_icon, (240, 190 - 20))
        draw_slider(300, 200 - 20, 200, 30, volume)

        music_sound = pygame.image.load('images/music.png').convert_alpha()
        music_icon = pygame.transform.scale(music_sound , (40, 40))
   
        screen.blit(music_icon, (240, 240 - 20))
        draw_slider_music(300, 250 - 20 , 200, 30, music )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

def confirm_quit():
    while True:
        
        screen.fill(BLACK)
        message = font.render("Quit Game?", True, WHITE)
        screen.blit(message, (300, 200))

        if draw_button("Yes", 250, 300, 100, 50, RED, (255, 100, 100)):
            return True
        if draw_button("No", 450, 300, 100, 50, GREEN, (100, 255, 100)):
            return False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True


# clock = pygame.time.Clock()

# while running:
#     screen.fill((30, 30, 30))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 paused = True
#                 pause_menu()

#     # Display the current volume
#     vol_display = font.render(f"Volume: {round(volume * 100)}%", True, WHITE)
#     screen.blit(vol_display, (300, 280))

#     info = font.render("Running game... Press ESC to pause", True, WHITE)
#     screen.blit(info, (120, 350))

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
