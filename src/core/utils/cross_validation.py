from core.config.config import DATABASE_CONF
from typing import List, Tuple


# def cross_validation(db_name: str, data: List, method: str, folds=3) -> Tuple:
#     templates = []
#     tests = []
#     group_number = DATABASE_CONF[db_name]['number_group']
#     for i in range(folds):
#         print(f"fold + {i}")
#         group = []
#         for j in range(group_number):
#             group.append(data[j][i+folds])
    