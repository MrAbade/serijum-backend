from dotenv import load_dotenv
from pathlib import Path
from os import getenv


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
    load_dotenv(dotenv_path=env_path, override=True)

    configuration = config[getenv('FLASK_CONFIGURATION')]
    print(getenv('FLASK_CONFIGURATION'))

    app.config.from_object(f'config.{configuration}')

