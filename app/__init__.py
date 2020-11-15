from flask import Flask

from .app_config import configure as config_app
from .migrate import configure as config_migrate
from .jwt import configure as config_jwt
from .api.models import configure as config_database
from .api.views import configure as config_blueprints


def create_app(default_config='production'):
    app = Flask(__name__)

    config_app(app, default_config)
    config_database(app)
    config_migrate(app, app.db)
    config_jwt(app)
    config_blueprints(app)

    return app
