from definitions import TolokaEnv, toloka_token
import toloka.client as toloka


def get_toloka_client(env: TolokaEnv):
    token = toloka_token[env]
    env_name = env.value[0]
    toloka_client = toloka.TolokaClient(token, env_name)
    return toloka_client
