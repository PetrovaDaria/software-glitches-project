import pandas as pd
from definitions import TOLOKA_JOINED_TASKS_DATASET_PATH, TOLOKA_SHUFFLED_TASKS_DATASET_PATH


def shuffle_dataset():
    df = pd.read_csv(TOLOKA_JOINED_TASKS_DATASET_PATH, sep='\t', encoding='utf-8')
    shuffled_df = df.sample(frac=1)
    shuffled_df.to_csv(TOLOKA_SHUFFLED_TASKS_DATASET_PATH, sep='\t', encoding='utf-8', index=False)


if __name__ == '__main__':
    shuffle_dataset()
