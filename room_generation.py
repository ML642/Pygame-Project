import pygame 
import random 

ROOM_WIDTH, ROOM_HEIGHT = 700 , 500


#ROOMS FORM 
# 1 : All gates 
# 2 : without top gate : right , left , bottom 
# 3 : without right gate : top ,left , bottom
# 4 : without top and right gate : left , bottom
# 5 : without right  and left  gate : top  , bottom
# 6 : left corridor only
# 7 : right corridor only
# 8 : bottom  and right corridor only    
#9  : left and right 
#10 : top only 
#11 : top and right 
class Room (pygame.sprite.Sprite) : 
    def __init__ (self, x , y , enemies_counter, scale_x =1 , scale_y =1): 
        super().__init__()        
        
        self.clear = False 
        self.enemies_counter = enemies_counter  
        self.active = False
        self.surface = pygame.Surface(((ROOM_WIDTH - 130)* scale_x, (ROOM_HEIGHT - 180)* scale_y))
        
        self.rect = self.surface.get_rect(topleft=(x + 60 * scale_x, y + 60  * scale_y))
        
        self.rect.x = x + 60 * scale_x 
        self.rect.y = y + 60 * scale_y




class Floor (pygame.sprite.Sprite) : 
    def __init__ (self, x , y , scale_x = 1 , scale_y = 1): 
        super().__init__()
        try :
            self.image_orig = pygame.image.load("images/Floor.png").convert_alpha()
            self.image = pygame.transform.scale(self.image_orig , (ROOM_WIDTH * scale_x,ROOM_HEIGHT * scale_y))
        except :
            self.image = pygame.Surface((50, 50))
            self.image.fill((100, 100, 100))
        
        self.rect = self.image.get_rect(topleft=(x,y))
class Floor_Hallway (pygame.sprite.Sprite) :
    def __init__ (self, x , y,  w ,  h  , scale_x = 1 , scale_y = 1): 
        super().__init__()
        try :
            self.image_orig = pygame.image.load("images/Floor.png").convert_alpha()
            self.image = pygame.transform.scale(self.image_orig , (w * scale_x,h* scale_y))
        except :
            self.image = pygame.Surface((50, 50))
            self.image.fill((100, 100, 100))
        
        self.rect = self.image.get_rect(topleft=(x,y))       


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h ,scale_x  , scale_y ):
        super().__init__()
        
        self.image_orig = pygame.image.load("images/Wall.jpg").convert_alpha()

        w = max(w, 0)
        h = max(h, 0)

        self.image = pygame.transform.scale(self.image_orig,(w * scale_x,h * scale_y))
        
        self.rect = self.image.get_rect( topleft=(x * scale_x, y * scale_y) )

class Gate(Wall):
        def __init__(self, x, y, w, h, open_image_path, closed_image_path,scale_x =1 ,scale_y = 1):
            super().__init__(x, y, w, h, scale_x , scale_y)
            self.open_image = pygame.image.load(open_image_path).convert_alpha()
            self.open_image = pygame.transform.scale(self.open_image, (w * scale_x , h * scale_y))
            self.closed_image = pygame.image.load(closed_image_path).convert_alpha()
            self.closed_image = pygame.transform.scale(self.closed_image, (w* scale_x, h * scale_y))
            self.is_open = True  # Initially closed
            self.original_rect = self.rect.copy()
            self.rect = pygame.Rect(5000, 5000, 0, 0)
            self.update_image()
        def update_image(self):
            """Update the gate's image based on its state."""
            if self.is_open:
                self.image = self.open_image
            else:
                self.image = self.closed_image
                
        def toogle(self,walls_group):
          self.is_open = not self.is_open
          if self.is_open:
               self.rect = pygame.Rect(5000, 5000, 0, 0)
          else:
              self.rect = self.original_rect 
             
          self.update_image()
