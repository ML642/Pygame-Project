import pygame 

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
        self.image = pygame.Surface((width, height))
        
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = color
        self.hover_color = hover_color
        self.active = False 
        self.text = text 
        self.width = width  
        self.height = height
        
    def update(self , x , y, screen):        
        font = pygame.font.Font(None, 36)
        if  self.active ==  False : 
             text_surface = font.render(self.text, True, BLACK)
        else :
             text_surface = font.render (self.text , True , WHITE )
             
        text_rect = text_surface.get_rect(center=(x + self.width / 2, y + self.height / 2))
        
        screen.blit(text_surface, (text_rect))
        
    def toogle  (self): 
         if self.active : 
             self.active = False 
             self.image.fill(self.color)
         else : 
             self.active = True
             self.image.fill(self.hover_color)