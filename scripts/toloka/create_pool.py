import toloka.client as toloka
import datetime

from definitions import TolokaEnv
from scripts.toloka.get_toloka_client import get_toloka_client


def create_pool(toloka_client, project_id, pool_name):
    new_pool = toloka.pool.Pool(
        project_id=project_id,
        private_name=pool_name,
        may_contain_adult_content=True,
        reward_per_assignment=0.01,
        assignment_max_duration_seconds=60 * 10,  # Gives performers 5 minutes to complete one task suite
        will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),
    )
    new_pool.defaults = toloka.pool.Pool.Defaults(
        default_overlap_for_new_tasks=3,
        default_overlap_for_new_task_suites=0,
    )
    new_pool.set_mixer_config(
        real_tasks_count=5,  # The number of tasks per page.
        golden_tasks_count=0,  # The number of test tasks per page. We do not use in this tutorial.
        training_tasks_count=0,  # The number of training tasks per page. We do not use in this tutorial.
    )
    new_pool.filter = toloka.filter.Languages.in_('EN')
    new_pool = toloka_client.create_pool(new_pool)
    return new_pool.id


if __name__ == '__main__':
    project_id = '71492'
    toloka_client = get_toloka_client(TolokaEnv.SANDBOX)
    id = create_pool(toloka_client, project_id, 'Norm settings?')
    print('new pool id ', id)
