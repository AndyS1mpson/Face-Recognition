from typing import Callable, List, Tuple
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

from core.config.config import DATA_PATH, RESULT


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
            plt.xlabel("param")
            plt.ylabel("score")
            plt.figtext(0, 0.95, f"Лучший score: {max(y)}", fontsize=10)
            plt.title(f"Число шаблонов: {index + 1}")
            plt.figtext(
                0,
                0.92,
                f"Параметр: "
                f"{[p for s, p in b_scor_per_size if  s == max(y)][0]}"
            )
            plt.savefig("".join([DATA_PATH, f"results/result_{index}.png"]))
            plt.figure().clear()
        return best_scores, test_images, templ_for_tests
    return wrapper


def parallel_system_plot(func) -> Callable:
    def wrapper(*args, **kwargs) -> List:
        best_scores = func(*args, **kwargs)

        x = [x for x, _ in best_scores]
        y = [y for _, y in best_scores]

        plt.plot(x, y)
        plt.xlabel("train sample size")
        plt.ylabel("score")
        plt.title("Параллельная система, зависимость от размера выборки")
        plt.savefig("".join([DATA_PATH, "results/parallel_result.png"]))
        return best_scores
    return wrapper
