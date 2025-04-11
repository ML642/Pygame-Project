import pygame 
import random 

ROOM_WIDTH, ROOM_HEIGHT = 700, 500

class Floor (pygame.sprite.Sprite) : 
    def __init__ (self, x , y): 
        super().__init__()
        try :
            self.image_orig = pygame.image.load("images/Floor.png").convert_alpha()
            self.image = pygame.transform.scale(self.image_orig , (ROOM_WIDTH,ROOM_HEIGHT))
        except :
            self.image = pygame.Surface((50, 50))
            self.image.fill((100, 100, 100))
        
        self.rect = self.image.get_rect(topleft=(x,y))
        


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image_orig = pygame.image.load("images/Wall.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image_orig,(w,h))
        
        self.rect = self.image.get_rect( topleft=(x, y) )

class Gate(Wall):
        def __init__(self, x, y, w, h, open_image_path, closed_image_path):
            super().__init__(x, y, w, h)
            self.open_image = pygame.image.load(open_image_path).convert_alpha()
            self.open_image = pygame.transform.scale(self.open_image, (w, h))
            self.closed_image = pygame.image.load(closed_image_path).convert_alpha()
            self.closed_image = pygame.transform.scale(self.closed_image, (w, h))
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
def generate_room():
    walls = pygame.sprite.Group()
    
    walls.add(Wall(50 + ROOM_WIDTH- 450, 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320))
    walls.add(Wall(50 + ROOM_WIDTH- 250, 70-(ROOM_HEIGHT-320)  ,20 , ROOM_HEIGHT-320)) # - top 
    walls.add(Wall(50, 50, ROOM_WIDTH - 450 , 20))# Top
    walls.add(Wall(500, 50, ROOM_WIDTH - 450 , 20))# Top
    
    
    
    Gate1 = Gate(ROOM_WIDTH - 400, 50, 220, 20, "images/Gate_Open.png", "images/Gate_Closed.png")
    walls.add(Gate1)
    # top gate gap 
    
    walls.add(Wall(50, 50, 20, ROOM_HEIGHT-320))  # Left
    walls.add(Wall(50,  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300))
    walls.add(Wall(50 - 180,  50+ROOM_HEIGHT-320 , 200, 20 ))
    walls.add(Wall(50 - 180,  50+ROOM_HEIGHT-320 + 100 , 200, 20 ))
    
    Gate2 = Gate(50, ROOM_HEIGHT - 270, 20, 120, "images/Gate_Open.png", "images/Gate_Closed.png")
    walls.add(Gate2)
    #left gate gap 
    
    walls.add(Wall(50+ROOM_WIDTH-20, 50, 20, ROOM_HEIGHT -320))  # Right
    walls.add(Wall(ROOM_WIDTH+30,  ROOM_HEIGHT - 150 , 20 , ROOM_HEIGHT-300))
    walls.add(Wall(50 +680,  50+ROOM_HEIGHT-320 , 200, 20 ))
    walls.add(Wall(50 + 680,  50+ROOM_HEIGHT-320 + 100 , 200, 20 ))
    
    Gate3 = Gate(30+ROOM_WIDTH , ROOM_HEIGHT-270  , 20  , 120, "images/Gate_Open.png", "images/Gate_Closed.png")
    
    walls.add(Gate3)
    
    walls.add(Wall(50, 50+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20))  # Bottom
    walls.add(Wall(500, 50+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20)) 

    walls.add(Wall(50 + ROOM_WIDTH- 450, 70-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320))
    walls.add(Wall(50 + ROOM_WIDTH- 250, 70-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320)) # - bottom 
    
    
    Gate4 = Gate(ROOM_WIDTH-400 , 30+ROOM_HEIGHT, 220  , 20 ,   "images/Gate_Open.png", "images/Gate_Closed.png")
  
    walls.add(Gate4)
    
    # Inner walls (random)
    for _ in range(5):
        x = random.randint(100, 600)
        y = random.randint(100, 400)
        if random.random() > 0.5:
            walls.add(Wall(x, y, random.randint(50, 150), 20))
        else:
            walls.add(Wall(x, y, 20, random.randint(50, 150)))
    return walls
