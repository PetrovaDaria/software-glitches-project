from definitions import TolokaEnv, TOLOKA_TASKS_DATASET_PATH
from scripts.toloka.create_tasks_dataset import create_tasks_dataset
from scripts.toloka.create_tasks import create_tasks
from scripts.toloka.get_toloka_client import get_toloka_client
from scripts.toloka.upload_tasks import upload_tasks


if __name__ == '__main__':
    # define dataset path
    # create_tasks_dataset(TOLOKA_TASKS_DATASET_PATH)


    pool_id = '938929'
    tasks = create_tasks(pool_id)
    #
    toloka_client = get_toloka_client(TolokaEnv.SANDBOX)
    upload_tasks(tasks, toloka_client)