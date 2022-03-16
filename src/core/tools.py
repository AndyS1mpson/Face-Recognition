from typing import List, Tuple

from src.config import DATABASE_CONF

import core.feature_extractors as feature_extractors

from .dist import dist


def db_data_to_vec(data, db_name: str, method, param) -> List:
    """Выделение признакового описания для каждого изображения из data.

    Args:
        data:
            набор изображений.
        db_name:
            имя базы данных.
        method:
            метод извлечения признакового описания.
        param:
            параметр методаю

    Returns:
        List:
            список признаковых описаний объектов.
    """
    number_gr = DATABASE_CONF[db_name]['number_group']
    number_img = DATABASE_CONF[db_name]['number_img']
    data_vec = []
    for gr in range(number_gr):
        group_vec = []
        for im in range(number_img):
            group_vec.append(feature_extractors.HANDLER[method](data[gr][im], param)[1])
        data_vec.append(group_vec)
    return data_vec


def recognition(img, method, param, database_data, g_range, i_range):
    print(f"START 'Recognition'. Method '{method}'[{param}]")
    img_features, img_vec = feature_extractors.HANDLER[method](img, param)

    rec_img = None
    rec_img_features = None
    d_min = float("inf")
    for g_i in range(g_range):
        for im_i in range(i_range):
            tmp_img = database_data[g_i][im_i]
            tmp_img_features, tmp_img_vec = feature_extractors.HANDLER[method](tmp_img, param)
            if (d := dist(img_vec, tmp_img_vec)) < d_min:
                d_min = d
                rec_img = (g_i, im_i)
                rec_img_features = tmp_img_features
    print('END')
    return img_features, rec_img, rec_img_features


def _search(templates: Tuple, test: Tuple):
    """Поиск эталона для тестового изображения по критерию минимального расстояния.

    Args:
        templates:
            набор эталонных изображений.
        test:
            тестовое изображение.

    Returns:
        _type_:
            изображение, наиболее 'схожее' с тестовым.
    """
    test_vec = test[0]
    d_min = float("inf")
    template_min = None
    for template in templates:
        template_vec = template[0]
        if(d := dist(template_vec, test_vec)) < d_min:
            d_min = d
            template_min = template
    return template_min


def classification_quality(templates: Tuple, tests: Tuple) -> float:
    """Расчёт качества классификации.

    Args:
        templates:
            набор эталонных изображений.
        tests:
            набор тестовых изображений.

    Returns:
        float:
            качество классификации.
    """
    number_true = 0
    for test in tests:
        template_search = _search(templates, test)
        class_test = test[1]
        class_search  = template_search[1]
        if class_test == class_search: number_true += 1
    score = (number_true / len(tests)) * 100
    return score
