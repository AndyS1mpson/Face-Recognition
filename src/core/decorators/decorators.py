from typing import Callable, Tuple

import matplotlib.pyplot as plt

from core.config.config import DATA_PATH, RESULT


def param_plot(func) -> Callable:
    def wrapper(*args, **kwargs) -> Tuple:
        x, y = func(*args, **kwargs)
        plt.plot(x, y)
        plt.title("Изменение score при разных параметрах")
        plt.xlabel("param")
        plt.ylabel("score")
        plt.savefig(RESULT.format(im="param_plot"))
        return x, y

    return wrapper


def templ_num_plot(func) -> Callable:
    """Создание графиков для результатов исследования.

    Args:
        func:
            исследование.
    """

    def wrapper(*args, **kwargs) -> Tuple:
        best_scores, test_images, templ_for_tests = func(*args, **kwargs)
        for index, b_scor_per_size in enumerate(best_scores):
            x = [x for _, x in b_scor_per_size]
            y = [y for y, _ in b_scor_per_size]
            plt.plot(x, y)
            plt.title(f"Число шаблонов: {index + 1}")
            plt.xlabel("param")
            plt.ylabel("score")
            plt.savefig("".join([DATA_PATH, f"/results/result_{index}.png"]))
            plt.figure().clear()
        return best_scores, test_images, templ_for_tests

    return wrapper
