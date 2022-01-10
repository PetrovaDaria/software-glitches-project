from typing import List

import toloka.client as toloka


def upload_tasks(tasks: List[toloka.task.Task], toloka_client: toloka.TolokaClient):
    toloka_client.create_tasks(tasks, toloka.task.CreateTasksParameters(allow_defaults=True))
