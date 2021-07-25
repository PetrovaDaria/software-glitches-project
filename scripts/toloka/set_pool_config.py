from toloka.client import TolokaClient

from definitions import TolokaEnv
from scripts.toloka.get_toloka_client import get_toloka_client


def set_pool_config(pool_id: str, env: TolokaEnv):
    toloka_client = get_toloka_client(env)
    set_mixer_config(toloka_client, pool_id)


def set_mixer_config(toloka_client: TolokaClient, pool_id: str):
    pool = toloka_client.get_pool(pool_id)
    pool.set_mixer_config(
        real_tasks_count=5,  # The number of tasks per page.
        golden_tasks_count=0,  # The number of test tasks per page. We do not use in this tutorial.
        training_tasks_count=0,  # The number of training tasks per page. We do not use in this tutorial.
        mix_tasks_in_creation_order=True,
        shuffle_tasks_in_task_suite=True
    )
    toloka_client.update_pool(pool_id, pool)


if __name__ == '__main__':
    pool_id = '938929'
    set_pool_config(pool_id, TolokaEnv.SANDBOX)