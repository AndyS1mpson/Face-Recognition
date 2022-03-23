from typing import List, Tuple

from core.config.config import DATABASE_CONF, METHODS_PARAM
from core.utils.load_data import load

from core.classifiers.classifier import Classifier
from core.decorators import param_plot


def recognition(
    db_name: str,
    method: str,
    param: int,
    from_test_num: int,
    to_test_num: int
) -> Tuple[float, List[Tuple]]:
    """Классификация изображений.

    Args:
        db_name:
            имя базы данных.
        method (str):
            метод для извлечения признаков.
        param:
            параметр метода.
        from_test_num:
            номер изображения, с которого начинается тренировочная выборка.
        to_test_num:
            номер изображения, по который идет тренировочная выборка.

    Raises:
        Exception:
            Некорректные параметры.

    Returns:
        Tuple[float, List[Tuple]]:
            Точность предсказания, 
            список тестовых изображений и предсказанные метки классов.
    """
    print(f'{db_name=} ; {method=}')
    images = load(db_name)
    groups_number = DATABASE_CONF[db_name]['number_group']
    images_per_group_num = DATABASE_CONF[db_name]['number_img']

    if from_test_num < 1 or from_test_num > images_per_group_num \
        or to_test_num < 1 or to_test_num > images_per_group_num:
        raise Exception("Incorrect params")

    classifier = Classifier(method)
    templates = []
    tests = []
    right_groups = []
    # Проходимся по каждой группе изображений
    for group_num in range(groups_number):
        # Создаем тренировочную выборку для каждой группы
        for train_im_num in range(from_test_num - 1, to_test_num):
            templates.append((
                images[group_num][train_im_num],
                group_num
            ))
        # Создаем тестовую выборку
        for test_image_num in range(images_per_group_num):
            if test_image_num not in range(from_test_num - 1, to_test_num):
                tests.append(images[group_num][test_image_num])
                right_groups.append(group_num)
    classifier.fit(templates, param)
    predicted_images = classifier.predict(tests)
    predicted_groups = [index for _, index in predicted_images]
    score = classifier.score(right_groups, predicted_groups)

    templates_for_tests = []
    for mark in predicted_groups:
        templates_for_tests.append(images[mark][0])

    print(f'{param=} ; {score=}')
    return score, predicted_images, templates_for_tests
