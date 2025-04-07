import pygame
import random
import math
from player import Player
from enemy import Enemy


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

ROOM_WIDTH, ROOM_HEIGHT = 700, 500
CELL_SIZE = 40

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image_orig = pygame.image.load("images/Wall.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image_orig,(w,h))
        
        self.rect = self.image.get_rect(topleft=(x, y))

def generate_room():
    walls = pygame.sprite.Group()
    
    walls.add(Wall(50, 50, ROOM_WIDTH, 20))  # Top
    walls.add(Wall(50, 50, 20, ROOM_HEIGHT))  # Left
    walls.add(Wall(50, 50+ROOM_HEIGHT-20, ROOM_WIDTH, 20))  # Bottom
    walls.add(Wall(50+ROOM_WIDTH-20, 50, 20, ROOM_HEIGHT))  # Right
    
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
    #when there are no enemies adds more 
    if enemies_counter <= 0:
            enemies_counter = random.randint(1, 6) 
            enemies_to_spawn = enemies_counter
            
            while enemies_to_spawn > 0:
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                enemy = Enemy(x, y)
                
                # Check collision with all walls
                collision = False
                for wall in walls:
                    if enemy.rect.colliderect(wall.rect):
                        collision = True
                        break  
                
                if not collision:
                    enemies.add(enemy)
                    enemies_to_spawn -= 1
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left click
        mx, my = pygame.mouse.get_pos()
        dx = mx - player.rect.centerx
        dy = my - player.rect.centery
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        player.shoot((dx/dist, dy/dist))
    
   
    player.update(walls)
    enemies.update(player, walls)
    

    for tear in player.tears[:]:
        if tear.update():
            player.tears.remove(tear)
        else:
            for enemy in enemies:
                if tear.rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if tear in player.tears:
                        player.tears.remove(tear)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        enemies_counter -=1
                    break
    for tear in player.tears[:] : 
        for wall in walls : 
           if tear.rect.colliderect(wall.rect) : 
               player.tears.remove(tear)
    
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.health -= 0.1 
   
    
    screen.fill(BLACK)
    
    for x in range(50, 750, CELL_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 50), (x, 550))
    for y in range(50, 550, CELL_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (50, y), (750, y))
    
    walls.draw(screen)
    enemies.draw(screen)
    for tear in player.tears:
        screen.blit(tear.image, tear.rect)
    screen.blit(player.image, player.rect)
    
    
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Hearts: {int(player.health)}", True, WHITE)
    screen.blit(health_text, (20, 20))
    if player.health <= 1 : 
        pygame.quit()   
  if stop == True : 
      {}
  pygame.display.flip()
  clock.tick(60)

pygame.quit()
