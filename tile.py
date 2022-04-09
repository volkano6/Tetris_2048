import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
import random
from point import Point


# Class used for modeling numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and size used for displaying the tile number
    font_family, font_size = "Courier", 16

    # Constructor that creates a tile with 2 as the number on it
    def __init__(self):

        self.position = Point()
        self.position.x = None
        self.position.y = None

        random_list = [2, 4]
        x = random.choice(random_list)
        if x == 2:
            # set the number on the tile
            self.number = 2
            # set the colors of the tile
            self.background_color = Color(249, 246, 242)  # background (tile) color
            self.foreground_color = Color(0, 0, 0)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        else:
            # set the number on the tile
            self.number = 4
            # set the colors of the tile
            self.background_color = Color(237, 224, 200)  # background (tile) color
            self.foreground_color = Color(0, 0, 0)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

    def tile_value_for_merge(self, value):

        if value == 4:
            # set the number on the tile
            self.number = 4
            # set the colors of the tile
            self.background_color = Color(237, 224, 200)  # background (tile) color
            self.foreground_color = Color(0, 0, 0)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 8:
            # set the number on the tile
            self.number = 8
            # set the colors of the tile
            self.background_color = Color(242, 177, 121)  # background (tile) color
            self.foreground_color = Color(255, 255, 255)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 16:
            # set the number on the tile
            self.number = 16
            # set the colors of the tile
            self.background_color = Color(245, 149, 99)  # background (tile) color
            self.foreground_color = Color(255, 255, 255)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 32:
            # set the number on the tile
            self.number = 32
            # set the colors of the tile
            self.background_color = Color(246, 124, 95)  # background (tile) color
            self.foreground_color = Color(255, 255, 255)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 64:
            # set the number on the tile
            self.number = 64
            # set the colors of the tile
            self.background_color = Color(246, 94, 59)  # background (tile) color
            self.foreground_color = Color(255, 255, 255)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 128:
            # set the number on the tile
            self.number = 128
            # set the colors of the tile
            self.background_color = Color(237, 207, 114)  # background (tile) color
            self.foreground_color = Color(255, 255, 255)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 256:
            # set the number on the tile
            self.number = 256
            # set the colors of the tile
            self.background_color = Color(237, 204, 97)  # background (tile) color
            self.foreground_color = Color(255, 255, 255)  # foreground (number) color
            self.box_color = Color(187, 173, 160)  # box (boundary) color

        elif value == 512:
            # set the number on the tile
            self.number = 512
            # set the colors of the tile
            self.background_color = Color(100, 190, 200)  # background (tile) color
            self.foreground_color = Color(192, 192, 192)  # foreground (number) color
            self.box_color = Color(0, 0, 128)  # box (boundary) color

        elif value == 1024:
            # set the number on the tile
            self.number = 1024
            # set the colors of the tile
            self.background_color = Color(100, 190, 200)  # background (tile) color
            self.foreground_color = Color(192, 192, 192)  # foreground (number) color
            self.box_color = Color(0, 0, 128)  # box (boundary) color

        elif value == 2048:
            # set the number on the tile
            self.number = 2048
            # set the colors of the tile
            self.background_color = Color(100, 190, 200)  # background (tile) color
            self.foreground_color = Color(192, 192, 192)  # foreground (number) color
            self.box_color = Color(0, 0, 128)  # box (boundary) color

    def merge_tile_color(self, a):

        value = int(a)

        if value == 4:
            # set the number on the tile
            self.number = 4
            # set the colors of the tile
            self.background_color = Color(145, 196, 131)  # background (tile) color
            self.foreground_color = None  # foreground (number) color
            self.box_color = Color(145, 196, 131)  # box (boundary) color

        elif value == 8:
            # set the number on the tile
            self.number = 8
            # set the colors of the tile
            self.background_color = Color(145, 196, 131)  # background (tile) color
            self.foreground_color = Color(238, 238, 238)  # foreground (number) color
            self.box_color = Color(145, 196, 131)  # box (boundary) color

        stddraw.show(300)



    def move(self, dx, dy):
        self.position.translate(dx, dy)

    # Method for drawing the tile
    def draw(self, position, length=1):
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        # draw the bounding box around the tile as a square
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.boldText(position.x, position.y, str(self.number))
