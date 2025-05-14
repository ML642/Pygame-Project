import pygame
from pygame import mixer
import ctypes
import sys 


class SettingsMenu:
    def __init__(self, screen_width, screen_height , settings_data=None):
        
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        self.max_resolution = (root.winfo_screenwidth(), root.winfo_screenheight())
        root.destroy()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.font_large = pygame.font.SysFont("Arial", 48)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_low = pygame.font.SysFont("Arial" , 24 )
        self.setting_data = settings_data

        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.music_slider_rect = pygame.Rect(300, 200, 200, 20)
        self.sfx_slider_rect = pygame.Rect(300, 300, 200, 20)
        
         
        self.active_button = 1
        
        self.pass_difficulty = 0
        self.resolution2 = [(800,600) , (1350,700) , self.max_resolution]
        self.pass_resolution = 0
        self.pass_volume = 0.5
        self.pass_music = 0
        
        print(settings_data)

        
        # Button rects
        self.back_button = pygame.Rect(300, 400, 200, 50)
        
        self.volume  = 50 
        
        self.music = 50 
        
        
        self.difficult = ["easy","medium" , "hard" ]
        
        
        self.resolution = ["800x600" , "1350x700" , "Full Screen"]
        self.resolution_n =0 
        
      
        
        mixer.init()
        #pygame.mixer.music.load("path_to_your_music_file.mp3")  # Replace with your music file
    def update (self):
        if self.setting_data :
            self.music = self.setting_data["music_volume"]
            self.pass_music = self.setting_data["music_volume"]
            self.pass_volume = self.setting_data["sfx_volume"]
            self.volume = self.setting_data["sfx_volume"]
            if self.setting_data["difficulty"] == "easy":
                self.difficult_n = 0
                self.pass_difficulty = 0
                print("easy")
            elif self.setting_data["difficulty"] == "medium":
                self.difficult_n = 1
                self.pass_difficulty = 1
                print("medium")
            elif self.setting_data["difficulty"] == "hard":
                self.difficult_n = 2
                self.pass_difficulty = 2
                print("hard")
        if self.setting_data["resolution"] == (800, 600):
            self.resolution_n = 0
            self.pass_resolution = 0
            print("800x600")
        elif self.setting_data["resolution"] == (1350, 700):
            self.resolution_n = 1
            self.pass_resolution = 1
            print("1350x750")
            
        elif self.setting_data["resolution"] == self.max_resolution:
            self.resolution_n = 2
            self.pass_resolution = 2
                
        #pygame.mixer.music.play(-1)
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
    def draw_back(self,screen ,x,y,width,height,text,color,hover_color ,value , active ):
        button_rect = pygame.Rect(x, y, width, height)

        if active == True :
            pygame.draw.rect(screen, ( 255,255,255) ,button_rect , 0 , 10 )
            title = self.font_medium.render(text, True, (0, 0, 0))            
            screen.blit(title ,( x + 75 , y + 20) )
        if active == False :
            pygame.draw.rect(screen, (0,0,0) , button_rect , 0 , 10   )
            title = self.font_medium.render(text, True, (255, 255, 255))
            screen.blit(title ,( x + 75  , y + 20) )
      
            
        
        
        
        
        
        
    def draw_option(self, screen, x, y, width, height, text, color, hover_color,value , active ,font_size, paddingX = 0 , paddingY = 0 ,scalex = 1 ,scaley=1):
        
        
        button_rect = pygame.Rect(x, y, width, height)

        if active == True :
            pygame.draw.rect(screen, ( 255,255,255) ,button_rect , 0 , 10 )
            font_medium = pygame.font.SysFont("Arial",int(32 * scalex))
          
            title = font_medium.render(text, True, (0, 0, 0))
          
            font = pygame.font.SysFont("Arial", int(font_size * scalex))
            value  = font.render(f"{value}", True, (0, 0, 0))
           
            value_width,value_height =  value.get_size()
            
            
            
            screen.blit(title ,( x + 50 , y + 20) )
            
            self.draw_triangle(screen , x +325* scalex, y + 40* scaley , 20 * scalex , (0,0,0) ,  "left")
            
            screen.blit(value , ( x  + (400 -25 - paddingX)* scalex ,y + 20* scaley + paddingY   ))  
            
            self.draw_triangle(screen , x + (470)* scalex, y + 40 * scaley , 20  * scalex, (0,0,0) ,  "right")
            
        if active == False :
            pygame.draw.rect(screen, (0,0,0) , button_rect , 0 , 10   )
            
            font_medium = pygame.font.SysFont("Arial",int(32 * scalex))

            title = font_medium.render(text, True, (255, 255, 255))
            font = pygame.font.SysFont("Arial", int(font_size * scalex))

            value  = font.render(f"{value}", True, (255, 255, 255))
          
            screen.blit(title ,( x + 50  , y + 20) )
            
            self.draw_triangle(screen , x +325* scalex, y + 40 * scaley , 20 * scalex , (255,255,255) ,  "left")
            
            screen.blit(value , ( x  +(400 -25 - paddingX)* scalex  , y + (20 + paddingY)* scaley   ))  
            
            self.draw_triangle(screen , x + 470 * scalex, y + 40  * scaley, 20 * scalex , (255,255,255) ,  "right")
            

        

     
    def draw(self, screen, scalex, scaley):
        # Semi-transparent background
        self.screen_width = self.resolution2[self.pass_resolution][0]
        self.screen_height = self.resolution2[self.pass_resolution][1]
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        rect = pygame.Rect(100, 10, self.screen_width - 200, self.screen_height - 20 )
        pygame.draw.rect(screen, (50, 50, 50), rect, border_radius=20)
        
        
        if self.active_button == 1:
         self.draw_option(screen , 150  * scalex, (150-50) * scaley , 500 * scalex , 75 * scaley , "DIFFICULTY", (0,0,0) , (255,255,255) , self.difficult[self.difficult_n] , True ,  22 ,15  , 5 ,  scalex , scaley)
        else :
         self.draw_option(screen , 150 * scalex,(150 -50) * scaley, 500 * scalex , 75 * scaley , "DIFFICULTY", (0,0,0) , (255,255,255) , self.difficult[self.difficult_n] , False  ,22 , 15 , 5 , scalex , scaley)
        if self.active_button == 2:
            self.draw_option(screen , 150 * scalex, (250 -50 ) * scaley , 500 * scalex , 75 * scaley , "RESOLUTION" , (0,0,0) , (255,255,255),self.resolution[self.resolution_n], True ,22 ,20  , 7 , scalex , scaley)
        else:
            self.draw_option(screen , 150 * scalex, (250 -50)* scaley, 500 * scalex , 75 * scaley , "RESOLUTION" , (0,0,0) , (255,255,255),self.resolution[self.resolution_n], False ,22,20  , 7 , scalex , scaley)

        if self.active_button == 3 :   
         self.draw_option(screen , 150 * scalex, (350 -50)*scaley, 500 * scalex, 75 * scaley , "MUSIC" , (0,0,0) , (255,255,255),self.music, True ,32,0 ,0 , scalex , scaley)
        else :
         self.draw_option(screen , 150  * scalex, (350 -50) * scaley, 500 * scalex, 75 * scaley , "MUSIC" , (0,0,0) , (255,255,255),self.music , False ,32,0 ,0 , scalex , scaley)
        if self.active_button == 4 :
         self.draw_option(screen , 150 * scalex , (450 -50)* scaley, 500 * scalex, 75 * scaley ,  "SOUND" , (0,0,0), (255,255,255) , self.volume ,  True ,32 ,0 ,0 , scalex , scaley)
        else :
          self.draw_option(screen , (150)* scalex , (450-50)* scaley, 500 * scalex, 75 * scaley ,  "SOUND" , (0,0,0), (255,255,255) , self.volume  ,  False ,32 ,0 ,0 , scalex , scaley)
        
        if self.active_button == 5:
          self.draw_back(screen,170* scalex,500* scaley ,225 * scalex,75 * scaley , "BACK" , (0,0,0),(255,255,255), 0 , True)
        else :
          self.draw_back(screen,170 * scalex,500 * scaley ,225 * scalex,75 * scaley , "BACK" , (0,0,0),(255,255,255), 0 , False) 
        
        
        if self.active_button == 6 : 
            self.draw_back(screen, (190 + 225) * scalex ,500* scaley ,225 * scalex,75 * scaley , "APPLY" , (0,0,0),(255,255,255), 0 , True)
        else :
            self.draw_back(screen,(190 + 225)* scalex,500* scaley ,225 * scalex,75 * scaley , "APPLY" , (0,0,0),(255,255,255), 0 , False)
           
        title = self.font_large.render("SETTINGS", True, (255, 255, 255))
        
        
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        

    def handle_event( self, event ):
        #print(self.active_button)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP  or event.key == pygame.K_w: 
                self.active_button -= 1
                if self.active_button < 1 :
                    self.active_button  = 5 
            if event.key == pygame.K_DOWN or event.key == pygame.K_s :
                self.active_button += 1
                if self.active_button > 5 :
                    self.active_button  = 1
        #    print(self.active)
            if event.key == pygame.K_RIGHT :
                 if self.active_button == 1 :
                     self.difficult_n +=1
                     if self.difficult_n > 2 :
                         self.difficult_n = 0 
                 if self.active_button == 2 : 
                     self.resolution_n +=1
                     if self.resolution_n > 2 :
                         self.resolution_n = 0
          
                         
                 if self.active_button == 3 :
                     if self.music != 100 :
                          self.music +=1
                 if self.active_button ==4 :
                     if self.volume !=100 :
                      self.volume += 1    
                 if self.active_button ==5 :
                    self.active_button =6  
            if event.key == pygame.K_LEFT :
                 if self.active_button == 1 :
                     self.difficult_n -=1
                     if self.difficult_n < 0  :
                         self.difficult_n = 2 
                 if self.active_button == 2 : 
                     self.resolution_n -=1
                     if self.resolution_n < 0 :
                         self.resolution_n = 2
                 if self.active_button == 3 :
                     if self.music != 0 :
                          self.music -=1
                          
                 if self.active_button ==4 :
                     if self.volume !=0 :
                      self.volume -= 1  
                 if self.active_button == 6 :
                     self.active_button = 5
            if event.key == pygame.K_RETURN and self.active_button == 5:
                self.active = False 
            if event.key == pygame.K_RETURN and self.active_button == 6:
                self.pass_resolution = self.resolution_n 
                self.pass_music = self.music
                self.pass_difficulty = self.difficult
                self.pass_volume = self.volume 
                
                if self.resolution_n == 0 :               
                 screen = pygame.display.set_mode((800,600))
                if self.resolution_n == 1 :
                 screen = pygame.display.set_mode((1350,750))
                if self.resolution_n == 2 :
                 screen = pygame.display.set_mode(self.max_resolution)
                
                    
    def run(self, screen , Mainmenu):
        self.active = True
        #pygame.mixer.music.set_volume(self.music /100)
        pygame.mixer.init()
        pygame.mixer.music.load("sound/music.mp3")  # Relative path
        pygame.mixer.music.play(-1)
        while self.active:
            pygame.mixer.music.set_volume(self.music / 100)
            data = {
            "difficulty": self.difficult[self.difficult_n],
            "resolution": self.resolution2[self.pass_resolution],
            "music_volume": self.music,
            "sfx_volume": self.volume
            }
            scalex  = self.resolution2[self.pass_resolution][0] / 800
            scaley  = self.resolution2[self.pass_resolution][1] / 600
            
            #print(scalex , scaley)
      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return data
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.active = False
                        
                        
                self.handle_event(event)
            
            
            screen.fill((0, 0, 0))  # Clear screen
            self.draw(screen,scalex,scaley)
            pygame.display.flip()
        return data    