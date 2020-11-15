from dotenv import load_dotenv
from pathlib import Path

config = {
    'development': 'DevelopmentConfig',
    'test': 'TestingConfig',
    'production': 'ProductionConfig'
}

env_config = {
    'development': '.env.dev',
    'test': '.env.test',
    'production': '.env'
}


def configure(app, default_config):
    env_path = Path('..') / env_config[default_config]
    load_dotenv(dotenv_path=env_path)

    configuration = config['production']

    app.config.from_object(f'config.{configuration}')
