import pygame
from pygame.locals import *

from Main_Menu import Main_menu

def Restart (Rooms,player, enemies ,drops,scale_x, scale_y, OFFSET, OFFSETY): 
    for room in Rooms :
        room.active = False 
        room.clear = False 
    player.rect.center = ( -500 +(1-scale_x) * OFFSET ,50 + ( 700 / 2 )* scale_y - OFFSETY  )  # - move the player to the room
    player.health = player.max_health
    for enemy in enemies:
        enemy.kill()
        
        
    drops.empty()
    
    
    return 0
class GameOver:
    def __init__(self, screen, kills, time_elapsed, level_reached , start_time):
        self.screen = screen
        self.kills = kills
        self.time = time_elapsed
        self.level = level_reached
        self.width, self.height = screen.get_size()
        self.start_time = start_time
        
    
        # Load assets
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        # Load image (replace 'game_over_img.png' with your image)
        try:
            self.image = pygame.image.load('images/game_over_img.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (300, 100))  # Adjust size
        except:
            self.image = pygame.Surface((200, 100))
            self.image.fill((255,0,0))
            
        # Button parameters
        self.buttons = [
            {"rect": pygame.Rect(0,0,150,50), "text": "Retry", "action": "restart"},
            {"rect": pygame.Rect(0,0,150,50), "text": "Main Menu", "action": "menu"}
        ]
        
        # Position elements
        self._position_elements()
    def time_transform(self, time):
        print (time )
        time = time / 1000
        if time < 60:
            return f"{int(time)}s"
        elif time < 3600:
            minutes = int(time // 60)
            seconds = int(time % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(time // 3600)
            minutes = int((time % 3600) // 60)
            seconds = int(time % 60)
            return f"{hours}h {minutes}m {seconds}s"
    
        
    def _position_elements(self):
        # Image position
        self.img_rect = self.image.get_rect(center=(self.width//2, self.height//4))
        
        # Stats positions
        self.stats = [
            {"label": "KILLS", "value": self.kills},
            {"label": "TIME", "value": f"{self.time_transform(self.start_time)}"},
            {"label": "LEVEL", "value": self.level}
        ]
        
        # Button positions
        button_spacing = 20
        total_width = sum(b["rect"].width for b in self.buttons) + button_spacing
        start_x = (self.width - total_width) // 2
        for i, btn in enumerate(self.buttons):
            btn["rect"].topleft = (start_x + i*(150 + button_spacing), 
                                  self.height - 150)
            
    def draw_button(self, btn, mouse_pos):
        color = (200, 200, 200) if btn["rect"].collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(self.screen, color, btn["rect"])
        text_surf = self.small_font.render(btn["text"], True, (0,0,0))
        text_rect = text_surf.get_rect(center=btn["rect"].center)
        self.screen.blit(text_surf, text_rect)
        
    def draw(self, mouse_pos):
        # Dark background overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0,0))
        
        # Draw image
        self.screen.blit(self.image, self.img_rect)
        
        # Draw stats
        stat_y = self.img_rect.bottom + 40
        for i, stat in enumerate(self.stats):
            # Draw label
            label_surf = self.font.render(stat["label"], True, (255, 255, 255))
            label_rect = label_surf.get_rect(center=(self.width//2 - 200 + i*200, stat_y))
            self.screen.blit(label_surf, label_rect)
            
            # Draw value
            value_surf = self.font.render(str(stat["value"]), True, (255,255,0))
            value_rect = value_surf.get_rect(center=(self.width//2 - 200 + i*200, stat_y + 30))
            self.screen.blit(value_surf, value_rect)
        
        # Draw buttons
        for btn in self.buttons:
            self.draw_button(btn, mouse_pos)
            
    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    return btn["action"]
        return None

# Example usage in your game loop:

def game_over_screen(screen, kills, time, level,start_time):
    game_over = GameOver(screen, kills, time, level ,start_time)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 'exit'
            elif event.type == MOUSEBUTTONDOWN:
                action = game_over.handle_input(event)
                if action == 'restart':
                    return 'restart'
                elif action == 'menu':
                    return 'menu'
        
        # Draw background (your game's last frame should be underneath)
        game_over.draw(mouse_pos)
        pygame.display.flip()
        
