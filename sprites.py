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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sheet, center):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = sheet
        self.EXPLOSION_LIST = [self.sheet.image_at((0, 0, 31, 31), -1), self.sheet.image_at((32, 0, 31, 31), -1),
                               self.sheet.image_at((65, 0, 31, 31), -1), self.sheet.image_at((96, 0, 31, 31), -1),
                               self.sheet.image_at((128, 0, 31, 31), -1), self.sheet.image_at((160, 0, 31, 31), -1)]
        self.EXPLOSION_LIST = [pygame.transform.scale2x(explosion) for explosion in self.EXPLOSION_LIST]
        self.image = self.EXPLOSION_LIST[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 50
        self.kill_center = center
        self.previous_update = pygame.time.get_ticks()

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.previous_update > self.frame_rate:
            self.previous_update = current
            self.frame += 1
        elif self.frame == len(self.EXPLOSION_LIST):
            self.kill()
        else:
            self.image = self.EXPLOSION_LIST[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.kill_center



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet, running, display):
        pygame.sprite.Sprite.__init__(self)
        self.surface = sheet.image_at((0, 95, 47, 47), -1)
        self.surface = pygame.transform.scale(self.surface, (250, 250))
        self.image = self.surface
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.run = [sheet.image_at((10, 110, 32, 30), -1), sheet.image_at((57, 110, 32, 30), -1)]
        self.run = [pygame.transform.scale(player, (150, 150)) for player in self.run]
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
        self.image.fill(BLUE)
        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def get_keys(self, time):
        self.time = time
        keys = pygame.key.get_pressed()
        self.current_move = pygame.time.get_ticks()
        if self.current_move - self.time > move_delay:
            self.time = self.current_move

            if keys[pygame.K_s] and self.rect.y < 636:
                self.rect.y += 65
            if keys[pygame.K_w] and self.rect.y > 180:
                self.rect.y -= 65
        #print(self.rect.y)


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, display, color, speed):
        pygame.sprite.Sprite.__init__(self)
        self.red_car = pygame.image.load("assets/red car.png")
        self.teal_car = pygame.image.load("assets/teal car.png")
        self.white_car = pygame.image.load("assets/truckFlat.png")
        self.violet_car = pygame.image.load("assets/van.png")
        self.yellow_car = pygame.image.load("assets/taxi.png")
        self.cop_car = pygame.image.load("assets/police.png")
        self.fast_car = pygame.image.load("assets/raceFuture.png")
        self.health_car = pygame.image.load("assets/ambulance.png")
        self.rect = self.red_car.get_rect()
        self.speed = speed
        if color == "R":
            self.image = self.red_car
        if color == "T":
            self.image = self.teal_car
        if color == "W":
            self.image = self.white_car
        if color == "V":
            self.image = self.violet_car
        if color == "Y":
            self.image = self.yellow_car
        if color == "C":
            self.image = self.cop_car
        if color == "F":
            self.image = self.fast_car
        if color == "H":
            self.image = self.health_car
        self.rect.x = x
        self.rect.y = y
        self.display = display

    def update(self):
        self.rect.x -= self.speed
        #self.image.fill(RED)
        self.display.blit(self.image, (self.rect.x, self.rect.y))


class Layout:
    def __init__(self, sheet, display, sheet_2):
        pygame.sprite.Sprite.__init__(self)
        self.layout = LAYOUT
        self.display = display
        self.player_grp = pygame.sprite.GroupSingle()
        self.car_grp = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * TILE_SIZE
                y_val = i * 75

                if col == "P":
                    player = Player(x_val, y_val, sheet, True, self.display)
                    self.player_grp.add(player)
                if col == "R":
                    car = Car(x_val, y_val, self.display, col, 22)
                    self.car_grp.add(car)
                if col == "T":
                    car = Car(x_val, y_val, self.display, col, 18)
                    self.car_grp.add(car)
                if col == "W":
                    car = Car(x_val, y_val, self.display, col, 15)
                    self.car_grp.add(car)
                if col == "V":
                    car = Car(x_val, y_val, self.display, col, 12)
                    self.car_grp.add(car)
                if col == "Y":
                    car = Car(x_val, y_val, self.display, col, 15)
                    self.car_grp.add(car)
                if col == "C":
                    car = Car(x_val, y_val, self.display, col, 28)
                    self.car_grp.add(car)
                if col == "F":
                    car = Car(x_val, y_val, self.display, col, 35)
                    self.car_grp.add(car)
                if col == "H":
                    car = Car(x_val, y_val, self.display, col, 8)
                    self.car_grp.add(car)

    def update(self, display, time):
        for sprite in self.all_sprites.sprites():
            display.blit(sprite.surface, sprite.rect)
        for player in self.player_grp.sprites():
            player.update()
            player.get_keys(time)
        for car in self.car_grp.sprites():
            car.update()

        #self.collied()

    def collied(self):
        touched = False
        player = self.player_grp.sprite

        collide_list = pygame.sprite.spritecollide(player, self.car_grp, False)
        if collide_list:
            touched = True
            player.rect.y += 2000
            print("YEH")
        return touched, player.rect.center


