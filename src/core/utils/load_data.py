import os
from typing import List

import cv2
from core.config.config import DATABASE_CONF
from sklearn.datasets import fetch_olivetti_faces


def upload(database):
    """Загрузка данных.

    Args:
        database:
            данные.
    """
    data_images = fetch_olivetti_faces()
    database_data = data_images["images"]
    for g_i in range(DATABASE_CONF[database]["number_group"]):
        os.mkdir("./data/ORL/s{g}".format(g=g_i + 1))
        for im_i in range(DATABASE_CONF[database]["number_img"]):
            print(
                DATABASE_CONF["ORL"]["img_path"]
                .format(g=g_i + 1, im=im_i + 1)
            )
            img = database_data[g_i * 10 + im_i] * 255
            cv2.imwrite(
                DATABASE_CONF["ORL"]["img_path"]
                .format(g=g_i + 1, im=im_i + 1),
                img
            )


def load(database) -> List:
    """Выгрузка данных.

    Args:
        database:
            имя базы данных.

    Returns:
        List:
            данные.
    """
    database_data = []
    for g_i in range(DATABASE_CONF[database]["number_group"]):
        database_group = []
        for im_i in range(DATABASE_CONF[database]["number_img"]):
            img = cv2.imread(
                DATABASE_CONF["ORL"]["img_path"]
                .format(g=g_i + 1, im=im_i + 1),
                -1
            )
            database_group.append(img)
        database_data.append(database_group)
    return database_data
