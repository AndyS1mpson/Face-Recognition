from typing import List, Tuple


def split_data(data: List, templ_from: int = 0, templ_to: int = 5) -> Tuple:
    X_train = []
    X_test = []
    y_train = []
    y_test = []
    for group_num, group in enumerate(data):
        for img_num, img in enumerate(group):
            if templ_from <= img_num < templ_to:
                X_train.append(img)
                y_train.append(group_num)
            else:
                X_test.append(img)
                y_test.append(group_num)
    return X_train, X_test, y_train, y_test
