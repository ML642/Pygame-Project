import pygame
from pygame import mixer

class SettingsMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.font_large = pygame.font.SysFont("Arial", 48)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        
        # Slider values (0.0 to 1.0)
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.music_slider_rect = pygame.Rect(300, 200, 200, 20)
        self.sfx_slider_rect = pygame.Rect(300, 300, 200, 20)
        
        self.active  = True 
        self.active_button = 1
        
        
        # Button rects
        self.back_button = pygame.Rect(300, 400, 200, 50)
        
        self.volume  = 50 
        self.music = 50 
        self.difficult = ["easy","medium" , "hard" , "extreme"]
        
        self.resolution = ["600x800" , "1350x750" , "Full Screen"]
        
    
    def draw_triangle(self,surface, x, y, size=40, color=(255, 0, 0), direction="up"):
        if direction == "up":
            points = [(x, y), (x - size // 2, y + size), (x + size // 2, y + size)]
        elif direction == "down":
            points = [(x, y), (x - size // 2, y - size), (x + size // 2, y - size)]
        elif direction == "left":
            points = [(x, y), (x + size, y - size // 2), (x + size, y + size // 2)]
        elif direction == "right":
            points = [(x, y), (x - size, y - size // 2), (x - size, y + size // 2)]
        else:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

        pygame.draw.polygon(surface, color, points)
    def draw_option(self, screen, x, y, width, height, text, color, hover_color,value , active ):
        
        
        button_rect = pygame.Rect(x, y, width, height)

        if active == True :
            pygame.draw.rect(screen, ( 255,255,255) ,button_rect , 0 , 10 )
            
          
            title = self.font_medium.render(text, True, (0, 0, 0))
          
            value  = self.font_large.render(f"{value}", True, (0, 0, 0))
          
            screen.blit(title ,( x + 50 , y + 20) )
            
            self.draw_triangle(screen , x +325, y + 40 , 20 , (0,0,0) ,  "left")
            
            screen.blit(value , ( x  + 400 , y + 20   ))  
            
            self.draw_triangle(screen , x + 470, y + 40 , 20 , (0,0,0) ,  "right")
            
        if active == False :
            pygame.draw.rect(screen, (0,0,0) , button_rect , 0 , 10   )
            
            title = self.font_medium.render(text, True, (255, 255, 255))
          
            value  = self.font_large.render(f"{value}", True, (255, 255, 255))
          
            screen.blit(title ,( x + 50 , y + 20) )
            
            self.draw_triangle(screen , x +325, y + 40 , 20 , (255,255,255) ,  "left")
            
            screen.blit(value , ( x  + 400 , y + 20   ))  
            
            self.draw_triangle(screen , x + 470, y + 40 , 20 , (255,255,255) ,  "right")
            

        

     
    def draw(self, screen):
        # Semi-transparent background
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        rect = pygame.Rect(100, 50, self.screen_width - 200, self.screen_height - 100 )
        pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=20)
        
        
        if self.active_button == 1:
         self.draw_option(screen , 150 , 150 , 500 , 75 , "DIFFICULTY", (0,0,0) , (255,255,255) , self.difficult , True  )
        else :
         self.draw_option(screen , 150 , 150 , 500 , 75 , "DIFFICULTY", (0,0,0) , (255,255,255) , self.difficult , False  )
        if self.active_button == 2:
            self.draw_option(screen , 150 , 250 , 500 , 75 , "RESOLUTION" , (0,0,0) , (255,255,255),self.resolution, True )
        else:
            self.draw_option(screen , 150 , 250 , 500 , 75 , "RESOLUTION" , (0,0,0) , (255,255,255),self.resolution, False )

        if self.active_button == 3 :   
         self.draw_option(screen , 150 , 350 , 500 , 75 , "MUSIC" , (0,0,0) , (255,255,255),self.resolution, True )
        else :
         self.draw_option(screen , 150 , 350 , 500 , 75 , "MUSIC" , (0,0,0) , (255,255,255),self.resolution , False )
        if self.active_button == 4 :
         self.draw_option(screen , 150 , 450, 500 , 75 ,  "SOUND" , (0,0,0), (255,255,255) , 0 ,  True  )
        else :
          self.draw_option(screen , 150 , 450, 500 , 75 ,  "SOUND" , (0,0,0), (255,255,255) , 0 ,  False  )
 
           
        title = self.font_large.render("SETTINGS", True, (255, 255, 255))
        
        
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        
        
        
        
        # screen.blit(self.music_icon, (200, 190))
        # music_text = self.font_medium.render("Music:", True, (255, 255, 255))
        # screen.blit(music_text, (250, 190))
        
        # # Music slider
        # pygame.draw.rect(screen, (100, 100, 100), self.music_slider_rect)
        # pygame.draw.rect(screen, (0, 200, 0), 
        #                 (self.music_slider_rect.x, 
        #                  self.music_slider_rect.y, 
        #                  self.music_slider_rect.width * self.music_volume, 
        #                  self.music_slider_rect.height))
        
        # # SFX Volume
        # screen.blit(self.sfx_icon, (200, 290))
        # sfx_text = self.font_medium.render("SFX:", True, (255, 255, 255))
        # screen.blit(sfx_text, (250, 290))
        
        # # SFX slider
        # pygame.draw.rect(screen, (100, 100, 100), self.sfx_slider_rect)
        # pygame.draw.rect(screen, (0, 150, 200), 
        #                 (self.sfx_slider_rect.x, 
        #                  self.sfx_slider_rect.y, 
        #                  self.sfx_slider_rect.width * self.sfx_volume, 
        #                  self.sfx_slider_rect.height))
        
        # # Back button
        # pygame.draw.rect(screen, (70, 70, 70), self.back_button, border_radius=10)
        # back_text = self.font_medium.render("BACK", True, (255, 255, 255))
        # screen.blit(back_text, (self.back_button.centerx - back_text.get_width()//2, 
        #                        self.back_button.centery - back_text.get_height()//2))

    def handle_event( self, event ):
        print(self.active_button)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP  or event.key == pygame.K_w: 
                self.active_button -= 1
                if self.active_button < 1 :
                    self.active_button  = 4 
            if event.key == pygame.K_DOWN or event.key == pygame.K_s :
                self.active_button += 1
                if self.active_button > 4 :
                    self.active_button  = 1
            if event.key == pygame.K_RIGHT :
                {}
            if event.key == pygame.K_LEFT :
                {}
               
    
    def run(self, screen):
        self.active = True
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.active = False
                
                self.handle_event(event)
            
            screen.fill((0, 0, 0))  # Clear screen
            self.draw(screen)
            pygame.display.flip()