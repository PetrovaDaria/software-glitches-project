# first of all add 6 thousand tasks to dataset
# then sample another 4 thousand and add them

from definitions import GOOD_TEXTS_DIR_PATH, TOLOKA_TASKS_DATASET_PATH
import os
import pandas as pd
import re
from scripts.text_processing.get_first_n_sentences import get_joined_first_n_sentences


def create_tasks_dataset(dataset_path: str):
    df = pd.DataFrame(columns=[
        'id',
        'url',
        'title',
        'text',
        'in_6k_chosen_texts'
    ])
    file_names = os.listdir(GOOD_TEXTS_DIR_PATH)
    for file_name in file_names[:10]:
        file_path = os.path.join(GOOD_TEXTS_DIR_PATH, file_name)
        new_rows = get_file_text_dicts(file_path, file_name)
        for new_row in new_rows:
            df = df.append(new_row, ignore_index=True)
    df.to_csv(dataset_path, sep='\t', encoding='utf-8', index=False)


def get_file_text_dicts(file_path, file_name):
    base_id = get_id_from_file_name(file_name)
    df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
    i = 0
    new_rows = []
    for item in df.itertuples():
        new_row = {
            'id': base_id + '_' + str(i),
            'url': item.url,
            'title': item.title,
            'text': get_joined_first_n_sentences(item.text),
            'in_6k_chosen_texts': True
        }
        new_rows.append(new_row)
        i += 1
    return new_rows


def get_id_from_file_name(file_name):
    return re.match(r'filtered_by_header_(.*)\.warc\.gz\.csv', file_name).group(1)


if __name__ == '__main__':
    create_tasks_dataset(TOLOKA_TASKS_DATASET_PATH)
