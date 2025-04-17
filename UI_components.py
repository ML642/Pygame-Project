import pygame 
import random 


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


def draw_health_bar(surface, current_hp, max_hp):
    bg_rect = pygame.Rect(20, 20, 200 , 20)
    pygame.draw.rect(surface, WHITE, bg_rect)

    health_width = int((current_hp / max_hp) * 200)
    health_rect = pygame.Rect(20, 20, health_width, 20 )
    
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