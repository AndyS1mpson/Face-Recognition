# from typing import List, Tuple

# from core.config.config import DATABASE_CONF, METHODS_PARAM
# from core.utils.load_data import load

# from core.classifiers.classifier import Classifier
# from core.decorators import param_plot


# def research(
#     db_name: str,
#     method: str
# ) -> Tuple[float, List[Tuple]]:
#     print(f'{db_name=} ; {method=}')
#     images = load(db_name)
#     groups_number = DATABASE_CONF[db_name]['number_group']
#     images_per_group_num = DATABASE_CONF[db_name]['number_img']
#     range_params = METHODS_PARAM[method]["range"]

#     classifier = Classifier(method)
#     templates = []
#     tests = []
#     right_groups = []
#     best_scores_with_params = []
#     # Проходимся по всем параметрам
#     for param in range(*range_params):
#         # Изменяем число шаблонов в тренирочной выборке
#         for img_num in range(*images_per_group_num):
#             # Проходимся по каждой группе изображений
#             for group_num in range(groups_number):
#                 # Создаем тренировочную выборку для каждой группы
#                 for i in range(*images_per_group_num):
#                     if i < img_num:
#                         templates.append((
#                             images[group_num][i],
#                             group_num
#                         ))
#                     else:
#                 # Создаем тестовую выборку
#                         tests.append(images[group_num][i])
#                         right_groups.append(group_num)
            
#             classifier.fit(templates, param)
#             predicted_images = classifier.predict(tests)
#             predicted_groups = [index for _, index in predicted_images]
#             score = classifier.score(right_groups, predicted_groups)
#             # Записываем скор при текущем параметре метода и числе изображений в тестовой выборке
#             best_scores_with_params.append(
#                 (
#                     score,
#                     img_num,
#                     param
#                 )
#             )

#     templates_for_tests = []
#     for mark in predicted_groups:
#         templates_for_tests.append(images[mark][0])

#     print(f'{param=} ; {score=}')
#     return score, predicted_images, templates_for_tests
