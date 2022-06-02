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
    flying_players = sprites.SpriteSheet("assets/$euphus_young_fly.png")

    layout = sprites.Layout(STARTING_LAYOUT, players, screen, 50, 76, flying_players)

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
    flying_players = sprites.SpriteSheet("assets/$euphus_young_fly.png")
    explosion_sheet = sprites.SpriteSheet("assets/explosion.png")
    explosion_group = pygame.sprite.Group()
    layout = sprites.Layout(LAYOUT, players, screen, 50, 76, flying_players)

    previous_movement = pygame.time.get_ticks()
    tree_game = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(bg_image, (0, 0))

        score = sprites.Score(FONT, screen, layout.collied()[2], 50, 20)

        layout.update(screen, previous_movement)

        score.draw_score()

        if layout.collied()[0]:
            running = False
        tree_game = layout.collied()[3]

        pygame.display.flip()

        clock.tick(FPS)

        if tree_game:
            running = False

    return tree_game


def play_tree():
    bg_image = pygame.image.load("assets/maxresdefault.jpg")
    bg_image = pygame.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Bird Run")
    players = sprites.SpriteSheet("assets/$euphus_young_fly.png")
    flying_players = sprites.SpriteSheet("assets/$euphus_young_fly.png")

    layout = sprites.Layout(LAYOUT, players, screen, 76, 50, flying_players)

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

        start_text = BIG_FONT.render("THE", True, BLACK)
        start_text_2 = BIG_FONT.render("FOREST", True, BLACK)
        start_text_3 = FONT.render("press \"p\" to start", True, WHITE)
        screen.blit(start_text, (200, 400))
        screen.blit(start_text_2, (740, 400))
        screen.blit(start_text_3, (550, 800))

        pygame.display.flip()
        clock.tick(FPS)


start_screen()
if play():
    play_tree()
    game_over()

while True:
    play()
    game_over()

pygame.quit()
