import game_grid
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes


# MAIN FUNCTION OF THE PROGRAM
# -----------------------------------------------------------------------------------
# Main function where this program  starts execution

def create_canvas():
    # set the dimensions  of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas
    canvas_h, canvas_w = 43 * grid_h, 55 * grid_w
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system
    stddraw.setXscale(-0.6, grid_w + 4.7)
    stddraw.setYscale(-0.6, grid_h - 0.4)

    grid_h, grid_w = 20, 12
    # set the dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

    # create the game grid
    grid = GameGrid(grid_h, grid_w)

    # display a simple menu before opening    game
    # by using the display_game_menu function defined below
    display_game_menu(grid)

    # The part where game flow
    start(grid)

# The part where game flow
def start(grid):
    # created list ("tetromino_list") for tetrominoes
    # When the "current_tetromino" is done None, new tetromino takes in "tetromino_list"
    tetromino_list = [create_tetromino(grid.grid_height, grid.grid_width),
                      create_tetromino(grid.grid_height, grid.grid_width),
                      create_tetromino(grid.grid_height, grid.grid_width)]
    # tetromino list is entered the game grid
    grid.tetromino_list = tetromino_list

    # first tetromino is entered the game grid
    # by using the create_tetromino function defined below
    current_tetromino = tetromino_list[0]
    grid.current_tetromino = current_tetromino

    # First value of "tetromino_list" is used. This part update tetrominoes list.
    tetromino_list.pop(0)
    tetromino_list.append(create_tetromino(grid.grid_height, grid.grid_width))

    # When the game is finished, we can store total score from this arr.
    score_array = [0]

    # setting for rotate
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
                # change the active tetromino rotate direction
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
            # if user typed 'p', the game will pause
            if key_typed == 'p':
                display_pause(grid.grid_height, grid.grid_width)
            # if user typed 'p', the game will restart
            if key_typed == 'r':
                new_grid = GameGrid(grid.grid_height, grid.grid_width)
                start(new_grid)
            # if user typed 'e', the game exit
            if key_typed == 'e':
                new_grid = GameGrid(grid.grid_height, grid.grid_width)
                display_game_over(new_grid, score_array)
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
            tetromino_list.append(create_tetromino(grid.grid_height, grid.grid_width))

        score_array.pop(0)
        score_array.append(grid.total_score)
        # display the game grid and the current tetromino
        grid.display()
    # print a message on the console when the game is over
    display_game_over(grid, score_array)
    print("Game over")

