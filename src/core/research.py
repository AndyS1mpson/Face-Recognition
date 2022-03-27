from collections import Counter
from typing import List, Tuple

from core.classifiers.classifier import Classifier
from core.config import DATABASE_CONF, METHODS_PARAM
from core.decorators import parallel_system_plot, templ_num_plot
from core.utils import feature_extractors, load, split_data


@templ_num_plot
def research(db_name: str, method: str) -> Tuple[List, List, List]:
    """Нахождение лучших параметров последовательного метода.

    Args:
        db_name:
            имя базы данных изображений.
        method:
            метод извлечения признаков.

    Returns:
        Tuple[List, List, List]:
            список скоров при разных параметрах метода
                для каждого размера тренировочной выборки,
            список тестовых изображений,
            спсок шаблонов каждого класса, присвоенного тестовым изображения.
    """
    print(f"{db_name=} ; {method=}")
    images = load(db_name)
    images_per_group_num = DATABASE_CONF[db_name]["number_img"]
    range_params = METHODS_PARAM[method]["range"]

    classifier = Classifier(feature_extractors.HANDLER[method])
    best_scores_with_params = []
    for param in range(*range_params):
        print("==================================")
        print(f"Current param: {param}")
        # Разделяем выборку
        X_train, X_test, y_train, y_test = \
            split_data(data=images, templ_to=2)
        classifier.fit(X_train, y_train, param)
        y_predicted = classifier.predict(X_test)
        score = classifier.score(y_test, y_predicted)
        # Записываем скор при текущем параметре метода
        best_scores_with_params.append((score, param))

    templates_for_tests = []
    for mark in y_predicted:
        templates_for_tests.append(images[mark][0])

    print(f"{param=} ; {score=}")
    return best_scores_with_params, X_test, templates_for_tests


@parallel_system_plot
def parallel_system_research(
    db_name: str,
    params: List[Tuple[str, int]]
) -> List:
    """Нахождение лучшего числа тестовой выборки в параллельной системе.

    Args:
        db_name:
            название бд.
        params:
            методы и их параметры.

    Returns:
        List:
            список точностей при разных размерах выборки.
    """
    images = load(db_name)
    images_per_group_num = DATABASE_CONF[db_name]["number_img"]
    methods = [param[0] for param in params]
    classifiers: List[Classifier] = []
    for method in methods:
        classifiers.append(Classifier(feature_extractors.HANDLER[method]))

    best_scores = []

    for img_num in range(1, images_per_group_num):
        print("==================================")
        print(f"Current train sample size: {img_num}")
        X_train, X_test, y_train, y_test = \
            split_data(data=images, templ_to=img_num)
        predicted_tests = []
        for index, classifier in enumerate(classifiers):
            classifier.fit(X_train, y_train, params[index][1])
            predicted_y = classifier.predict(X_test)
            predicted_tests.append(predicted_y)
        # Транспонируем двумерный список,
        # чтобы получить список ответов на каждое изображение.
        transp_preds = list(map(list, zip(*predicted_tests)))
        num_true = 0
        for index, preds in enumerate(transp_preds):
            class_search = Counter()
            for pr in preds:
                class_search[pr] += 1
            class_voting = class_search.most_common(1)[0][0]
            if class_voting == y_test[index]:
                num_true += 1
        score = num_true/len(y_test)
        best_scores.append((
            img_num,
            score
        ))
        print(f"Voting score: {score}")
    return best_scores
