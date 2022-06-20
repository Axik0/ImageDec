from PIL import Image
import numpy as np

img = Image.open("kitty.jpg")
# img.show()


def adv_filter(cls):
    """we fill our 10-colour palette but skip ~similar adjacent rgb colors (differ <= thr componentwise) """
    thr = 10
    # take the very first one anyway, the global maximum which must be there + we need a non-empty array for np.append
    palette = [cls[0]]
    i, j = 1, 0
    while i in range(1, 10):
        # compare 2 arrays (current) element by (previous) element with a given tolerance
        if np.allclose(cls[i+j], cls[i+j-1], atol=thr):
            # shift 1 step forward to skip the same comparison on next turn and evade infinite looping
            j += 1
        else:
            # append this row to numpy array and proceed as usual
            palette = np.append(palette, [cls[i + j]], axis=0)
            i += 1
    print(f"{j} colours were skipped")
    return palette


def basic(cls):
    """basic treatment, take 10 most frequent elements (implying cls has been already sorted) """
    return cls[:10]


def image_process(sample):
    img_arr = np.array(sample)
    # extract all the colors values,position (2D matrix) doesn't matter anymore=>cast it into (dimX*dimY,3)-shaped array
    img_colors = img_arr.reshape((-1, 3))
    # count unique colours in this 2-dimensional array
    color, occurrence = np.unique(img_colors, axis=0, return_counts=True)
    # it's sorted but wrong way, I must sort this again based on value of each color's occurrence in return_counts
    # since they're connected by index, I am going to retrieve proper indices from 2nd array first
    indices_by_occurrence = np.argsort(-occurrence)
    # shuffle 1st array with those and extract first 10 colours
    colours = color[indices_by_occurrence]
    rgb_10c = adv_filter(colours)
    argb_10c = abs(rgb_10c-[[255, 255, 255]])
    # now we should convert from rgb to hex and get a list of 3
    # just wanna play with format options in, I do know that there is a built-in hex converter
    hex_10c = ['#' + "".join(f'{c:02x}' for c in rgb3) for rgb3 in rgb_10c]
    ahex_10c = ['#' + "".join(f'{c:02x}' for c in rgb3) for rgb3 in argb_10c]
    return hex_10c, ahex_10c

print(image_process(img))