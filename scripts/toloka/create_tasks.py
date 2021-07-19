import toloka.client as toloka
import pandas as pd
from definitions import TOLOKA_TASKS_DATASET_PATH


def create_tasks(pool_id: str):
    df = pd.read_csv(TOLOKA_TASKS_DATASET_PATH, sep='\t', encoding='utf-8')
    tasks = [
        toloka.task.Task(
            input_values={
                'title': item.title,
                'text': item.text,
                'url': item.url
            },
            pool_id=pool_id,
            id=item.id
        )
        for item in df.itertuples()
    ]
    return tasks