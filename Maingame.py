import pygame
import random
import math
from player import Player
from enemy import Enemy
from camera import Camera

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
camera = Camera(800,600 , 2000,2000)

ROOM_WIDTH, ROOM_HEIGHT = 700, 500
CELL_SIZE = 40

floors = pygame.sprite.Group()
kills = 0



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
        
floors.add(Floor(50,50))
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
    
    
    
    Gate1 = Gate(ROOM_WIDTH - 400, 50, 250, 20, "images/Gate_Open.png", "images/Gate_Closed.png")
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
    
    Gate3 = Gate(30+ROOM_WIDTH , ROOM_HEIGHT-270  , 20  , ROOM_HEIGHT-320, "images/Gate_Open.png", "images/Gate_Closed.png")
    
    walls.add(Gate3)
    
    walls.add(Wall(50, 50+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20))  # Bottom
    walls.add(Wall(500, 50+ROOM_HEIGHT-20, ROOM_WIDTH - 450, 20)) 

    walls.add(Wall(50 + ROOM_WIDTH- 450, 70-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320))
    walls.add(Wall(50 + ROOM_WIDTH- 250, 70-(ROOM_HEIGHT-320)+640  ,20 , ROOM_HEIGHT-320)) # - bottom 
    
    
    Gate4 = Gate(ROOM_WIDTH-400 , 30+ROOM_HEIGHT, 250  , 20 ,   "images/Gate_Open.png", "images/Gate_Closed.png")
  
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


player = Player()
walls = generate_room()
enemies = pygame.sprite.Group()
enemies_counter = 0
copy = walls.copy()
spawn_delay = 5000 
last_spawn_time = 0

running = True
stop = False 
# ... (keep all your previous code until the main loop)

running = True
stop = False 
while running:
    if stop == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Game logic updates
        if enemies_counter > 0:
            for wall in walls:
                if isinstance(wall, Gate) and wall.is_open:
                    wall.toogle(walls)
        
        if enemies_counter <= 0: 
            for wall in walls:
                if isinstance(wall, Gate) and not wall.is_open:
                    wall.toogle(walls)

        if enemies_counter <= 0 and pygame.time.get_ticks() - last_spawn_time > spawn_delay:
            enemies_counter = random.randint(1, 6)
            enemies_to_spawn = enemies_counter
            last_spawn_time = pygame.time.get_ticks()
            
            while enemies_to_spawn > 0:
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                enemy = Enemy(x, y)
                
                if not any(enemy.rect.colliderect(wall.rect) for wall in walls):
                    enemies.add(enemy)
                    enemies_to_spawn -= 1

        # Player input and updates
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click
    # Get mouse position in WORLD coordinates
          mouse_world_x = pygame.mouse.get_pos()[0] - camera.camera.x
          mouse_world_y = pygame.mouse.get_pos()[1] - camera.camera.y
    
    # Calculate direction relative to player's WORLD position
          dx = mouse_world_x - player.rect.centerx
          dy = mouse_world_y - player.rect.centery
          dist = max(1, math.sqrt(dx*dx + dy*dy))
          player.shoot((dx/dist, dy/dist))
        player.update(walls)
        camera.update(player)

       
        screen.fill(BLACK)
        for tear in player.tears[:]:
         if tear.update():
            if tear in player.tears:
                player.tears.remove(tear)
         else:
            for enemy in enemies:
                if tear.rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if tear in player.tears:
                        player.tears.remove(tear)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        kills +=1 
                        enemies_counter -=1
                    break
        
        for floor in floors:
            screen.blit(floor.image, camera.apply(floor))

        
       
        
        for wall in walls:
            screen.blit(wall.image, camera.apply(wall))

        
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy))

        
        screen.blit(player.image, camera.apply(player))

        # Draw tears with camera offset
        for tear in player.tears:
            adjusted_pos = tear.rect.topleft + pygame.math.Vector2(camera.camera.topleft)
            screen.blit(tear.image, adjusted_pos)

        # Collision detection and game logic
        enemies.update(player, walls)
        
        for tear in player.tears[:]:
            tear.update()
            for wall in walls:
                if tear.rect.colliderect(wall.rect):
                    player.tears.remove(tear)
                    break

        # Health and UI elements (drawn without camera offset)
        font = pygame.font.SysFont(None, 36)
        health_text = font.render(f"Hearts: {int(player.health)}", True, WHITE)
        coordinates  = font.render(f"Player coordinates: X  {int(player.rect.x)} Y  {int(player.rect.y)}", True, WHITE)
        
        screen.blit(health_text, (20, 20))
        screen.blit(coordinates, (20, 50))
        if player.health <= 1:
            pygame.quit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
