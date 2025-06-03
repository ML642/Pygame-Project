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


    def pickup(self, player , Fire_Modes ):
        if self.drop_type == "hp": # Health type, there is no "ammo" type, it spawn itself automatically, because we have no munition system.
            player.health = min(player.health + 50, player.max_health)
        else:
            for fire_mode in Fire_Modes.values():
                if fire_mode.get("full") is not None:
                    fire_mode["ammo"] += fire_mode["full"]
                else:
                    fire_mode["ammo"] += 1

             
        self.kill()
        return Fire_Modes 