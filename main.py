import pygame
import sprites
from settings import *

pygame.init()

bg_image = pygame.image.load("assets/background-1 (1).png")
bg_image = pygame.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Bird Run")

clock = pygame.time.Clock()
running = True
players = sprites.SpriteSheet("assets/$euphus_young.png")
layout = sprites.Layout(players, screen)

previous_movement = pygame.time.get_ticks()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))

    layout.update(screen, previous_movement)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
