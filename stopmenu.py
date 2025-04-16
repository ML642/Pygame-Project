import pygame
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pause Menu Test")
font = pygame.font.SysFont("Arial", 40)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

running = True
paused = False
volume = 0.5

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return clicked

def draw_slider(x, y, width, height, value):
    global volume
    pygame.draw.rect(screen, DARK_GRAY, (x, y + height // 2 - 5, width, 10))
    handle_x = x + int(width * value)
    handle_rect = pygame.Rect(handle_x - 10, y, 20, height)
    pygame.draw.rect(screen, GREEN, handle_rect)

    if pygame.mouse.get_pressed()[0]:
        if pygame.Rect(x, y, width, height).collidepoint(pygame.mouse.get_pos()):
            mouse_x = pygame.mouse.get_pos()[0]
            volume = min(1.0, max(0.0, (mouse_x - x) / width))
    return volume

def pause_menu():
    global paused, running

    while paused:
        screen.fill(BLUE)
        title = font.render("PAUSED", True, WHITE)
        screen.blit(title, (330, 100))

        # Buttons
        if draw_button("Resume", 300, 200, 200, 50, GREEN, (100, 255, 100)):
            paused = False

        if draw_button("Quit", 300, 270, 200, 50, RED, (255, 100, 100)):
            if confirm_quit():
                running = False
                paused = False

        # Volume slider
        screen.blit(font.render("Volume", True, WHITE), (330, 360))
        draw_slider(300, 400, 200, 30, volume)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

def confirm_quit():
    while True:
        screen.fill(BLACK)
        message = font.render("Quit Game?", True, WHITE)
        screen.blit(message, (300, 200))

        if draw_button("Yes", 250, 300, 100, 50, RED, (255, 100, 100)):
            return True
        if draw_button("No", 450, 300, 100, 50, GREEN, (100, 255, 100)):
            return False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

#Main game loop
clock = pygame.time.Clock()

# while running:
#     screen.fill((30, 30, 30))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 paused = True
#                 pause_menu()

#     # Display the current volume
#     vol_display = font.render(f"Volume: {round(volume * 100)}%", True, WHITE)
#     screen.blit(vol_display, (250, 280))

#     info = font.render("Running game... Press ESC to pause", True, WHITE)
#     screen.blit(info, (120, 350))

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
