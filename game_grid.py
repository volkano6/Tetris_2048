import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
import copy

from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for modelling the game grid


# draw next tetromino on the right bottom of game grid.
def show_next_tetromino(arr):
    # draw title
    stddraw.setFontSize(17)
    stddraw.boldText(14.1, 9, "NEXT TETROMINOS")

    stddraw.setPenRadius(0.01)
    stddraw.setPenColor(Color(201, 201, 201))
    stddraw.rectangle(12, 5.4, 4.2, 3.2)
    arr[0].draw_next_tetromino(12.6, 6)

    stddraw.setPenRadius(0.01)
    stddraw.setPenColor(Color(201, 201, 201))
    stddraw.rectangle(12, 1.4, 4.2, 3.2)

    arr[1].draw_next_tetromino(12.6, 2)


def show_options():
    stddraw.setFontSize(16)
    stddraw.boldText(14.1, 15, "Press 'R' to Restart")
    stddraw.boldText(14.1, 14, "Press 'E' to Exit")
    stddraw.boldText(14.1, 13, "Press 'P' to Pause")

    stddraw.setPenRadius(0.01)
    stddraw.setPenColor(Color(201, 201, 201))
    stddraw.rectangle(12, 12.4, 4.2, 3.2)


class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # score
        self.total_score = 0
        self.delay_game = 220
        self.delay_merge_and_clear_row = 20
        # create the te1tromino that is currently being moved on the game grid
        self.current_tetromino = None
        self.tetromino_list = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(238, 238, 238)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(221, 221, 221)
        self.boundary_color = Color(201, 201, 201)
        # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.008
        self.box_thickness = 1.5 * self.line_thickness

    def merge(self):
        score = 0
        # satır sütun dolaşır
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # alt alta olan satırlar
                current_tile = self.tile_matrix[row][col]
                bottom_current_tile = self.tile_matrix[row - 1][col]

                if self.tile_matrix[row - 1][col] is not None and self.tile_matrix[row][col] is not None:

                    # eğer numberları aynı ise merge işlemini gerçekleştir.
                    if current_tile.number == bottom_current_tile.number:

                        sum = current_tile.number + bottom_current_tile.number
                        score = self.tile_matrix[row][col].number + self.tile_matrix[row - 1][col].number
                        stddraw.show(self.delay_merge_and_clear_row)
                        bottom_current_tile.tile_value_for_merge(sum)
                        self.tile_matrix[row][col] = None
                        self.total_score += score

                        # method is droped same colm with merging
                        self.after_merge_col_drop(row, col)

                        # Labeling in here
                    label_arr, equivalency_list = self.label_array(self.tile_array_to_binary())

                    self.drop_labeling_tiles(label_arr, equivalency_list)

    def print_score(self):

        stddraw.setPenColor(Color(201, 201, 201))
        stddraw.setPenRadius(0.01)
        stddraw.rectangle(12, 17.3, 4.2, 2)
        stddraw.setPenColor(stddraw.BLACK)

        stddraw.setFontSize(21)
        stddraw.boldText(14.1, 18.8, "SCORE")
        stddraw.boldText(14.1, 18, str(self.total_score))

    # Method used for displa ying the game grid
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
        self.print_score()
        # draw next tetromino
        show_next_tetromino(self.tetromino_list)
        show_options()

        self.merge()

        self.clear_full_lines()

        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(self.delay_game)

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
        pos_x, pos_y = -0.5, -0.52
        stddraw.rectangle(pos_x, pos_y, self.grid_width + 0.04, self.grid_height)
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

    def is_inside_for_tile(self, row, col):
        if row < 1 or row >= self.grid_height - 1:
            return False
        if col < 1 or col >= self.grid_width - 1:
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

    def after_merge_col_drop(self, row, col):

        control_row_count = self.grid_height - (row + 1)

        for current_tile in range(1, control_row_count):
            if self.tile_matrix[row + current_tile][col] is not None:
                a = self.tile_matrix[row + current_tile][col]
                self.tile_matrix[row + current_tile - 1][col] = a
                self.tile_matrix[row + current_tile][col] = None
                stddraw.show(self.delay_merge_and_clear_row)

    def tile_array_to_binary(self):
        # get the shape of the tile matrix
        (nrows, ncols) = self.tile_matrix.shape

        # create a new array filled with zeros that has the 2 more columns and 3 more rows
        arr = np.full((nrows + 3, ncols + 2), 0)

        # make a base line filled with ones to understand the tiles that are connected to bottom
        arr[1] = np.full((1, ncols + 2), 1)
        arr[1][0] = 0
        arr[1][ncols + 1] = 0

        # make the non-empty cells one
        for i in range(nrows):
            for j in range(ncols):
                if self.tile_matrix[i][j] != None:
                    arr[i + 2][j + 1] = 1

        # return binarized array
        return arr

    # Method for labeling the binarized tile matrix to distinguish the tiles that are not connected to the bottom
    # of the matrix
    def label_array(self, binarized):
        max_label = int(10000)
        nrow = binarized.shape[0]
        ncol = binarized.shape[1]

        # create a new array that will hold the labels and that has the same shape with the binarized array
        im = np.full(shape=(nrow, ncol), dtype=int, fill_value=max_label)

        # create an label holder array
        a = np.arange(0, max_label, dtype=int)

        k = 0
        # start labeling by checking connected tiles
        for i in range(1, nrow - 1):
            for j in range(1, ncol - 1):
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
        for i in range(nrow):
            for j in range(ncol):
                if binarized[i][j] == 1 and im[i][j] != max_label:
                    im[i][j] = a[im[i][j]]
                else:
                    im[i][j] = 0

        # resize array
        im_origin = np.delete(im, 0, 0)
        im_origin_2 = np.delete(im_origin, 0, 0)
        im_origin_3 = np.delete(im_origin_2, len(im_origin_2) - 1, 0)
        im_origin_4 = np.delete(im_origin_3, 0, 1)
        im_origin_5 = np.delete(im_origin_4, len(im_origin_2[0]) - 2, 1)

        # return the labeled array, label list
        return im_origin_5, labels

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

    def drop_labeling_tiles(self, array_with_label, count_of_label):

        # count of label in içinde gezer
        for x in range(1, len(count_of_label)):

            # matrikste gezer
            for row in range(1, len(array_with_label)):
                for col in range(len(array_with_label[0])):

                    if array_with_label[row][col] == count_of_label[x]:
                        a = self.tile_matrix[row][col]
                        self.tile_matrix[row - 1][col] = a
                        self.tile_matrix[row][col] = None

    def piece_drop(self):
        while self.current_tetromino.can_be_moved("down", self):
            self.current_tetromino.bottom_left_cell.y -= 1

    # Write commend
    def clear_full_lines(self):

        score = 0
        # satır sütun dolaşır
        for row in range(1, self.grid_height):
            full_cell = 0
            for col in range(self.grid_width):

                if self.tile_matrix[row][col] is not None:
                    full_cell += 1
                    score += self.tile_matrix[row][col].number
                else:
                    score = 0

                if full_cell >= self.grid_width:
                    for row2 in range(self.grid_width):
                        self.tile_matrix[row][row2] = None
                        stddraw.show(self.delay_merge_and_clear_row )
                    self.total_score += score
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

    def labeling_matrix(self, arr):

        label_array = copy.deepcopy(arr)
        for x in range(label_array.shape[1]):
            label_array[0][x] = 0

        # find image size
        img_height = label_array.shape[0]
        img_width = label_array.shape[1]

        background = 0
        curr_object = 0
        equivalency_list = {}

        # iterate through pixels and assign classifications
        for a in range(1, img_height):
            for b in range(1, img_width):
                if label_array[a][b] != background:

                    if a > 0:
                        # look at pixel above
                        pixel_above = label_array[a - 1][b]

                    if b > 0:
                        # look at pixel before
                        pixel_before = label_array[a][b - 1]

                    if pixel_above != background and pixel_before != background:
                        classification = min(pixel_above, pixel_before)
                        equivalency_list[max(pixel_above, pixel_before)] = classification
                    elif pixel_above != background:
                        classification = pixel_above
                    elif pixel_before != background:
                        classification = pixel_before
                    else:
                        # assign a new label
                        curr_object += 1
                        equivalency_list[curr_object] = curr_object
                        classification = curr_object

                    label_array[a][b] = classification

        # update classifications based on equivalency list
        for a in range(img_height):
            for b in range(img_width):
                if label_array[a][b] != background:
                    new_value = equivalency_list[label_array[a][b]]
                    label_array[a][b] = new_value

        print("New Image: " + str(label_array))
        print("Equivalency List: " + str(equivalency_list))
        return label_array, equivalency_list
