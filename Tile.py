import constants as con
import pygame
import os

TILESIZE = 128


class Tile:
    TILESIZE = 128

    def __init__(self, id, x, y, kind_of_tile):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.kind_of_tile = kind_of_tile
        # ----
        if kind_of_tile == 2: filename = con.TWO
        elif kind_of_tile == 4 : filename = con.FOUR
        elif kind_of_tile == 8: filename = con.EIGHT
        elif kind_of_tile == 16: filename = con.SIXTEEN
        elif kind_of_tile == 0: filename = con.ZERO
        elif kind_of_tile == 32: filename = con.THIRTY_TWO
        elif kind_of_tile == 64: filename = con.SIXTY_FOUR
        elif kind_of_tile == 64: filename = con.SIXTY_FOUR
        elif kind_of_tile == 128: filename = con.HOUNDRED
        elif kind_of_tile == 256: filename = con.TWO_HOUNDRED
        elif kind_of_tile == 512: filename = con.FIVE_HOUNDRED
        elif kind_of_tile == 1024: filename = con.THOUSAND
        elif kind_of_tile == 2048: filename = con.TWO_THOUSAND

        else: raise ValueError("Error! kind of tile: ", kind_of_tile)
        # ---------------------
        self.rect = pygame.Rect(self.x * TILESIZE, self.y * TILESIZE, TILESIZE, TILESIZE)
        image_path = os.path.join("data", "images")

        self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()

        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))



    def debug_print(self):
        s = "id: {}, x: {}, y: {}, kind: {}"
        s = s.format(self.id, self.x, self.y, self.kind_of_tile)
        print(s)
