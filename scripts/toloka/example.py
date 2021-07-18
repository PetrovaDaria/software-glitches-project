import datetime
import time

import pandas
import ipyplot

import toloka.client as toloka
import toloka.client.project.template_builder as tb

import os
from dotenv import load_dotenv, find_dotenv

from definitions import TOLOKA_TUTORIAL_DATASET_PATH

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

token = os.environ.get('SANDBOX_TOLOKA_TOKEN')

print('token ', token)

toloka_client = toloka.TolokaClient(token, 'SANDBOX')  # Or switch to 'PRODUCTION'
# Lines below check that the OAuth token is correct and print your account's name
requester = toloka_client.get_requester()
print(f'Your account: {requester}')

new_project = toloka.project.Project(
    assignments_issuing_type='AUTOMATED',
    public_name='Cat or Dog?',
    public_description='Specify the type of animal depicted in a photo.',
)

input_specification = {'image': toloka.project.field_spec.UrlSpec()}
output_specification = {'result': toloka.project.field_spec.StringSpec()}

# This component shows images
image_viewer = tb.view.ImageViewV1(url=tb.data.InputData(path='image'), ratio=[1, 1])

# This component allows to select a label
radio_group_field = tb.fields.RadioGroupFieldV1(
    data=tb.data.OutputData(path='result'),
    validation=tb.conditions.RequiredConditionV1(),
    options=[
        tb.fields.GroupFieldOption(label='Cat', value='cat'),
        tb.fields.GroupFieldOption(label='Dog', value='dog'),
    ]
)

# Allows to set a width limit when displaying a task
task_width_plugin = tb.plugins.TolokaPluginV1(
    layout=tb.plugins.TolokaPluginV1.TolokaPluginLayout(
        kind='scroll',
        task_width=400,
    )
)

# How performers will see the task
project_interface = toloka.project.view_spec.TemplateBuilderViewSpec(
    config=tb.TemplateBuilder(
        view=tb.view.ListViewV1(items=[image_viewer, radio_group_field]),
        plugins=[task_width_plugin],
    )
)

# This block assigns task interface and input/output data specification to the project
# Note that this is done via the task specification class
new_project.task_spec = toloka.project.task_spec.TaskSpec(
    input_spec=input_specification,
    output_spec=output_specification,
    view_spec=project_interface,
)

new_project.public_instructions = 'Look at the picture. Determine what is on it: a <b>cat</b> or a <b>dog</b>. Choose the correct option.'

# !!! new_project = toloka_client.create_project(new_project)
print(f'Created project with id {new_project.id}')
print(f'To view the project, go to https://toloka.yandex.com/requester/project/{new_project.id}')

new_pool = toloka.pool.Pool(
    project_id=new_project.id,
    private_name='Pool 1',  # Only you can see this information
    may_contain_adult_content=False,
    reward_per_assignment=0.01,  # Sets the minimum payment amount for one task suite in USD
    assignment_max_duration_seconds=60*5,  # Gives performers 5 minutes to complete one task suite
    will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),  # Sets that the pool will close after one year
)

new_pool.defaults = toloka.pool.Pool.Defaults(
    default_overlap_for_new_tasks=3,
    default_overlap_for_new_task_suites=0,
)

new_pool.set_mixer_config(
    real_tasks_count=10,  # The number of tasks per page.
    golden_tasks_count=0,  # The number of test tasks per page. We do not use in this tutorial.
    training_tasks_count=0,  # The number of training tasks per page. We do not use in this tutorial.
)

new_pool.filter = toloka.filter.Languages.in_('EN')

# Turns on captchas
new_pool.set_captcha_frequency('MEDIUM')
# Bans performers by captcha criteria
new_pool.quality_control.add_action(
    # Type of quality control rule
    collector=toloka.collectors.Captcha(history_size=5),
    # This condition triggers the action below
    # Here overridden comparison operator actually returns a Condition object
    conditions=[toloka.conditions.FailRate > 20],
    # What exactly should the rule do when the condition is met
    # It bans the performer for 1 day
    action=toloka.actions.RestrictionV2(
        scope='PROJECT',
        duration=1,
        duration_unit='DAYS',
        private_comment='Captcha',
    )
)

# !!! new_pool = toloka_client.create_pool(new_pool)
# print(f'To view this pool, go to https://toloka.yandex.com/requester/project/{new_project.id}/pool/{new_pool.id}')
print(f'To view this pool, go to https://sandbox.toloka.yandex.com/requester/project/{new_project.id}/pool/{new_pool.id}') # Print a sandbox version link

dataset = pandas.read_csv(TOLOKA_TUTORIAL_DATASET_PATH, sep='\t')

print(f'\nDataset contains {len(dataset)} rows\n')

dataset = dataset.sample(frac=1).reset_index(drop=True)

ipyplot.plot_images(
    images=[row['url'] for _, row in dataset.iterrows()],
    labels=[row['label'] for _, row in dataset.iterrows()],
    max_images=12,
    img_width=300,
)

project_id = '71482'
pool_id = '937415'

tasks = [
    toloka.task.Task(input_values={'image': url}, pool_id=pool_id)
    for url in dataset['url']
]
# Add tasks to a pool
# !!! toloka_client.create_tasks(tasks, toloka.task.CreateTasksParameters(allow_defaults=True))
print(f'Populated pool with {len(tasks)} tasks')
print(f'To view this pool, go to https://toloka.yandex.com/requester/project/{project_id}/pool/{pool_id}')
# print(f'To view this pool, go to https://sandbox.toloka.yandex.com/requester/project/{new_project.id}/pool/{new_pool.id}') # Print a sandbox version link

# Opens the pool
# !!! new_pool = toloka_client.open_pool(pool_id)

answers = []

for assignment in toloka_client.get_assignments(pool_id=pool_id, status='ACCEPTED'):
    print('assignment ', assignment)
    for task, solution in zip(assignment.tasks, assignment.solutions):
        print('task ', task)
        print('solution ', solution)
        answers.append([task.input_values['image'], solution.output_values['result'], assignment.user_id])

print(f'answers count: {len(answers)}')
print(answers)