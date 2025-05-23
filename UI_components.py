import pygame 
import random 



BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


def draw_health_bar(surface, current_hp, max_hp, scale_x = 2 , scale_y = 2):
    bg_rect = pygame.Rect(140* scale_x, 5 * scale_y, 300 * scale_x , 30 * scale_y)
    pygame.draw.rect(surface, WHITE, bg_rect)

    health_width = int((current_hp / max_hp) * 300 * scale_x)
    health_rect = pygame.Rect(140 * scale_x, 5* scale_y, health_width, 30 * scale_y )
    
    pygame.draw.rect(surface, RED, health_rect)
    pygame.draw.rect(surface, BLACK, bg_rect, 2) 




class Menu_option (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, hover_color,text):
        super().__init__()
        self.image = pygame.Surface((width , height))
        
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = color
        self.hover_color = hover_color
        
        self.original_width = width 
        self.original_height = height
        
        self.hover_width = width + 100
        self.hover_height = height  
         
        
        
        self.active = False 
        self.text = text 
        self.width = width  
        self.height = height
    
    
    
    def update(self , x , y, screen):        
            font = pygame.font.SysFont("Bauhaus 93", 42)
            shadow = font.render(self.text, True, BLACK)
            shadow.set_alpha(150,150)
            # Smoothly transition the size
            target_width = self.hover_width if self.active else self.original_width
            target_height = self.hover_height if self.active else self.original_height

            self.width += (target_width - self.width) * 0.05
            self.height += (target_height - self.height) * 0.2
           
            self.image = pygame.Surface((int(self.width), int(self.height)), pygame.SRCALPHA)  # Use SRCALPHA for transparency
           
            self.image.fill((0, 0, 0, 0))
           
            pygame.draw.rect(
                    self.image,
                    self.hover_color if self.active else self.color,
                    (0, 0, int(self.width), int(self.height)),
                    border_radius = 15  # Adjust the border radius for rounded corners
                )
            
            # Update the button's image and rect
            
            
            self.rect = self.image.get_rect(topleft=(x, y))

            # Draw the text
            text_surface = font.render(self.text, True, BLACK if not self.active else WHITE)
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
            
            if self.active == True :
                self.image.blit(shadow, (text_rect.x + 10, text_rect.y + 5))

            self.image.blit(text_surface, text_rect)
           
            # Blit the button to the screen
            screen.blit(self.image, self.rect.topleft)
        
    def toogle  (self): 
       self.active = not self.active
    
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
    
def draw_reload_bar(screen, x, y, scale_x, scale_y, reload_progress, 
                   bg_color=(50, 50, 50), fill_color=(255, 150, 0),
                   glow_color=(255, 223, 0), text_color=(255, 255, 200)):
    """
    Draws an animated reload progress bar
    Parameters:
    - screen: Target surface to draw on
    - x, y: Top-left position (base coordinates before scaling)
    - scale_x, scale_y: Scaling factors
    - reload_progress: 0.0-1.0 value indicating reload completion
    - colors: Optional color overrides
    """
    # Calculate scaled dimensions
    bar_width = int(200 * scale_x)
    bar_height = int(24 * scale_y)
    pos_x = int(x * scale_x)
    pos_y = int(y * scale_y)
    border_radius = int(5 * scale_x)
    
    # Animated glow background
    glow_alpha = abs(pygame.time.get_ticks() % 1000 - 500) / 5
    glow_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
    pygame.draw.rect(glow_surface, (*glow_color, int(glow_alpha)), 
                    glow_surface.get_rect(), border_radius=border_radius)
    screen.blit(glow_surface, (pos_x, pos_y))
    
    # Background container
    pygame.draw.rect(screen, bg_color, (pos_x, pos_y, bar_width, bar_height), 
                    border_radius=border_radius)
    pygame.draw.rect(screen, (100, 100, 100), (pos_x, pos_y, bar_width, bar_height), 
                    2, border_radius=border_radius)
    
    # Progress bar
    current_width = bar_width * reload_progress
    gradient = pygame.Surface((current_width, bar_height))
    for i in range(int(current_width)):
        alpha = int(255 * (i/current_width)) if current_width > 0 else 0
        pygame.draw.line(gradient, (fill_color[0], fill_color[1] + alpha//4, fill_color[2]), 
                        (i, 0), (i, bar_height))
    
    # Clip the gradient to rounded rectangle
    mask = pygame.Surface((current_width, bar_height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255,255,255,255), (0, 0, current_width, bar_height), 
                    border_radius=border_radius)
    gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    screen.blit(gradient, (pos_x, pos_y))
    
    # Percentage text
    font = pygame.font.SysFont("Arial Bold", int(14 * scale_x))
    text = font.render(f"{int(reload_progress*100)}%", True, text_color)
    text_rect = text.get_rect(center=(pos_x + bar_width//2, pos_y + bar_height + 10 * scale_y))
    screen.blit(text, text_rect)
    
    # Reload icon (optional - needs image file)
    try:
        icon_size = int(20 * scale_x)
        reload_icon = pygame.transform.scale(pygame.image.load("images/reload_icon.png"), 
                                            (icon_size, icon_size))
        screen.blit(reload_icon, (pos_x + bar_width + 5 * scale_x, pos_y - 2 * scale_y))
    except FileNotFoundError:
        pass

def draw_minimap(screen, player, Rooms, boss_room_rect=None):
    minimap_width = 200
    minimap_height = 150
    minimap_surface = pygame.Surface((minimap_width, minimap_height))
    minimap_surface.fill((30, 30, 30))

    room_scale_x = 10
    room_scale_y = 7

    all_rects = [room.rect for room in Rooms]
    if boss_room_rect:
        all_rects.append(boss_room_rect)

    min_x = min(rect.x for rect in all_rects)
    min_y = min(rect.y for rect in all_rects)

    for room in Rooms:
        rect = pygame.Rect(
            ((room.rect.x - min_x) // 70),
            ((room.rect.y - min_y) // 70),
            room.rect.width // 70,
            room.rect.height // 70
        )
        pygame.draw.rect(minimap_surface, (100, 100, 255), rect)

    if boss_room_rect:
        rect = pygame.Rect(
            ((boss_room_rect.x - min_x) // 70),
            ((boss_room_rect.y - min_y) // 70),
            boss_room_rect.width // 70,
            boss_room_rect.height // 70
        )
        pygame.draw.rect(minimap_surface, (255, 0, 0), rect, 2)

    player_pos = (
        (player.rect.centerx - min_x) // 70,
        (player.rect.centery - min_y) // 70
    )
    pygame.draw.circle(minimap_surface, (0, 255, 0), player_pos, 3)

    screen.blit(minimap_surface, (screen.get_width() - minimap_width - 10, 10))

    
    
class StopButton :
        def __init__(self, screen, x, y, width, height):
            self.screen = screen
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.image = pygame.image.load('images/button.webp').convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect(topleft=(x, y))
            
        def draw(self,screen):
            screen.blit(self.image, (self.x, self.y))
            pygame.draw.rect(screen, WHITE, self.rect, 2)

