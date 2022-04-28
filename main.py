import pygame
import sprites
from settings import *

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("The Beach")

clock = pygame.time.Clock()
running = True
players = sprites.SpriteSheet("assets/$euphus_young.png")
layout = sprites.Layout(players)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    layout.update(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
