from typing import List, Tuple

from core.classifiers.classifier import Classifier
from core.config.config import DATABASE_CONF
from core.utils import feature_extractors, load, split_data


def recognition(
    db_name: str, method: str, param: int, templ_from: int, templ_to: int
) -> Tuple[float, List, List]:
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
        Tuple[float, List, List]:
            Точность предсказания,
            Тестовая выборка,
            Шаблоны из каждой каждой группы,
                соответсвующией предсказанным группам тестовой выборки.
    """
    print(f"{db_name=} ; {method=}")
    images = load(db_name)
    images_per_group_num = DATABASE_CONF[db_name]["number_img"]

    if (
        templ_from < 1
        or templ_from > images_per_group_num
        or templ_to < 1
        or templ_to > images_per_group_num
        or templ_from > templ_to
    ):
        raise Exception("Incorrect params")

    classifier = Classifier(feature_extractors.HANDLER[method])
    # Создаем train и test выборки
    X_train, X_test, y_train, y_test = split_data(images, templ_from, templ_to)

    classifier.fit(X_train, y_train, param)
    y_predicted = classifier.predict(X_test)

    score = classifier.score(y_test, y_predicted)

    templates_for_tests = []
    for mark in y_predicted:
        templates_for_tests.append(images[mark][0])

    print(f"{param=} ; {score=}")
    return score, X_test, templates_for_tests
