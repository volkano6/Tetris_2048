import numpy
import numpy as np
import matplotlib.pyplot as plt



if __name__ == "__main__":

    #binary_tile_arr= numpy.array(list)

    list = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


    # find image size
    list_height = list.shape[0]
    list_width = list.shape[1]

    background = 0
    curr_object = 0
    equivalency_list = {}

    # iterate through pixels and assign classifications
    for a in range(list_height):
        for b in range(list_width):
            if list[a][b] != background:

                if a > 0:
                    # look at pixel above
                    tile_above = list[a - 1][b]

                if b > 0:
                    # look at pixel before
                    tile_before = list[a][b - 1]

                if tile_above != background and tile_before != background:
                    classification = min(tile_above, tile_before)
                    equivalency_list[max(tile_above, tile_before)] = classification
                elif tile_above != background:
                    classification = tile_above
                elif tile_before != background:
                    classification = tile_before
                else:
                    # assign a new label
                    curr_object += 1
                    equivalency_list[curr_object] = curr_object
                    classification = curr_object

                list[a][b] = classification

    # update classifications based on equivalency list
    for a in range(list_height):
        for b in range(list_width):
            if list[a][b] != background:
                new_value = equivalency_list[list[a][b]]
                list[a][b] = new_value

    print("New Labeled List: " + str(list))
    print("Equivalency List: " + str(equivalency_list))