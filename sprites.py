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
    def __init__(self, x, y, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.surface = sheet.image_at((0, 95, 47, 47), -1)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.run = [sheet.image_at((0, 95, 47, 47), -1), sheet.image_at((47, 95, 47, 47), -1)]
        self.running = False
        self.dodging_up = False
        self.dodging_down = False



class Layout:
    def __init__(self, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.layout = LAYOUT
        self.player_grp = pygame.sprite.GroupSingle()
        self.all_sprites = pygame.sprite.Group()

        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * 81 + 50

                if col == "P":
                    player = Player(x_val, y_val, sheet)
                    print(player.rect.x, player.rect.y)
                    self.player_grp.add(player)
                    self.all_sprites.add(player)

    def update(self, display):
        for sprite in self.all_sprites.sprites():
            display.blit(sprite.surface, sprite.rect)
            #print(sprite.rect.x, sprite.rect.y)
