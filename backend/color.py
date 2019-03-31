# import sys
import numpy as np

# import matplotlib.pylab as plt

# replace the following with the path of the images. note: ripe_norm_bnd represents the urgently edible stage
# path = 'C:/Users/Gunalan N/Music/image_data/rotten2.npy'
# print(path)


def buffer(x, y):
    if (x + 50 > y) or (x - 50 < y):
        return True


def colorAnalyze(arc):
    # arc = np.load(route)
    valid_count = []
    blu_conch = 0
    red_conch = 0
    gre_conch = 0
    whitespace = 0
    black = 0
    yellow_conch = 0
    reference = int(arc.shape[0] / 2)


    for n in range(0, arc.shape[0]):
        for m in range(0, arc.shape[1]):
            for q in range(0, 3):
                if arc[n][m][q] != arc[0, reference][q]:
                    valid_count.append(arc[n, m])
    # print("valid pixels: " + str(len(valid_count)))
    for n in valid_count:
        if n[0] > 230 and n[1] > 230 and n[2] > 220:
            whitespace = whitespace + 1
        if n[0] < 120 and n[1] < 120 and n[2] < 120:
            black = black + 1
        elif n[1] > n[2] and n[1] > n[0]:
            gre_conch = gre_conch + 1
        elif buffer(n[0], n[1]) == True:
            yellow_conch = yellow_conch + 1
        elif n[2] > n[1] and n[2] > n[0]:
            blu_conch = blu_conch + 1
        if n[0] > n[1] + 50 and n[0] > n[2]:
            red_conch = red_conch + 1

    comp = len(valid_count) - whitespace

    if (gre_conch / comp) > yellow_conch / comp:
        return 0  # print("unripe")
    elif (black / comp) > (0.5 * yellow_conch / comp):
        return 2  # print("overripe")
    elif (red_conch / comp) + 0.1 > (0.5 * yellow_conch / comp):
        return 1  # print("soon to expire: eat soon")
    else:
        return 1  # print("store ready")
