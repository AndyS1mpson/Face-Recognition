from typing import List, Tuple

import numpy as np

from core.utils import feature_extractors


class Classifier:
    def __init__(self, method: str) -> None:
        self.method = method
        self.train_data = []


    def __get_features(self, image: List) -> List:
        """Извлечение признакового описания изображения.

        Args:
            image:
                изображение.

        Returns:
            List:
                признаковое описание.
        """
        return feature_extractors.HANDLER[self.method](image, self.param)[1]

    
    def __dist(self, arr1: List, arr2: List) -> float:
        """Нахождение расстояния между двумя векторами в признаковом описании объектов.

        Args:
            arr1:
                вектор из признакового описания объектов. 
            arr2:
                вектор из признакового описания объектов.

        Returns:
            float:
                расстояние между данными векторами
        """
        return np.sqrt(np.sum((arr1 - arr2)**2))


    def __search(self, test) -> Tuple:
        """Поиск эталона для тестового изображения по критерию минимального расстояния.
        Args:
            test:
                тестовое изображение.
        Returns:
            Tuple:
                изображение, наиболее 'схожее' с тестовым,
                номер группы которому принадлежит шаблон.
        """
        d_min = float("inf")
        template_min = None
        template_group = None
        for group, group_templates in enumerate(self.train_data):
            for template in group_templates:
                if (d := self.__dist(template, test)) < d_min:
                    d_min = d
                    template_min = template
                    template_group = group
        return template_min, template_group


    def fit(self, images: List[Tuple], param: int) -> None:
        features: List = [[] for i in range(len(images))] 
        self.param = param
        for image, im_group in images:
            features[im_group].append(
                self.__get_features(image)
            )
        self.train_data = features


    def predict(self, images: List) -> List[Tuple]:
        """Классификация изображений.

        Args:
            images:
                изображения которые надо проклассифицировать.

        Returns:
            List[Tuple]:
                список, содержащий изображения и назначенные им классификатором группы.
        """
        predicted_groups = []
        for image in images:
            image_features = self.__get_features(image)
            _, group_num = self.__search(image_features)
            predicted_groups.append((image, group_num))
        return predicted_groups

    def score(self, true_answers: List, predicted_answers: List) -> float:
        if len(true_answers) != len(predicted_answers):
            raise Exception("Received arguments have different length")
        number_true = 0
        for index, ta in enumerate(true_answers):
            if ta == predicted_answers[index]: number_true += 1
        return (number_true/len(predicted_answers)) * 100
