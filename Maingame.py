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



class Tear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.orig = pygame.image.load('images/Soldier.png').convert_alpha()
        self.image = pygame.transform.scale(self.orig , (10,10))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.direction = direction
        self.lifetime = 1
        
    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.lifetime -= 1
        return self.lifetime <= 0


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image_orig = pygame.image.load("images/Wall.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image_orig,(w,h))
        
        self.rect = self.image.get_rect(topleft=(x, y))

# Room generation
def generate_room():
    walls = pygame.sprite.Group()
    
    # Outer walls
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
    if enemies_counter <= 0 :
        enemies_counter = int(random.uniform(0,6))
        for _ in range(enemies_counter):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            enemies.add(Enemy(x, y))
    # Shooting (mouse)
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left click
        mx, my = pygame.mouse.get_pos()
        dx = mx - player.rect.centerx
        dy = my - player.rect.centery
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        player.shoot((dx/dist, dy/dist))
    
    # Update
    player.update(walls)
    enemies.update(player, walls)
    
    # Update tears
    for tear in player.tears[:]:
        if tear.update():
            player.tears.remove(tear)
        else:
            # Tear-enemy collision
            for enemy in enemies:
                if tear.rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if tear in player.tears:
                        player.tears.remove(tear)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        enemies_counter -=1
                    break
    
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
