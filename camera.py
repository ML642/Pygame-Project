import pygame
class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height,scale_x =1  , scale_y =1 ):
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        
        self.scale_x = scale_x
        self.scale_y = scale_y  
  
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + (self.screen_width // 2) 
        y = -target.rect.centery + (self.screen_height // 2) 
        
        # Limit camera to world bounds
        x = max(-(self.world_width - self.screen_width), x)  # Right
        y = max(-(self.world_height - self.screen_height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.world_width / self.scale_x, self.world_height / self.scale_y)

