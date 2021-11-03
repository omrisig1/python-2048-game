
import pygame
import os
import sys

import constants as con
import random
import copy
import Tile
import Tiles

TITLE = "2048"
TILES_HORIZONTAL = 4
TILES_VERTICAL = 4
TILESIZE = 128
WINDOW_WIDTH = (TILESIZE * TILES_HORIZONTAL)+135
WINDOW_HEIGHT = (TILESIZE * TILES_VERTICAL)

# --------------------------------------------------------
#                   class Game
# --------------------------------------------------------

class Game:

    def __init__(self):
        self.game_arr = self.initialize_board()
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.BG_COLOR = con.LIGHTGREY
        self.keep_looping = True
        # ----
        self.tiles = Tiles.Tiles(self.surface, self.game_arr)
        self.myfont = pygame.font.SysFont("monospace", 40)
        self.gameWon = False
        self.playGoal= 512

    def initialize_board(self):
        self.grids = []
        board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        i = random.choice([0, 1, 2, 3])
        j = random.choice([0, 1, 2, 3])
        board[i][j] = 2
        self.grids = [copy.deepcopy(board)]
        return board

    def events(self):
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_DOWN:
                    self.game_arr = self.changeRowDown(self.game_arr)
                elif event.key == pygame.K_UP:
                    self.game_arr = self.changeRowUp(self.game_arr)
                elif event.key == pygame.K_RIGHT:
                    self.game_arr = self.changeRowRight(self.game_arr)
                elif event.key == pygame.K_LEFT:
                    self.game_arr = self.changeRowLeft(self.game_arr)

                self.tiles.tiles_arr = self.game_arr
                self.gameWon = self.isGameWon(self.tiles.tiles_arr)
                temp_grid = copy.deepcopy(self.tiles.tiles_arr)
                game_in_progress = self.checkAvailableMove(temp_grid)
                if game_in_progress:
                    self.tiles.tiles_arr = self.addNewRandomCell(self.tiles.tiles_arr)
                    self.tiles.update_inner()
                else:
                    label = self.myfont.render("No More Moves, Restarting", True, (255, 0, 0))
                    self.surface.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    self.restartGame()
                history_grid = copy.deepcopy(self.tiles.tiles_arr)
                self.grids.append(history_grid)


    def promtGameWon(self):
        label = self.myfont.render("You Won, Restarting..", True, (255, 0, 0))
        self.surface.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(2000)
        self.restartGame()

    def restartGame(self):
        print('restarting')
        self.game_arr = self.initialize_board()
        self.tiles.tiles_arr = self.game_arr
        self.tiles.update_inner()
        pygame.display.update()

    def isGameWon(self, grid):
        for i in (grid):
            for j in (i):
                if j == self.playGoal:
                    return True
        return False

    def array_compare(self, grid1, grid2):
        for index_i,i in enumerate(grid1):
            for index_j, j in enumerate(i):
                if grid2[index_i][index_j] != j:
                    return False
        return True

    def checkAvailableMove(self, grid):
        temp_grid = copy.deepcopy(grid)
        changed_grid = self.changeRowLeft(grid)

        if (not self.array_compare(temp_grid, changed_grid)):
            return True
        changed_grid = self.changeRowRight(grid)

        if (not self.array_compare(temp_grid, changed_grid)):
            return True
        changed_grid = self.changeRowUp(grid)
        if (not self.array_compare(temp_grid, changed_grid)):
            return True
        changed_grid = self.changeRowDown(grid)
        if (not self.array_compare(temp_grid, changed_grid)):
            return True
        return False

    def pringrid(self, grid):
        for i in grid:
            print(i)

    def addNewRandomCell(self, grid):
        empty_cells = []
        for index_i, i in enumerate(grid):
            for index_j, j in enumerate(i):
                if j == 0:
                    empty_cells.append([index_i, index_j])
        if empty_cells:
            index = random.choice(empty_cells)
            options = self.getGridOptions(grid)
            list = []
            for k in options:
                list.append(k)
            value = random.choice(list)
            grid[index[0]][index[1]] = value
        return grid

    def getGridOptions(self, grid):
        max = 2
        for i in (grid):
            for j in (i):
                if j != 0:
                    if j > max:
                        max = j
        options = [2]
        index = 4
        if max > 16:
            max = 32
        while index < max:
            options.append(index)
            index *= 2
        return options

    def changeRowDown(self, grid):
        # premanary work: move all and ignore zeroes
        for i in range(3, -1, -1):
            index = 3
            for j in range(3, -1, -1):
                # print(grid[j][i])
                if grid[j][i] != 0:
                    if index == j:
                        index -= 1
                        continue
                    grid[index][i] = grid[j][i]
                    index -= 1
                    grid[j][i] = 0

        # start from the end of the row
        # for each row:
        for row_number in range(0, 4):
            for i in range(3, -1, -1):
                if grid[i][row_number] != 0 and grid[i][row_number] == grid[i - 1][row_number]:
                    # we have a match:
                    grid[i][row_number] *= 2
                    grid[i - 1][row_number] = 0

                    # print(grid[j][i])
                    i = row_number
                    index = 3
                    for j in range(3, -1, -1):
                        # print(grid[j][i])
                        if grid[j][i] != 0:
                            if index == j:
                                index -= 1
                                continue
                            grid[index][i] = grid[j][i]
                            index -= 1
                            grid[j][i] = 0

                    for i in range(3, -1, -1):
                        index = 3
                        for j in range(3, -1, -1):
                            # print(grid[j][i])
                            if grid[j][i] != 0:
                                if index == j:
                                    index -= 1
                                    continue
                                grid[index][i] = grid[j][i]
                                index -= 1
                                grid[j][i] = 0

                    # last cell set as 0
        return grid

    def changeRowUp(self, grid):
        # premanary work: move all and ignore zeroes
        for i in range(0, 4):
            index = 0
            for j in range(0, 4):
                # print(grid[j][i])
                if grid[j][i] != 0:
                    if index == j:
                        index += 1
                        continue
                    grid[index][i] = grid[j][i]
                    index += 1
                    grid[j][i] = 0
        # start from the end of the row
        # for each row:
        for row_number in range(0, 4):

            for i in range(0, 3):
                if grid[i][row_number] != 0 and grid[i][row_number] == grid[i + 1][row_number]:
                    # we have a match:
                    grid[i][row_number] *= 2
                    grid[i + 1][row_number] = 0
                    # print(grid[j][i])
                    i = row_number
                    index = 0
                    for j in range(0, 4):
                        # print(grid[j][i])
                        if grid[j][i] != 0:
                            if index == j:
                                index += 1
                                continue
                            grid[index][i] = grid[j][i]
                            index += 1
                            grid[j][i] = 0

                    # last cell set as 0
        return grid

    def changeRowRight(self, grid):
        # premanary work: move all and ignore zeroes
        for row in range(3, -1, -1):
            index = 3
            for i in range(3, -1, -1):
                if grid[row][i] != 0:
                    if index == i:
                        index -= 1
                        continue
                    grid[row][index] = grid[row][i]
                    index -= 1
                    grid[row][i] = 0

        # start from the end of the row
        # for each row:
        for row_number in range(0, 4):
            for i in range(3, 0, -1):
                if grid[row_number][i] != 0 and grid[row_number][i] == grid[row_number][i - 1]:
                    # we have a match:
                    grid[row_number][i] *= 2
                    for index in range(i - 1, 0, -1):  # move cells right
                        grid[row_number][index] = grid[row_number][index - 1]
                    # last cell set as 0
                    grid[row_number][0] = 0
        return grid

    def changeRowLeft(self, grid):
        # start from the start of the row
        # premanary work: move all and ignore zeroes
        for row in range(0, 4):
            index = 0
            for i in range(0, 4):
                if grid[row][i] != 0:
                    if index == i:
                        index += 1
                        continue
                    grid[row][index] = grid[row][i]
                    index += 1
                    grid[row][i] = 0

        # for each row:
        for row_number in range(0, 4):
            for i in range(0, 3):
                if grid[row_number][i] == grid[row_number][i + 1]:
                    # we have a match:
                    grid[row_number][i] *= 2
                    for index in range(i + 1, 3):  # move cells left
                        grid[row_number][index] = grid[row_number][index + 1]
                    # last cell set as 0
                    grid[row_number][3] = 0
        return grid

    def update(self):
        pass

    def draw(self):
        self.surface.fill(self.BG_COLOR)
        self.tiles.draw(self.surface)
        self.button('UNDO MOVE', 515, 80, 130, 20, (255, 0, 0), (124, 252, 0), self.undoMove)

        self.button('Play Till 16', 515, 115, 130, 20, (255, 0, 0), (124, 252, 0), self.Goal16)

        self.button('Play Till 32', 515, 140, 130, 20, (255, 0, 0), (124, 252, 0), self.Goal32)
        self.button('Play Till 256', 515, 165, 130, 20, (255, 0, 0), (124, 252, 0), self.Goal256)
        self.button('Play Till 512', 515, 190, 130, 20, (255, 0, 0), (124, 252, 0), self.Goal512)
        self.button('Play Till 1024', 515, 215, 130, 20, (255, 0, 0), (124, 252, 0), self.Goal1024)
        self.button('Play Till 2048', 515, 240, 130, 20, (255, 0, 0), (124, 252, 0), self.Goal2048)

        pygame.time.wait(70)
        self.smallfont = pygame.font.SysFont("monospace", 12)
        label2 = self.smallfont.render("Playing till " + str(self.playGoal), True, (255, 0, 0))
        self.surface.blit(label2, (515, 10))
        pygame.display.update()


    def Goal16(self):
        self.playGoal = 16
        self.restartGame()
    def Goal32(self):
        self.playGoal = 32
        self.restartGame()
    def Goal256(self):
        self.playGoal = 256
        self.restartGame()
    def Goal512(self):
        self.playGoal = 512
        self.restartGame()
    def Goal1024(self):
        self.playGoal = 1024
        self.restartGame()
    def Goal2048(self):
        self.playGoal = 2048
        self.restartGame()

    def undoMove(self):
        if self.grids is not None and len(self.grids) != 0:
            if len(self.grids) == 1:
                previous_grid = copy.deepcopy(self.grids[0])
            else:
                self.grids.pop()
                previous_grid = copy.deepcopy(self.grids[-1])
            self.game_arr = previous_grid
            self.tiles.tiles_arr = previous_grid
            self.tiles.update_inner()
            pygame.display.update()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surface, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()

        else:
            pygame.draw.rect(self.surface, ic, (x, y, w, h))

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurface = smallText.render(msg, True, (0, 0, 0))
        textSurf, textRect = textSurface, textSurface.get_rect()
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.surface.blit(textSurf, textRect)

    def main(self):

        while self.keep_looping:
            self.events()
            self.update()
            self.draw()
            if self.gameWon:
                self.promtGameWon()
                self.gameWon = False


if __name__ == "__main__":
    mygame = Game()
    mygame.main()