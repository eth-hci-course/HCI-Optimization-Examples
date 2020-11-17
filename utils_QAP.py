import numpy as np
import re
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Returns Euclidean distance between two element positions in a grid layout
def distance(columns, i, j):
    return np.sqrt(
        abs(j / columns - i / columns) ** 2 + abs(i % columns - j % columns) ** 2
    )


def wpm(avg_iki_in_s):
    """Computes the average words per minute that could be achieved with
    a keyboard from the given avg inter-key interval
    """
    if avg_iki_in_s == 0:
        return 0
    else:
        return (1.0 / avg_iki_in_s * 60) / 5


def get_bigram_frequency(letters):
    """
    reads the .csv file containing the bigram frequencies
    Returns a map from bigrams to frequencies
    """
    bigramdist = {}
    f = open("resources/bigram.csv", encoding="utf8")
    lines = f.readlines()
    for line in lines:
        if line[4] == '"':
            line = re.sub('"\t', "\t", line)
            line = re.sub('""', '"', line)
            line = re.sub('^"', "", line)
        line = re.sub(r"\r", "", line)
        line = re.sub(r"\n", "", line)
        if len(line) > 1:
            parts = re.split("\t", line)
            bigram = parts[0]
            if bigram[0] in letters and bigram[1] in letters:
                bigramdist[bigram[0], bigram[1]] = float(parts[1])

        # normalize
        s = np.sum([float(x) for x in bigramdist.values()])
        for c, v in bigramdist.items():
            bigramdist[c] = v / s

    return bigramdist


def fittslawcost(i, j, D):
    """
    Returns the fitts law cost for pointing from key i to key j.
    D: key distance
    """
    # Fitts parameter:
    a = 0.0  # a and b paramater as used in [zhai et al. 2000]
    b = 0.204

    arep = 0.127  # fixed mt for letter repetition
    W = 1.0  # key width
    mt = -9999999
    if i == j:
        mt = arep + b * math.log(D / W + 1, 2)  # repetition of the key, from the paper
    else:
        mt = a + b * math.log(D / W + 1, 2)
    return mt


def plot_keyboard(mapping, columns):
    """
    Plots the keyboard
    mapping: dict from letters to keynumber
    columns: the number of columns of the keyboard
    """

    rows = int(math.ceil(len(mapping) / float(columns)))

    fig, ax = plt.subplots(1)
    fig.set_size_inches(3, 3)

    # box dimensions
    key_height = 4
    key_width = 4

    # keyboard specifics
    row_distance = 0.5
    column_distance = 0.5

    for row in range(0, rows):
        for column in range(0, columns):
            x = (column * key_width) + column * column_distance
            y = (row * key_height) + row * row_distance

            # print button
            ax.add_patch(patches.Rectangle((x, y), key_width, key_height, fill=False))

    for l, slot in mapping.items():
        row = math.floor(slot / columns)
        column = slot % columns

        x = (column * key_width) + column * column_distance + key_width / float(2)
        y = (row * key_height) + row * row_distance + key_height / float(2)
        # print label
        l = l.capitalize()
        ax.text(
            x,
            y,
            l,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=18,
            color="k",
        )

    max_x = (columns - 1) * key_width + (columns - 1) * column_distance + key_width + 1
    max_y = (rows - 1) * key_height + (rows - 1) * row_distance + key_height + 1

    plt.axis("off")
    ax.set_xlim([-1, max(max_x, max_y)])
    ax.set_ylim([-1, max(max_x, max_y)])
    plt.show()
