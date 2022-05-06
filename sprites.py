import pygame
from settings import *


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
            y_margin=0, y_padding=0, width=None, height=None, colorkey = None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                    - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                    - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, running, display):
        pygame.sprite.Sprite.__init__(self)
        self.surface = sheet.image_at((0, 95, 47, 47), -1)
        self.surface = pygame.transform.scale(self.surface, (250, 250))
        self.image = self.surface
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.run = [sheet.image_at((0, 95, 47, 47), -1), sheet.image_at((47, 95, 47, 47), -1)]
        self.run = [pygame.transform.scale(player, (250, 250)) for player in self.run]
        self.frame = 0
        self.frame_rate = 50
        self.previous_update = pygame.time.get_ticks()
        self.image_delay = 100
        self.running = running
        self.dodging_up = False
        self.dodging_down = False
        self.display = display

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.previous_update >= self.image_delay:
            self.previous_update = now
            if self.frame >= len(self.run):
                self.frame = 0
            self.image = self.run[self.frame]
            self.frame = self.frame + 1
        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def get_keys(self, time):
        self.time = time
        keys = pygame.key.get_pressed()
        self.current_move = pygame.time.get_ticks()
        if self.current_move - self.time > move_delay:
            self.time = self.current_move

            if keys[pygame.K_s] and self.rect.y < 564:
                self.rect.y += 65
            if keys[pygame.K_w] and self.rect.y > 150:
                self.rect.y -= 65
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, display):
        pygame.sprite.Sprite.__init__(self)
        self.red_car = pygame.image.load("assets/sedanSports_S.png")
        self.rect = self.red_car.get_rect()
        self.image = self.red_car
        self.rect.x = x
        self.rect.y = y
        print(x, y)
        display.blit(self.image, (self.rect.x, self.rect.y))





class Layout:
    def __init__(self, sheet, display):
        pygame.sprite.Sprite.__init__(self)
        self.layout = LAYOUT
        self.display = display
        self.player_grp = pygame.sprite.GroupSingle()
        self.car_grp = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * 75 - 6

                if col == "P":
                    player = Player(x_val, y_val, sheet, True, self.display)
                    self.player_grp.add(player)
                if col == "C":
                    car = Car(x_val, y_val, self.display)
                    self.car_grp.add(car)
                    #self.all_sprites.add(car)



    def update(self, display, time):
        for sprite in self.all_sprites.sprites():
            display.blit(sprite.surface, sprite.rect)
        for player in self.player_grp.sprites():
            player.update()
            player.get_keys(time)
