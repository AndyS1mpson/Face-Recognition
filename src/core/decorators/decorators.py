import matplotlib.pyplot as plt
from config import RESULT


def param_plot(func):
    def wrapper(*args, **kwargs):
        x, y = func(*args, **kwargs)
        plt.plot(x, y)
        plt.title('Изменение score при разных параметрах')
        plt.xlabel('param')
        plt.ylabel('score')
        plt.savefig(RESULT.format(im='param_plot'))
        return x, y
    return wrapper


def templ_num_plot(func):
    def wrapper(*args, **kwargs):
        x, y = func(*args, **kwargs)
        plt.plot(x, y)
        plt.title('Изменение score при разном числе изображений в выборке')
        plt.xlabel('num')
        plt.ylabel('score')
        plt.axis(x, labels=["{L}/{N_L}".format(num, x[-1] - num) for num in x])
        plt.savefig(RESULT.format(im='templ_num_plt'))
        return plt.show()
    return wrapper
