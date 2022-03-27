from collections import Counter
from typing import List, Tuple
from core.decorators import parallel_ex_plot
from core.classifiers.classifier import Classifier
from core.config.config import DATABASE_CONF
from core.utils import feature_extractors, load, split_data


def recognition(
    db_name: str,
    method: str,
    param: int,
    templ_from: int,
    templ_to: int
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


@parallel_ex_plot
def parallel_recognition(
    db_name: str,
    params: List[Tuple],
    templ_to: int
) -> List:
    """Классификация изображений в параллельной системе.

    Args:
        db_name:
            название бд изображений.
        params:
            параметры методов.
        templ_to:
            число шаблонов тренировочной выборки.

    Returns:
        List:
            список точностей классификации для
            каждого количества тестовых изображений.
    """
    images = load(db_name)
    methods = [param[0] for param in params]
    classifiers: List[Classifier] = []

    for method in methods:
        classifiers.append(Classifier(feature_extractors.HANDLER[method]))

    X_train, X_test, y_train, y_test = \
        split_data(data=images, templ_to=templ_to)

    for index, classifier in enumerate(classifiers):
        classifier.fit(X_train, y_train, params[index][1])

    accuracy_at_num_of_images = []

    for index, _ in enumerate(X_test):
        print(f"Current images num: {index}")
        current_tests = []
        current_right_y = []
        predicted_tests = []
        for i in range(index + 1):
            current_tests.append(X_test[i])
            current_right_y.append(y_test[i])
        for index, classifier in enumerate(classifiers):
            predicted_y = classifier.predict(current_tests)
            predicted_tests.append(predicted_y)
        # Транспонируем список, чтобы поулчить
        # список всех оценок для каждого изображения
        transp_preds = list(map(list, zip(*predicted_tests)))
        num_true = 0
        # Находим метки изображений на основе голосования
        for index, preds in enumerate(transp_preds):
            class_search = Counter()
            for pr in preds:
                class_search[pr] += 1
            class_voting = class_search.most_common(1)[0][0]
            if class_voting == y_test[index]:
                num_true += 1
        score = num_true/len(current_right_y)
        accuracy_at_num_of_images.append((
            index,
            score
        ))
    return accuracy_at_num_of_images
