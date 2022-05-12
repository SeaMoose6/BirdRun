import pygame
import sprites
from settings import *

pygame.init()

bg_image = pygame.image.load("assets/background_no_signs.png")
bg_image = pygame.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Bird Run")

clock = pygame.time.Clock()
running = True
players = sprites.SpriteSheet("assets/$euphus_young.png")
explosion_sheet = sprites.SpriteSheet("assets/explosion.png")
explosion_group = pygame.sprite.Group()
layout = sprites.Layout(players, screen, explosion_sheet)

previous_movement = pygame.time.get_ticks()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_image, (0, 0))

    layout.update(screen, previous_movement)
    if layout.collied()[0]:
        explosion = sprites.Explosion(explosion_sheet, layout.collied()[1])
        explosion_group.add(explosion)

    #explosion_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
