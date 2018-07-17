
from PIL import Image, ImageDraw
import random as rnd
from math import trunc
from data.base import make_dir, save_file
import os
import numpy as np


def generate(folder, batch_size, already_generated, width=30, height=30):
    make_dir(folder)
    while len(os.listdir(folder)) < batch_size:

        part_width = int(trunc(width / 3))
        part_height = int(trunc(height / 3))

        frame_x = rnd.randint(0, part_width)
        frame_y = rnd.randint(0, part_height)
        frame_width = rnd.randint(part_width, width - frame_x - 1)
        frame_height = rnd.randint(part_height, width - frame_y - 1)

        x = rnd.randint(frame_x + 1, frame_x + frame_width - 1)
        y = rnd.randint(frame_y + 1, frame_y + frame_height - 1)

        xy_str = str(x) + "_" + str(y) + "_" + str(frame_x) + "_" + str(frame_y) + "_" + str(frame_width) + "_" + str(
            frame_height)
        if already_generated.count(xy_str) == 0:
            already_generated.append(xy_str)
            image = Image.new('RGB', [width, height], 'white')
            draw = ImageDraw.Draw(image)
            draw.rectangle([frame_x, frame_y, frame_x + frame_width, frame_y + frame_height], "white", "black")
            draw.point([x, y], 'black')
            save_file(folder, xy_str, image)
    return already_generated

def parse_y(tokens, size):
    """
    :param tokens: array of image parameters vector in the form: [image_n] = [image_width, image_height, frame_x, frame_y, frame_widht, frame_height, x, y]
    :param size: Size of the outputs position vector.
    :return: vector containing coordinate of point: [image_n] = [[0,0,1,0,0], [0,0,0,0,1]] - coordinate 0.5 of width, 1 of height
    """

    out = np.zeros([len(tokens), 2, size])
    for n in range(0, len(tokens)):
        frame_x = tokens[n, 2]
        frame_y = tokens[n, 3]
        frame_width = tokens[n, 4]
        frame_height = tokens[n, 5]
        x = tokens[n, 6]
        y = tokens[n, 7]
        framed_x = x - frame_x
        framed_y = y - frame_y
        out[n, 0, int((framed_x / frame_width) * size)] = 1
        out[n, 1, int((framed_y / frame_height) * size)] = 1
    return out
