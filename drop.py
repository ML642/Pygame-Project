import pygame

class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y, drop_type):
        super().__init__()
        self.drop_type = drop_type
        if self.drop_type == "hp":
            self.image = pygame.image.load('images/HPDrop.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        else:
            self.image = pygame.image.load('images/SDrop.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))


    def pickup(self, player):
        if self.drop_type == "hp": # Health type, there is no "ammo" type, it spawn itself automatically, because we have no munition system.
            player.health = min(player.health + 20, player.max_health)
        else:
            pass
        self.kill()