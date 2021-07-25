import pandas as pd
from definitions import TOLOKA_TASKS_DATASET_PATH, TOLOKA_BAD_TASKS_DATASET_PATH, TOLOKA_JOINED_TASKS_DATASET_PATH


def join_datasets():
    tasks_df = pd.read_csv(TOLOKA_TASKS_DATASET_PATH, sep='\t', encoding='utf-8')
    bad_tasks_df = pd.read_csv(TOLOKA_BAD_TASKS_DATASET_PATH, sep='\t', encoding='utf-8')
    joined_df = pd.concat([tasks_df, bad_tasks_df], axis=0)
    joined_df.to_csv(TOLOKA_JOINED_TASKS_DATASET_PATH, sep='\t', encoding='utf-8', index=False)


if __name__ == '__main__':
    join_datasets()
