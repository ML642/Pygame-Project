import pygame

class LoadingScreen:
    def __init__(self, screen, total_items):
        self.screen = screen
        self.total_items = total_items
        self.loaded_items = 0
        self.font = pygame.font.SysFont(None, 36)
        self.progress = 0
        
    def update(self, items_loaded=1):
        self.loaded_items += items_loaded
        self.progress = min(self.loaded_items / self.total_items, 1.0)  # Ensure progress doesn't exceed 100%
        
    def draw(self):
        # Dark overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Loading text
        text = self.font.render("Generating Dungeon...", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Progress bar background
        bar_width = 400
        bar_height = 30
        bar_x = self.screen.get_width()//2 - bar_width//2
        bar_y = self.screen.get_height()//2 + 20
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress bar fill
        fill_width = int(bar_width * self.progress)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height))
        
        # Percentage text
        percent_text = self.font.render(f"{int(self.progress * 100)}%", True, (255, 255, 255))
        percent_rect = percent_text.get_rect(center=(self.screen.get_width()//2, bar_y + bar_height + 20))
        self.screen.blit(percent_text, percent_rect)
        
        pygame.display.flip()  # Important: Update the display