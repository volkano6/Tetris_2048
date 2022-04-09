import game_grid
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  #used for creating tetrominoes with random types/shapes


# MAIN FUNCTION OF THE PROGRAM
# -----------------------------------------------------------------------------------
# Main function where this program  starts execution

def create_canvas():

    # set the dimensions  of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 50 * grid_h, 60 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.6, grid_w + 4.7)
    stddraw.setYscale(-0.6, grid_h - 0.4)

    display_game_menu(grid_h, grid_w + 5)


def start():
    grid_h, grid_w = 20, 12
    # set the dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

    # create the game grid
    grid = GameGrid(grid_h, grid_w)

    # created list ("tetromino_list") for tetrominoes
    # When the "current_tetromino" is done None, new tetromino takes in "tetromino_list"
    tetromino_list = [create_tetromino(grid_h, grid_w),
                      create_tetromino(grid_h, grid_w),
                      create_tetromino(grid_h, grid_w)]
    # tetromino list is entered the game grid
    grid.tetromino_list = tetromino_list

    # first tetromino is entered the game grid
    # by using the create_tetromino function defined below
    current_tetromino = tetromino_list[0]
    grid.current_tetromino = current_tetromino

    # First value of "tetromino_list" is used. This part update tetrominoes list.
    tetromino_list.pop(0)
    tetromino_list.append(create_tetromino(grid_h, grid_w))

    score_array = [0]

    # display a simple menu before opening    game
    # by using the display_game_menu function defined below

    clock_direction = True
    # the main game loop (keyboard interaction for moving the tetromino)

    while True:

        # check user interactions via the keyboard
        if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            # if the left arrow key has been pressed
            if key_typed == "left":
                # move the active tetromino left by one
                current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
            elif key_typed == "right":
                # move the active tetromino right by one
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the active tetromino down by one
                # (soft drop: causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid)
            elif key_typed == "left ctrl":
                # move the active tetromino down to deepest
                if clock_direction:
                    clock_direction = False
                else:
                    clock_direction = True
            elif key_typed == "up":
                # move the active tetromino's rotate change
                grid.current_tetromino.rotate_tertromino(grid, clock_direction)
            # clear the queue of the pressed keys for a smoother interaction
            elif key_typed == "space":
                # move the active tetromino drop
                # (drop: causes the tetromino to fall to the deepest place )
                grid.piece_drop()
            #if user typed 'r', the game restart
            if key_typed == 'p':
                display_pause(grid_h,grid_w)
            if key_typed == 'r':
                start()
            if key_typed == 'e':
                display_game_over(grid_h,grid_w,score_array)
            # clear the queue of the pressed keys for a smoother interaction
            stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
        success = current_tetromino.move("down", grid)
        # place the active tetromino on the grid when it cannot go down anymore
        if not success:


            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)

            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over
            if game_over:
                score_array.pop(0)
                score_array.append(grid.total_score)

                break

            # create the next tetromino to enter the game grid
            # by using the crea  te_tetromino function defined below
            current_tetromino = tetromino_list[0]
            grid.current_tetromino = current_tetromino

            # First value of "tetromino_list" is used. This part update tetrominoes list.
            tetromino_list.pop(0)
            tetromino_list.append(create_tetromino(grid_h, grid_w))


        score_array.pop(0)
        score_array.append(grid.total_score)
        # display the game grid and the current tetromino
        grid.display()
    # print a message on the console when the game is over
    display_game_over(grid_h, grid_w, score_array)
    print("Game over")

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    # colors used for the menu
    background_color = Color(221,221,221)
    button_color = Color(201,201,201)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 5, 1.7
    # coordinates of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the button
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game

def display_game_over(grid_height, grid_width,arr):

    grid = GameGrid(grid_height, grid_width)
    background_color = Color(221,221,221)
    button_color = Color(201,201,201)
    text_color = Color(0,0,0)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/game_over4.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width+3.7) / 2, grid_height - 6
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 3.8, 1.5
    # coordinate display_game_overs of the bottom left corner of the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 5
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Helvetica")
    stddraw.setFontSize(35)
    stddraw.setPenColor(text_color)
    text_to_display = "PLAY AGAIN"
    stddraw.text(img_center_x, 5.8, text_to_display)
    stddraw.setFontSize(50)
    stddraw.boldText(grid_width-4, 10, "SCORE")
    stddraw.boldText(grid_width-4, 9, str(arr[0]))
    # menu interaction loop

    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the button
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    start()  # break the loop to end

def display_pause(grid_height, grid_width):
    grid = GameGrid(grid_height, grid_width)
    button_color = Color(201,201,201)
    text_color = Color(255,255,255)
    # clear the background canvas to background_color
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/pause.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width+4) / 2, grid_height - 9
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 7, 1.3
    # coordinate display_game_overs of the bottom left corner of the start game button
    button_blc_x, button_blc_y = (grid_width+4) / 2 - button_w / 2, 7
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Helvetica")
    stddraw.setFontSize(35)
    stddraw.setPenColor(text_color)
    text_to_display = "START"
    stddraw.text((grid_width+4) / 2, 7.6, text_to_display)
    # menu interaction loop

    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the button
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end




# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'S', 'T', 'L', 'J']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    create_canvas()
    start()
