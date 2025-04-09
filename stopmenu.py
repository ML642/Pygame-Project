import pygame
import random
import math
from player import Player
from enemy import Enemy
import os 

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 40)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    clicked = False
    button_rect = pygame.Rect(x, y, width, height)
    
    # Hover effect
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            clicked = True
    else:
        pygame.draw.rect(screen, color, button_rect)
    
    # Button text
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    return clicked

def pause_menu():
    global paused, running
    
    while paused:
        screen.fill(BLUE)
        
        # Draw menu title
        title = font.render("PAUSED", True, WHITE)
        screen.blit(title, (350, 200))
        
        # Resume button
        if draw_button("Resume", 300, 300, 200, 50, GREEN, (100, 255, 100)):
            paused = False
        
        # Quit button
        if draw_button("Quit", 300, 370, 200, 50, RED, (255, 100, 100)):
            if confirm_quit():
                running = False
                paused = False
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

def confirm_quit():
    confirm = False
    while True:
        screen.fill(BLACK)
        
        # Draw confirmation message
        message = font.render("Quit Game? (Y/N)", True, WHITE)
        screen.blit(message, (300, 250))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False