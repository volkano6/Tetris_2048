import numpy as np


if __name__ == "__main__":

    img = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    # find image size
    img_height = img.shape[0]
    img_width = img.shape[1]

    background = 0
    curr_object = 0
    equivalency_list = {}

    # iterate through pixels and assign classifications
    for a in range(img_height):
        for b in range(img_width):
            if img[a][b] != background:

                if a > 0:
                    # look at pixel above
                    pixel_above = img[a - 1][b]

                if b > 0:
                    # look at pixel before
                    pixel_before = img[a][b - 1]

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

                img[a][b] = classification

    # update classifications based on equivalency list
    for a in range(img_height):
        for b in range(img_width):
            if img[a][b] != background:
                new_value = equivalency_list[img[a][b]]
                img[a][b] = new_value

    print("New Image: " + str(img))
    print("Equivalency List: " + str(equivalency_list))