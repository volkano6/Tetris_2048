import numpy

import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from tile import Tile

from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for modelling the game grid
def print_score():
    stddraw.setPenColor(stddraw.GRAY)
    stddraw.boldText(14, 19, "SCORE")


# draw next tetromino on the right bottom of game grid.
def show_next_tetromino(arr):
    # draw title
    stddraw.boldText(13.8, 5, "NEXT TETROMINO")
    arr[0].draw_next_tetromino()


class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the te1tromino that is currently being moved on the game grid
        self.current_tetromino = None
        self.tetromino_list = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(42, 69, 99)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.002
        self.box_thickness = 2 * self.line_thickness

    def merge(self):

        tiles = self.find_all_tiles_position()

        for tile in reversed(range(len(tiles))):  # Tileler arasında büyükten küçüğe dolaş
            # sıradaki tile path
            current_tile = self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x]
            # eğer ilk satırda değilsek devam et
            if current_tile.position.y != 0:
                # current tilenin altındaki tile pathı
                bottom_tile = self.tile_matrix[tiles[tile].position.y - 1][tiles[tile].position.x]
                # eğer none değilse konum ataması yap
                if bottom_tile is not None:
                    # Alttaki cell boş orayı tail ile doldururuz
                    bottom_tile.position = Point()
                    bottom_tile.position.x = current_tile.position.x
                    bottom_tile.position.y = current_tile.position.y
                    bottom_tile.position.y -= 1

                    # eğer numberları aynı ise merge işlemini gerçekleştir
                    if current_tile.number == bottom_tile.number:
                        bottom_tile.tile_value_for_merge(current_tile.number + bottom_tile.number)
                        self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x] = None
                        #self.delete_tiles_2048()

    def drop_tiles_2048(self):

        tiles = self.find_all_tiles_position()
        tiles_can_move_down = []

        for tile in range(len(tiles)):
            # tiles_can_move_down nın içi koşullara göre doldu
            if (self.tile_matrix[tiles[tile].position.y - 1][tiles[tile].position.x] is None) and (tiles[tile].position.y != 0) and (self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x - 1] is None) and (self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x + 1] is None):
                tiles_can_move_down.append(self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x])



            # for tile_in_move_list in range(len(tiles_can_move_down)):
            #     stop = (self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y - 1][tiles_can_move_down[tile_in_move_list].position.x] is not None) or (tiles_can_move_down[tile_in_move_list].position.y != 0) or (self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x - 1] is not None) or (self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x + 1] is not None)
            #     while stop:
            #         drop_tile = self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x]
            #         self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y - 1][tiles_can_move_down[tile_in_move_list].position.x] = drop_tile
            #         self.tile_matrix[tiles_can_move_down[tile_in_move_list].position.y][tiles_can_move_down[tile_in_move_list].position.x] = None
            #
            #         break

    def delete_tiles_2048(self):

        tiles = self.find_all_tiles_position()
        tiles_can_move_down = []

        for tile in range(len(tiles)):
            # tiles_can_move_down nın içi koşullara göre doldu
            if (self.tile_matrix[tiles[tile].position.y - 1][tiles[tile].position.x] is None) and \
                    (tiles[tile].position.y != 0) and \
                    (self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x - 1] is None) and \
                    (self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x + 1] is None):
                tiles_can_move_down.append(self.tile_matrix[tiles[tile].position.y][tiles[tile].position.x])

        for del_tiles in range(len(tiles_can_move_down)):
            self.tile_matrix[tiles_can_move_down[del_tiles].position.y][tiles_can_move_down[del_tiles].position.x] = None







        # for x in range(len(tiles_can_move_down)):
        #     print(tiles_can_move_down[x].position)
        # print("---------")
        # print("---------")

    def piece_drop(self):
        while self.current_tetromino.can_be_moved("down", self):
            self.current_tetromino.bottom_left_cell.y -= 1

    # Write commend
    def clear_full_lines(self):
        for row in range(self.grid_height):
            full_cell = 0
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:
                    full_cell += 1
                if full_cell >= 12:
                    for row2 in range(self.grid_width):
                        self.tile_matrix[row][row2] = None
                    self.drop_tiles_tetris(row)

    def drop_tiles_tetris(self, upThisrRow):

        tiles = self.find_all_tiles_position(upThisrRow)

        # ANA MATRİKSTEKİ TİLELERİN KONUMUNU BİRER AŞAĞI İNDİRİR
        for value in range(len(tiles)):
            a = self.tile_matrix[tiles[value].position.y][tiles[value].position.x]
            self.tile_matrix[tiles[value].position.y - 1][tiles[value].position.x] = a
            self.tile_matrix[tiles[value].position.y][tiles[value].position.x] = None

    def find_all_tiles_position(self, upThisrRow=0):
        tiles = []
        tiles_position = []

        # SİLİNEN KISMIN ÜST TARAFINDAKİ TİLE VE KONUMLARI BULUR VE TİLE ARRAYINE EKLER
        for row in range(upThisrRow, self.grid_height):
            for col in range(self.grid_width):
                if self.is_occupied(row, col):
                    tiles.append(self.tile_matrix[row][col])
                    cell_point = Point()
                    cell_point.x = col
                    cell_point.y = row
                    tiles_position.append(cell_point)
        for current_tile in range(len(tiles)):
            tiles[current_tile].position.x = tiles_position[current_tile].x
            tiles[current_tile].position.y = tiles_position[current_tile].y

        return tiles


    def tile_array_to_binary(self):
        (row,column)=self.tile_matrix.shape
        tile_arr_binary = np.full((row,column),0)
        for i in range(row):
            for j in (range(column)):
                if self.tile_matrix[i][j] != None:
                    tile_arr_binary[i][j]=1

        return tile_arr_binary

    def connected_component(self,binarized):
        max_label = int(100000)
        row = binarized.shape[0]
        column = binarized.shape[1]

        # create a new array that will hold the labels and that has the same shape with the binarized array
        im = np.full(shape=(row, column), dtype=int, fill_value=max_label)

        # create an label holder array
        a = np.arange(0, max_label, dtype=int)

        k = 0
        # start labeling by checking connected tiles
        for i in range(1, row - 1):
            for j in range(1, column - 1):
                # get the related tiles
                c = binarized[i][j]
                label_u = im[i - 1][j]
                label_l = im[i][j - 1]

                # check if the tile exists
                if c == 1:
                    # get the minimum labeled tile around the current one
                    min_label = min(label_u, label_l)

                    # if the minimum labeled tile has the maximum label value, give it a temp value
                    # else, update the array with the label
                    if min_label == max_label:  # u = l = 0
                        k += 1
                        im[i][j] = k
                    else:
                        im[i][j] = min_label
                        if min_label != label_u and label_u != max_label:
                            self.update_labeled_array(a, min_label, label_u)

                        if min_label != label_l and label_l != max_label:
                            self.update_labeled_array(a, min_label, label_l)

        # initialize an array for labels
        labels = []

        # final reduction in the label array, also add the labels into the label list
        for i in range(k + 1):
            index = i
            while a[index] != index:
                index = a[index]
            a[i] = a[index]
            labels.append(a[i])

        # Removes duplicates drom the list
        labels = list(dict.fromkeys(labels))
        labels.pop(0)

        # second pass to resolve labels
        for i in range(row):
            for j in range(column):
                if binarized[i][j] == 1 and im[i][j] != max_label:
                    im[i][j] = a[im[i][j]]
                else:
                    im[i][j] = 0

        print(im)
        print(labels)
        # return the labeled array, label list
        return im, len(labels)

    def update_labeled_array(self, a, label1, label2):
        index = lab_small = lab_large = 0
        if label1 < label2:
            lab_small = label1
            lab_large = label2
        else:
            lab_small = label2
            lab_large = label1
        index = lab_large
        while index > 1 and a[index] != lab_small:
            if a[index] < lab_small:
                temp = index
                index = lab_small
                lab_small = a[temp]
            elif a[index] > lab_small:
                temp = a[index]
                a[index] = lab_small
                index = temp
            else:
                break

    # Method used for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()

        # draw SCORE board
        print_score()
        # draw next tetromino
        show_next_tetromino(self.tetromino_list)

        self.merge()

        self.connected_component(self.tile_array_to_binary())

        self.clear_full_lines()

        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(300)

    # Method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over



