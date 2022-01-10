import os
import pandas as pd
from definitions import TOLOKA_TASKS_DATASET_PATH, ALYA_SOFTWARE_DIR_PATH, TOLOKA_BAD_TASKS_DATASET_PATH
from scripts.text_processing.get_first_n_sentences import get_joined_first_n_sentences


def get_6k_file_names():
    df = pd.read_csv(TOLOKA_TASKS_DATASET_PATH, sep='\t', encoding='utf-8')
    ids = df['id'].to_list()
    file_names = list(map(lambda el: el[:-2], filter(lambda el: el.endswith('_0'), ids)))
    print(len(file_names))
    return file_names


def get_not_6k_file_names():
    all_filenames = os.listdir(ALYA_SOFTWARE_DIR_PATH)
    norm_tasks_file_names = get_6k_file_names()
    not_6k_file_names = list(filter(lambda el: el[:-12] not in norm_tasks_file_names, all_filenames))
    return not_6k_file_names


def create_other_tasks_dataset(dataset_path: str):
    df = pd.DataFrame(columns=[
        'id',
        'url',
        'title',
        'text',
        'in_6k_chosen_texts'
    ])
    not_6k_file_names = get_not_6k_file_names()
    count = 0
    i = 0
    for file_name in not_6k_file_names:
        if count >= 3332:
            print(i)
            break
        file_path = os.path.join(ALYA_SOFTWARE_DIR_PATH, file_name)
        print(file_path)
        new_rows = get_file_text_dicts(file_path, file_name)
        count += len(new_rows)
        for new_row in new_rows:
            df = df.append(new_row, ignore_index=True)
        i += 1
    print(count)
    df.to_csv(dataset_path, sep='\t', encoding='utf-8', index=False)


def get_file_text_dicts(file_path, file_name):
    base_id = file_name[:-12]
    df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
    i = 0
    new_rows = []
    for item in df.itertuples():
        try :
            if 'software' in item.simply_software_stat:
                new_row = {
                    'id': base_id + '_' + str(i),
                    'url': item.url,
                    'title': item.title,
                    'text': get_joined_first_n_sentences(item.text),
                    'in_6k_chosen_texts': False
                }
                new_rows.append(new_row)
        except:
            print('id ', base_id + '_' + str(i))
            print('text ', item.text)
        i += 1
    return new_rows


if __name__ == '__main__':
    create_other_tasks_dataset(TOLOKA_BAD_TASKS_DATASET_PATH)
