from collections import Counter
from typing import Tuple

from src.config import DATABASE_CONF, METHODS_PARAM

from .tools import classification_quality, db_data_to_vec


def research_1_N(db_name: str, db_data, method: str) -> Tuple:
    print(f'{db_name=} ; {method=}')

    range_param = METHODS_PARAM[method]['range']
    groups_number = DATABASE_CONF[db_name]['number_group']
    images_per_group_num = DATABASE_CONF[db_name]['number_img']

    param_CV_scores = []
    param_mean_scores = []

    for param in range(*range_param):
        # Преобразование изображений из БД в вектора
        data_vec = db_data_to_vec(db_data, db_name, method, param)

        param_scores = []
        # Цикл по выбранному количеству изображений из бд
        for templ_image_num in range(images_per_group_num):
            # Создание тренировочной выборки(по 1 эталону каждой группы) и 
            # тестовой(по N-1 изображению каждой группы)
            templates: Tuple = []   # Формат: (изображение, номер группы)
            tests: Tuple = []
            # Проходимся по каждой группе изображений
            for group_num in range(groups_number):
                # Добавляем в шаблоны по одному эталону каждой группы
                templates.append((
                    data_vec[group_num][templ_image_num],
                    group_num
                ))
                # Проходимся по каждому изображению из группы
                for test_image_num in range(images_per_group_num):
                    #  Добавляем в test выборку изображения кроме выбранного для этой группы эталона
                    if test_image_num != templ_image_num:
                            tests.append((
                                data_vec[group_num][test_image_num],
                                group_num
                            ))
            # Вычисляем качество классификации 
            score = classification_quality(templates, tests)
            param_scores.append(score)
        score_mean = sum(param_scores) / len(param_scores)
        param_mean_scores.append(score_mean)
        param_CV_scores.append(param_scores)
        print(f'{param=} ; {score_mean=}')
    return param_mean_scores, param_CV_scores