# Settings menu
def settings_game_menu(game_grid):
    width = game_grid.grid_width + 5
    height = game_grid.grid_height

    # colors used for the menu
    background_color = Color(221, 221, 221)
    button_color = Color(201, 201, 201)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    stddraw.clear(background_color)

    # center coordinates to display the image
    img_center_x, img_center_y = (width - 1) / 2, height - 7

    # dimensions of the start game button
    easy_button_w, easy_button_h = width - 5, 1.7
    # coordinates of the bottom left corner of the start game button
    easy_button_blc_x, easy_button_blc_y = img_center_x - easy_button_w / 2, 12.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(easy_button_blc_x, easy_button_blc_y, easy_button_w, easy_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Easy"
    stddraw.text(img_center_x, easy_button_blc_y + 0.86, text_to_display)

    # dimensions of the start game button
    medium_button_w, medium_button_h = width - 5, 1.7
    # coordinates of the bottom left corner of the start game button
    medium_button_blc_x, medium_button_blc_y = img_center_x - medium_button_w / 2, 8.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(medium_button_blc_x, medium_button_blc_y, medium_button_w, medium_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Medium"
    stddraw.text(img_center_x, medium_button_blc_y + 0.86, text_to_display)

    # dimensions of the start game button
    hard_button_w, hard_button_h = width - 5, 1.7
    # coordinates of the bottom left corner of the start game button
    hard_button_blc_x, hard_button_blc_y = img_center_x - hard_button_w / 2, 4.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(hard_button_blc_x, hard_button_blc_y, hard_button_w, hard_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Hard"
    stddraw.text(img_center_x, hard_button_blc_y + 0.86, text_to_display)

    # dimensions of the start game button
    back_button_w, back_button_h = width - 15, 1.7
    # coordinates of the bottom left corner of the start game button
    back_button_blc_x, back_button_blc_y = 0, 17.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(back_button_blc_x, back_button_blc_y, back_button_w, back_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Back"
    stddraw.text(back_button_blc_x + 1, back_button_blc_y + 0.9, text_to_display)

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
            if mouse_x >= easy_button_blc_x and mouse_x <= easy_button_blc_x + easy_button_w:
                if mouse_y >= easy_button_blc_y and mouse_y <= easy_button_blc_y + easy_button_h:
                    game_grid.delay_game = 290
                    game_grid.delay_merge_and_clear_row = 50

            if mouse_x >= medium_button_blc_x and mouse_x <= medium_button_blc_x + medium_button_w:
                if mouse_y >= medium_button_blc_y and mouse_y <= medium_button_blc_y + medium_button_h:
                    game_grid.delay_game = 220
                    game_grid.delay_merge_and_clear_row = 20

            if mouse_x >= hard_button_blc_x and mouse_x <= hard_button_blc_x + hard_button_w:
                if mouse_y >= hard_button_blc_y and mouse_y <= hard_button_blc_y + hard_button_h:
                    game_grid.delay_game = 150
                    game_grid.delay_merge_and_clear_row = 10

            if mouse_x >= back_button_blc_x and mouse_x <= back_button_blc_x + back_button_w:
                if mouse_y >= back_button_blc_y and mouse_y <= back_button_blc_y + back_button_h:
                    display_game_menu(game_grid)
                    break

# Function for displaying a simple menu before starting the game
def display_game_menu(game_grid):
    width = game_grid.grid_width + 5
    height = game_grid.grid_height

    # colors used for the menu
    background_color = Color(221, 221, 221)
    button_color = Color(201, 201, 201)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (width - 1) / 2, height - 7
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = width - 5, 1.7
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

    # dimensions of the start game button
    settings_button_w, settings_button_h = width - 5, 1.7
    # coordinates of the bottom left corner of the start game button
    settings_button_blc_x, settings_button_blc_y = img_center_x - settings_button_w / 2, 2.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(settings_button_blc_x, settings_button_blc_y, settings_button_w, settings_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Game Settings"
    stddraw.text(img_center_x, settings_button_blc_y + 0.85, text_to_display)

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
                    break
            if mouse_x >= settings_button_blc_x and mouse_x <= settings_button_blc_x + settings_button_w:
                if mouse_y >= settings_button_blc_y and mouse_y <= settings_button_blc_y + settings_button_h:
                    settings_game_menu(game_grid)

def display_game_over(game_grid, arr):

    new_grid = GameGrid(game_grid.grid_height, game_grid.grid_width)
    new_grid.delay_game = game_grid.delay_game
    new_grid.delay_merge_and_clear_row = game_grid.delay_merge_and_clear_row

    width = game_grid.grid_width
    height = game_grid.grid_height

    grid = GameGrid(height, width)
    background_color = Color(221, 221, 221)
    button_color = Color(201, 201, 201)
    text_color = Color(0, 0, 0)
    # clear the background canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/game_over4.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (width + 3.7) / 2, height - 6
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = width - 3.8, 1.5
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
    stddraw.boldText(width - 4, 10, "SCORE")
    stddraw.boldText(width - 4, 9, str(arr[0]))
    # menu interaction loop

    # dimensions of the start game button
    settings_button_w, settings_button_h = width - 5, 1.7
    # coordinates of the bottom left corner of the start game button
    settings_button_blc_x, settings_button_blc_y = img_center_x - settings_button_w / 2, 2.1
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(settings_button_blc_x, settings_button_blc_y, settings_button_w, settings_button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(27)
    stddraw.setPenColor(text_color)
    text_to_display = "Game Settings"
    stddraw.text(img_center_x, settings_button_blc_y + 0.85, text_to_display)

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
                    start(new_grid)  # break the loop to end

            if mouse_x >= settings_button_blc_x and mouse_x <= settings_button_blc_x + settings_button_w:
                if mouse_y >= settings_button_blc_y and mouse_y <= settings_button_blc_y + settings_button_h:
                    settings_game_menu(new_grid)

def display_pause(grid_height, grid_width):

    grid = GameGrid(grid_height, grid_width)

    button_color = Color(201, 201, 201)
    text_color = Color(255, 255, 255)
    # clear the background canvas to background_color
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    img_file = current_dir + "/images/pause.png"
    # center coordinates to display the image
    img_center_x, img_center_y = (grid_width + 4) / 2, grid_height - 9
    # image is represented using the Picture class
    image_to_display = Picture(img_file)
    # display the image
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    button_w, button_h = grid_width - 7, 1.3
    # coordinate display_game_overs of the bottom left corner of the start game button
    button_blc_x, button_blc_y = (grid_width + 4) / 2 - button_w / 2, 7
    # display the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    stddraw.setFontFamily("Helvetica")
    stddraw.setFontSize(35)
    stddraw.setPenColor(text_color)
    text_to_display = "START"
    stddraw.text((grid_width + 4) / 2, 7.6, text_to_display)
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
