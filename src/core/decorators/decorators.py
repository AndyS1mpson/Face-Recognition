from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
from core.config.config import DATA_PATH


def templ_num_plot(func) -> Callable:
    """Создание графиков для результатов исследования.

    Args:
        func:
            исследование.
    """

    def wrapper(*args, **kwargs) -> Tuple:
        best_scores, test_images, templ_for_tests = func(*args, **kwargs)
        x = [x for _, x in best_scores]
        y = [y for y, _ in best_scores]

        plt.plot(x, y)
        plt.xlabel("param")
        plt.ylabel("score")
        plt.figtext(0, 0.95, f"Лучший score: {max(y)}", fontsize=10)
        plt.title(f"Зависимость точности от значений параметра")
        plt.figtext(
            0,
            0.92,
            f"Параметр: "
            f"{[p for s, p in best_scores if  s == max(y)][0]}"
        )
        plt.savefig("".join([DATA_PATH, f"results/result_1_n.png"]))
        plt.figure().clear()
        return best_scores, test_images, templ_for_tests
    return wrapper


def parallel_system_plot(func) -> Callable:
    """
    Создание графиков для результатов исследования параллельной системы.
    """
    def wrapper(*args, **kwargs) -> List:
        best_scores = func(*args, **kwargs)

        x = [x for x, _ in best_scores]
        y = [y for _, y in best_scores]

        plt.plot(x, y)
        plt.xlabel("train sample size")
        plt.ylabel("score")
        plt.title("Параллельная система, зависимость от размера выборки")
        plt.savefig("".join([DATA_PATH, "results/parallel_result.png"]))
        plt.figure().clear()
        return best_scores
    return wrapper


def parallel_ex_plot(func) -> Callable:
    """
    Создание графиков для результатов экспериментов с параллельной системой.
    """
    def wrapper(*args, **kwargs) -> List:
        scores = func(*args, **kwargs)

        x = [x for x, _ in scores]
        y = [y for _, y in scores]

        plt.plot(x, y)
        plt.xlabel("Количество изображений")
        plt.ylabel("Точность")
        plt.title("Результаты работы параллельной системы")
        plt.savefig(
            "".join([DATA_PATH, "results/parallel_experiment_result.png"])
        )
        plt.figure().clear()
        return scores
    return wrapper
