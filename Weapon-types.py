import pygame
import time
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Конфигурация режимов стрельбы
FIRE_MODES = {
    1: {"speed": 7, "damage": 10, "fire_rate": 0.3},  # обычный
    2: {"speed": 12, "damage": 5, "fire_rate": 0.1},  # быстрый
    3: {"speed": 5, "damage": 20, "fire_rate": 0.6},  # мощный
}

current_mode = 1
last_shot_time = 0

# Группа пуль
bullets = pygame.sprite.Group()

class Tear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=7, damage=10):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('images/bullet.png').convert_alpha(), (20, 20)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = direction
        self.lifetime = 50
        self.damage = damage

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

running = True
while running:
    dt = clock.tick(60) / 1000  # Время между кадрами в секундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Переключение режимов
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_mode = 1
            elif event.key == pygame.K_2:
                current_mode = 2
            elif event.key == pygame.K_3:
                current_mode = 3

    # Проверка зажатия ЛКМ
    mouse_buttons = pygame.mouse.get_pressed()
    current_time = time.time()
    mode = FIRE_MODES[current_mode]

   
    bullets.update()
    screen.fill((30, 30, 30))
    bullets.draw(screen)
    pygame.display.flip()

