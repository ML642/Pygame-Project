import pygame


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_x, scale_y):
        super().__init__()
        self.image = pygame.image.load("images/portal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80 * scale_x, 80 * scale_y))
        self.rect = self.image.get_rect(center=(x, y))
        self.used = False
