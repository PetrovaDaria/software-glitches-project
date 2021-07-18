import toloka.client as toloka
from crowdkit.aggregation import MajorityVote

import pandas

import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

token = os.environ.get('SANDBOX_TOLOKA_TOKEN')

answers =[]

toloka_client = toloka.TolokaClient(token, 'SANDBOX')  # Or switch to 'PRODUCTION'

project_id = '71482'
pool_id = '937415'

for assignment in toloka_client.get_assignments(pool_id=pool_id, status='ACCEPTED'):
    for task, solution in zip(assignment.tasks, assignment.solutions):
        answers.append([task.input_values['image'], solution.output_values['result'], assignment.user_id])

print(f'answers count: {len(answers)}')
print(answers)

answers_df = pandas.DataFrame(answers, columns=['task', 'label', 'performer'])
predicted_answers = MajorityVote().fit_predict(answers_df)
print('predicted answers')
print(predicted_answers)