import os
from enum import Enum
from dotenv import load_dotenv, find_dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TOLOKA_TUTORIAL_DATASET_PATH = os.path.join(ROOT_DIR, 'data/toloka-tutorial/dataset.tsv')


class TolokaEnv(Enum):
    SANDBOX = 'SANDBOX',
    PRODUCTION = 'PRODUCTION'


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
SANDBOX_TOLOKA_TOKEN = os.environ.get('SANDBOX_TOLOKA_TOKEN')
PROD_TOLOKA_TOKEN = os.environ.get('PROD_TOLOKA_TOKEN')

toloka_token = {
    TolokaEnv.SANDBOX: SANDBOX_TOLOKA_TOKEN,
    TolokaEnv.PRODUCTION: PROD_TOLOKA_TOKEN
}

TOLOKA_TASKS_DATASET_PATH = os.path.join(ROOT_DIR, 'data/toloka/tasks.tsv')

# valid only for remote machine
GOOD_TEXTS_DIR_PATH = ROOT_DIR + '/../software-glitches/csvs_by_header2'
