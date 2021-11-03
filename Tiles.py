
# --------------------------------------------------------
#                   class Tiles
# --------------------------------------------------------
import Tile

class Tiles:
    def __init__(self, screen, tiles_arr):
        self.screen = screen
        self.inner = []
        self.current_tile = None
        self.tiles_arr = tiles_arr
        self._load_data()

    def _load_data(self):
        self.inner = []
        id = 0
        for count_i, i in enumerate(self.tiles_arr):
            for count_j, j in enumerate(i):
                new_tile = Tile.Tile(id, count_j, count_i, j)
                self.inner.append(new_tile)
                id += 1
    def update_inner(self):
        self.inner = []
        id = 0
        for count_i, i in enumerate(self.tiles_arr):
            for count_j, j in enumerate(i):
                new_tile = Tile.Tile(id, count_j, count_i, j)
                self.inner.append(new_tile)
                id += 1

    def get_tile(self, x, y):
        for elem in self.inner:
            if elem.x == x:
                if elem.y == y:
                    return elem
        return None

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Doh! There are no tiles to display. 😕")
        for elem in self.inner:
            self.screen.blit(elem.image, elem.rect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()
