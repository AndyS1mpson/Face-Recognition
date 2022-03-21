from typing import List

from config import DATABASE_CONF, METHODS_PARAM
from data import load

from core.classifiers.classifier import Classifier
from core.decorators import param_plot


@param_plot
def research_1_N(db_name: str, method: str, template_num: int) -> List:
    print(f'{db_name=} ; {method=}')
    images = load(db_name)
    range_param = METHODS_PARAM[method]['range']
    groups_number = DATABASE_CONF[db_name]['number_group']
    images_per_group_num = DATABASE_CONF[db_name]['number_img']

    param_mean_scores = []
    classifier = Classifier(method)
    # Проходимся по количеству изображений в группах
    # Это необходимо для выбора разных изображений в качестве тренировочной выборки
    templates = []
    tests = []
    right_groups = []
    # Проходимся по каждой группе изображений
    for group_num in range(groups_number):
        # Создаем тренировочную выборку
        templates.append((
            images[group_num][template_num - 1],
            group_num
        ))
        # Создаем тестовую выборку
        for test_image_num in range(images_per_group_num):
            if test_image_num != template_num - 1:
                tests.append(images[group_num][test_image_num])
                right_groups.append(group_num)
    # Проходимся по всем параметрам
    for param in range(*range_param):
        param_scores = []
        classifier.fit(templates, param)
        predicted_images = classifier.predict(tests)
        predicted_groups = [index for _, index in predicted_images]
        param_scores.append(classifier.score(right_groups, predicted_groups))
        score_mean = sum(param_scores) / len(param_scores)
        param_mean_scores.append(score_mean)
        print(f'{param=} ; {score_mean=}')
    return range(*range_param), param_mean_scores
