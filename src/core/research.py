# from typing import List, Tuple

# from core.classifiers.classifier import Classifier
# from core.config import DATABASE_CONF, METHODS_PARAM
# from core.decorators import param_plot
# from core.utils import feature_extractors, load, split_data


# def research(
#     db_name: str,
#     method: str
# ) -> Tuple[float, List[Tuple]]:
#     print(f'{db_name=} ; {method=}')
#     images = load(db_name)
#     images_per_group_num = DATABASE_CONF[db_name]['number_img']
#     range_params = METHODS_PARAM[method]["range"]

#     classifier = Classifier(feature_extractors.HANDLER[method])
#     best_scores_per_templ_size = []
#     # Изменяем число шаблонов в тренирочной выборке
#     for img_num in range(*images_per_group_num):
#         best_scores_with_params = []
#         # Разделяем выборку
#         templates, tests = split_data(data=images, templ_to=img_num)
#         # Отделяем тестовые изображения от их меток 
#         right_groups = [group_num for _, group_num in tests]
#         tests = [img for img, _ in tests]
        
#         # Проходимся по всем параметрам
#         for param in range(*range_params): 
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
#         # Сохраняем результаты для каждого размера обучающей выборки
#         best_scores_per_templ_size.append(best_scores_with_params)

#     templates_for_tests = []
#     for mark in predicted_groups:
#         templates_for_tests.append(images[mark][0])

#     print(f'{param=} ; {score=}')
#     return score, predicted_images, templates_for_tests
