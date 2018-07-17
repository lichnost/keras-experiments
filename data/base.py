import os
from os.path import isdir
from os import listdir
import imageio
import numpy as np


def make_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


def save_file(folder, filename, image):
    image.save(folder + "/" + filename + ".png", "png")


def load_data(path, size, y_data_parser, as_gray=True):
    """
    Function loads trainint/testing data from images of the provided path.
    :param path: path to load images from
    :param size: size of x and y vectors
    :param y_data_parser: parser function to parse out data from image filename
    :param as_gray: load as gray(e.g. one image channel) or rgb(e.g. three channels)
    :return: tuple of two numpy arays (image_data, position_vectors)
    """
    if not isdir(path):
        raise NotADirectoryError()

    files = listdir(path)
    files_tokens = np.array(list(map(lambda p: np.array(list(map(lambda v: int(v), p.replace('.png', '').split('_')))),
                                     files)))
    x_data = np.array([imageio.imread(path + "/" + p, as_gray=as_gray) for p in files])
    x_data = x_data.reshape([x_data.shape[0], x_data.shape[1], x_data.shape[2], 1 if as_gray else 3])
    y_data = y_data_parser(files_tokens, size)

    del files, files_tokens
    return (x_data, y_data)