def generate_room( x , y , form , type ,scale_x = 1 , scale_y = 1 ):
    # print(f"Generating room ({x}, {y}), form: {form}") #Room gen type check, debug thing
    if form == 'boss':
        return generate_boss_room(x, y, scale_x, scale_y)
    walls = pygame.sprite.Group()
    if form == 1 : 
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 450,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x  , scale_y ))
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 250,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320,scale_x ,scale_y)) # - top 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH - 450 , 20,scale_x,scale_y))# Top
        walls.add(Wall((x-50)+500, 50 + (y-50), ROOM_WIDTH - 450 , 20 , scale_x, scale_y))# Top
     
     
        Gate1 = Gate((x-50)+ROOM_WIDTH - 400,(y-50) +  50, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png",scale_x , scale_y)
        walls.add(Gate1)
    # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT - 320, scale_x, scale_y))  # Left
        walls.add(Wall(x, (y-50)+ ROOM_HEIGHT - 150 ,  20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate2 = Gate(x, (y-50) + ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate2)
    #left gate gap 
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT -320, scale_x, scale_y))  # Right
        walls.add(Wall(ROOM_WIDTH+x-20, y - 50 +  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x +680,  y+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x + 680,  y+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate3 = Gate(x-20+ROOM_WIDTH ,y - 50 +  ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate3)
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y))  # Bottom
        walls.add(Wall(x - 50 + 500, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y)) 

        walls.add(Wall(x + ROOM_WIDTH- 450, y + 20-(ROOM_HEIGHT-320)+640, 20, ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall(x + ROOM_WIDTH- 250, y + 20-(ROOM_HEIGHT-320)+640, 20, ROOM_HEIGHT-320, scale_x, scale_y)) # - bottom 
        
        Gate4 = Gate(x -50 + ROOM_WIDTH-400, y-50+ 30+ROOM_HEIGHT, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate4)
   
    elif form == 2 : #  without top hall 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH  , 20, scale_x, scale_y))# Top
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT - 320, scale_x, scale_y))  # Left
        walls.add(Wall(x, (y-50)+ ROOM_HEIGHT - 150 ,  20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate2 = Gate(x, (y-50) + ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate2)
        #left gate gap 
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT -320, scale_x, scale_y))  # Right
        walls.add(Wall(ROOM_WIDTH+x-20, y - 50 +  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x +680,  y+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x + 680,  y+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate3 = Gate(x-20+ROOM_WIDTH ,y - 50 +  ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate3)
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y))  # Bottom
        walls.add(Wall(x - 50 + 500, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y)) 

        walls.add(Wall(x + ROOM_WIDTH- 450,y + 20-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall(x + ROOM_WIDTH- 250,y+ 20-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - bottom 
        
        
        Gate4 = Gate(x -50 + ROOM_WIDTH-400 ,y-50+ 30+ROOM_HEIGHT, 220  , 20 ,   "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate4)
        # Inner walls (random)
      
    elif form == 3 :  #without right hall 
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 450,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 250,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - top 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
        walls.add(Wall((x-50)+500, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
     
     
        Gate1 = Gate((x-50)+ROOM_WIDTH - 400,(y-50) +  50, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate1)
    # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT - 320, scale_x, scale_y))  # Left
        walls.add(Wall(x, (y-50)+ ROOM_HEIGHT - 150 ,  20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
    
        Gate2 = Gate(x,(y-50) + ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate2)
    #left gate gap 
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT, scale_x, scale_y))  # Right
        
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y))  # Bottom
        walls.add(Wall(x - 50 + 500, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y)) 

        walls.add(Wall(x + ROOM_WIDTH - 450, y + 20 - (ROOM_HEIGHT - 320) + 640, 20, ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall(x + ROOM_WIDTH - 250, y + 20 - (ROOM_HEIGHT - 320) + 640, 20, ROOM_HEIGHT-320, scale_x, scale_y)) # - bottom 
         
        
        Gate4 = Gate(x + ROOM_WIDTH - 450, y - 50 + 30 + ROOM_HEIGHT, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y) 
    
        walls.add(Gate4)
    # Inner walls (random)
    if form == 4  : #without top and right hall 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH  , 20, scale_x, scale_y))# Top
    # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT - 320, scale_x, scale_y))  # Left
        walls.add(Wall(x, (y-50)+ ROOM_HEIGHT - 150 ,  20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
    
        Gate2 = Gate(x, (y-50) + ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate2)
    #left gate gap 
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT, scale_x, scale_y))  # Right
        
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y))  # Bottom
        walls.add(Wall(x - 50 + 500, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y)) 

        walls.add(Wall(x + ROOM_WIDTH- 450, y + 20-(ROOM_HEIGHT-320)+640, 20, ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall(x + ROOM_WIDTH- 250, y+ 20-(ROOM_HEIGHT-320)+640, 20, ROOM_HEIGHT-320, scale_x, scale_y)) # - bottom 
        
        
        Gate4 = Gate(x -50 + ROOM_WIDTH-400, y-50+ 30+ROOM_HEIGHT, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
    
        walls.add(Gate4)
    elif form == 5 : # without left and right hall 
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 450,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 250,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - top 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
        walls.add(Wall((x-50)+500, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
     
     
        Gate1 = Gate((x-50)+ROOM_WIDTH - 400,(y-50) +  50, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate1)
    # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT, scale_x, scale_y))  # Left
       
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT, scale_x, scale_y)) 
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y))  # Bottom
        walls.add(Wall(x - 50 + 500, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y)) 

        walls.add(Wall(x + ROOM_WIDTH- 450,y + 20-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall(x + ROOM_WIDTH- 250,y+ 20-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - bottom 
        
        
        Gate4 = Gate(x -50 + ROOM_WIDTH-400 ,y-50+ 30+ROOM_HEIGHT, 220  , 20 ,   "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
    
        walls.add(Gate4)
    elif form == 6 :  #left corridor only 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH  , 20, scale_x, scale_y))# Top
    # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT - 320, scale_x, scale_y))  # Left
        walls.add(Wall(x, (y-50)+ ROOM_HEIGHT - 150 ,  20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
    
        Gate2 = Gate(x, (y-50) + ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate2)
    #left gate gap 
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT, scale_x, scale_y))  # Right
        
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH , 20, scale_x, scale_y))
    elif form == 7 : #right corridor only
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH  , 20, scale_x, scale_y))# Top
        # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT, scale_x, scale_y))
        #left gate gap   
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT -320, scale_x, scale_y))  # Right
        walls.add(Wall(ROOM_WIDTH+x-20, y - 50 +  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x +680,  y+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x + 680,  y+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate3 = Gate(x-20+ROOM_WIDTH ,y - 50 +  ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate3)
        
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH , 20, scale_x, scale_y))  # Bottom
    elif form == 8  : 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH  , 20, scale_x, scale_y))# Top
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT, scale_x, scale_y))
            
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT -320, scale_x, scale_y))  # Right
        walls.add(Wall(ROOM_WIDTH+x-20, y - 50 +  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x +680,  y+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x + 680,  y+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate3 = Gate(x-20+ROOM_WIDTH ,y - 50 +  ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate3)
        
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y))  # Bottom
        walls.add(Wall(x - 50 + 500, y+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20, scale_x, scale_y)) 

        walls.add(Wall(x + ROOM_WIDTH- 450,y + 20-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall(x + ROOM_WIDTH- 250,y+ 20-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - bottom 
        
        
        Gate4 = Gate(x -50 + ROOM_WIDTH-400 ,y-50+ 30+ROOM_HEIGHT, 220  , 20 ,   "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate4)
    elif form == 9 : # left and right corridor only
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH  , 20, scale_x, scale_y))# Top
        # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT - 320, scale_x, scale_y))  # Left
        walls.add(Wall(x, (y-50)+ ROOM_HEIGHT - 150 ,  20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x - 180, (y-50)+ 50+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate2 = Gate(x,(y-50) + ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate2)
        #left gate gap 
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT -320, scale_x, scale_y))  # Right
        walls.add(Wall(ROOM_WIDTH+x-20, y - 50 +  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x +680,  y+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x + 680,  y+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
         
        Gate3 = Gate(x-20+ROOM_WIDTH ,y - 50 +  ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate3)
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH , 20, scale_x, scale_y))#
        
    elif form == 10 :
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 450,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall((x-50)+50 + ROOM_WIDTH- 250,(y-50)+ 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - top 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
        walls.add(Wall((x-50)+500, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
         
         
        Gate1 = Gate((x-50)+ROOM_WIDTH - 400,(y-50) +  50, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate1)
       
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT, scale_x, scale_y))  # Left
           
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT, scale_x, scale_y)) 
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH , 20, scale_x, scale_y))  # Bottom
        
    elif form == 11 : # top   ,  right  
        walls.add(Wall((x-50)+50 + ROOM_WIDTH - 450, (y-50) + 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y))
        walls.add(Wall((x-50)+50 + ROOM_WIDTH - 250, (y-50) + 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320, scale_x, scale_y)) # - top 
        walls.add(Wall((x-50)+50, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
        walls.add(Wall((x-50)+500, 50 + (y-50), ROOM_WIDTH - 450 , 20, scale_x, scale_y))# Top
         
         
        Gate1 = Gate((x-50)+ROOM_WIDTH - 400,(y-50) +  50, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        walls.add(Gate1)
        # top gate gap 
        
        walls.add(Wall(x ,  y ,  20 ,  ROOM_HEIGHT, scale_x, scale_y))  # Left
           
        
        walls.add(Wall(x+ROOM_WIDTH-20, y, 20, ROOM_HEIGHT -320, scale_x, scale_y))  # Right
        walls.add(Wall(ROOM_WIDTH+x-20, y - 50 +  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300, scale_x, scale_y))
        walls.add(Wall(x +680,  y+ROOM_HEIGHT-320 , 200, 20, scale_x, scale_y))
        walls.add(Wall(x + 680,  y+ROOM_HEIGHT-320 + 100 , 200, 20, scale_x, scale_y))
        
        Gate3 = Gate(x-20+ROOM_WIDTH ,y - 50 +  ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)
        
        walls.add(Gate3)
        
        walls.add(Wall(x, y+ROOM_HEIGHT-20, ROOM_WIDTH, 20, scale_x, scale_y))  # Bottom
       
    for _ in range(2):
            q = random.randint(int((x+50 +100) ), int((x+50  + ROOM_WIDTH -300)))
            w = random.randint(int((y+50  + 100)),int( (y+50 + ROOM_HEIGHT -300) ))
        
            
            if random.random() > 0.5:
                walls.add(Wall(q, w, random.randint(50, 150), 20, scale_x , scale_y))
            else:
                walls.add(Wall(q, w, 20, random.randint(50, 150), scale_x , scale_y) )
    return walls

# First boss
def generate_boss_room(x, y, scale_x=1, scale_y=1):
    walls = pygame.sprite.Group()
    floors = pygame.sprite.Group()

    room_width = 900
    room_height = 700
    wall_thickness = 20

    # Main walls
    walls.add(Wall(x, y, room_width, wall_thickness, scale_x, scale_y))  # top
    walls.add(Wall(x, y + room_height - wall_thickness, room_width, wall_thickness, scale_x, scale_y))  # bottom
    walls.add(Wall(x + room_width - wall_thickness, y, wall_thickness, room_height, scale_x, scale_y))  # right

    # Entrance cutout (corridor)
    corridor_height = 120
    corridor_top = y + (room_height - corridor_height) // 2
    corridor_bottom = corridor_top + corridor_height
    walls.add(Wall(x, y, wall_thickness, corridor_top - y, scale_x, scale_y))
    walls.add(Wall(x, corridor_bottom, wall_thickness, y + room_height - corridor_bottom, scale_x, scale_y))

    # Floor
    floors.add(Floor(x * scale_x, y * scale_y, scale_x=scale_x * (900 / ROOM_WIDTH), scale_y=scale_y * (700 / ROOM_HEIGHT)))






    # Walls inside
    center_x = x + room_width // 2
    center_y = y + room_height // 2
    walls.add(Wall(center_x - 200, center_y - 100, 50, 50, scale_x, scale_y))
    walls.add(Wall(center_x + 200, center_y, 50, 50, scale_x, scale_y))
    gate = Gate(x, y + 300, 20, 100, "images/Gate_Open.png", "images/Gate_Closed.png", scale_x, scale_y)

    gate.toogle(walls)
    walls.add(gate)

    return walls, floors, (center_x * scale_x, center_y * scale_y), gate



