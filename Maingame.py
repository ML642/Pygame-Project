import pygame
import random
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Isaac-like Prototype")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Game states
ROOM_WIDTH, ROOM_HEIGHT = 700, 500
CELL_SIZE = 40

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(400, 300))
        self.speed = 5
        self.health = 3
        self.shot_cooldown = 0
        self.tears = []  # Projectiles
        
    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]: dx -= self.speed
        if keys[pygame.K_RIGHT]: dx += self.speed
        if keys[pygame.K_UP]: dy -= self.speed
        if keys[pygame.K_DOWN]: dy += self.speed
        
        # Diagonal movement normalization
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071
        
        # Wall collision
        new_rect = self.rect.copy()
        new_rect.x += dx
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dx = 0
                break
                
        new_rect = self.rect.copy()
        new_rect.y += dy
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dy = 0
                break
                
        self.rect.x += dx
        self.rect.y += dy
        
        # Shooting cooldown
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            
    def shoot(self, direction):
        if self.shot_cooldown == 0:
            tear = Tear(self.rect.centerx, self.rect.centery, direction)
            self.tears.append(tear)
            self.shot_cooldown = 15

# Tears (projectiles)
class Tear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.direction = direction
        self.lifetime = 60
        
    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.lifetime -= 1
        return self.lifetime <= 0

# Enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1
        self.health = 2
        
    def update(self, player, walls):
        # Simple AI: move toward player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        dx, dy = dx/dist, dy/dist
        
        # Wall collision
        new_rect = self.rect.copy()
        new_rect.x += dx * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dx = 0
                break
                
        new_rect = self.rect.copy()
        new_rect.y += dy * self.speed
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                dy = 0
                break
                
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Walls
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(WHITE)
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

# Game setup
player = Player()
walls = generate_room()
enemies = pygame.sprite.Group()
for _ in range(5):
    x = random.randint(100, 700)
    y = random.randint(100, 500)
    enemies.add(Enemy(x, y))

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
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
                    break
    
    # Player-enemy collision
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.health -= 0.1  # Gradual damage
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw grid (optional)
    for x in range(50, 750, CELL_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 50), (x, 550))
    for y in range(50, 550, CELL_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (50, y), (750, y))
    
    walls.draw(screen)
    enemies.draw(screen)
    for tear in player.tears:
        screen.blit(tear.image, tear.rect)
    screen.blit(player.image, player.rect)
    
    # UI
    font = pygame.font.SysFont(None, 36)
    health_text = font.render(f"Hearts: {int(player.health)}", True, WHITE)
    screen.blit(health_text, (20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()