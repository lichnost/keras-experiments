from PIL import Image, ImageDraw
import random as rnd
from data.base import make_dir, save_file
import os
import numpy as np


def generate(folder, batch_size, already_generated, height=30, width=30):
    make_dir(folder)
    while len(os.listdir(folder)) < batch_size:
        x = rnd.randint(0, width)
        y = rnd.randint(0, height);

        xy_str = str(width) + "_" + str(height) + "_" + str(x) + "_" + str(y)
        if already_generated.count(xy_str) == 0:
            already_generated.append(xy_str)
            image = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(image)
            draw.point([x, y], 'black')
            save_file(folder, xy_str, image)
    return already_generated


def parse_y(tokens: np.ndarray, size):
    """
    :param tokens: array of image parameters vector in the form: [image_n] = [image_width, image_height, x, y]
    :param size: Size of the outputs position vector.
    :return: vector containing coordinate of point: [image_n] = [[0,0,x,0,0], [0,0,0,0,y]]
    """
    out = np.zeros([tokens.shape[0], 2, size])
    for n in range(0, out.shape[0]):
        x_index = int((tokens[n, 2] / tokens[n, 0]) * size) - 1
        y_index = int((tokens[n, 3] / tokens[n, 1]) * size) - 1
        out[n, 0, x_index] = 1
        out[n, 1, y_index] = 1
    return out
