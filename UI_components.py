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