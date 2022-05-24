import pygame as pg
import sprites
from settings import *

pygame.init()


def start_screen():
    bg_image = pg.image.load("assets/background_no_signs.png")
    bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Space Pirates")
    players = sprites.SpriteSheet("assets/$euphus_young.png")

    layout = sprites.Layout(STARTING_LAYOUT, players, screen)

    clock = pygame.time.Clock()

    previous_movement = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False

        screen.blit(bg_image, (0, 0))

        layout.update(screen, previous_movement)

        start_text = BIG_FONT.render("BIRD", True, BLACK)
        start_text_2 = BIG_FONT.render("RUN", True, BLACK)
        start_text_3 = FONT.render("press \"p\" to start", True, WHITE)
        screen.blit(start_text, (200, 400))
        screen.blit(start_text_2, (740, 400))
        screen.blit(start_text_3, (550, 800))

        pygame.display.flip()

        clock.tick(FPS)


def game_over():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Bird Run")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False

        screen.fill(BLACK)
        text = BIG_FONT.render(f"GAME OVER", True, RED)
        text_2 = FONT.render(f"Score:{SCORE}", True, WHITE)
        screen.blit(text, (300, 400))
        screen.blit(text_2, (560, 600))

        start_text_3 = FONT.render("press \"p\" to play again", True, WHITE)
        screen.blit(start_text_3, (500, 700))

        pygame.display.flip()
        clock.tick(FPS)

def play():
    bg_image = pygame.image.load("assets/background_no_signs.png")
    bg_image = pygame.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Bird Run")

    clock = pygame.time.Clock()
    running = True
    players = sprites.SpriteSheet("assets/$euphus_young.png")
    explosion_sheet = sprites.SpriteSheet("assets/explosion.png")
    explosion_group = pygame.sprite.Group()
    layout = sprites.Layout(LAYOUT, players, screen)

    previous_movement = pygame.time.get_ticks()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(bg_image, (0, 0))

        score = sprites.Score(FONT, screen, layout.collied()[2], 50, 20)

        layout.update(screen, previous_movement)
        if layout.collied()[0]:
            explosion = sprites.Explosion(explosion_sheet, layout.collied()[1])
            explosion_group.add(explosion)

        score.draw_score()
        #print(score)

        pygame.display.flip()

        clock.tick(FPS)


start_screen()

while True:
    play()
    game_over()

pygame.quit()
