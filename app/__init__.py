from flask import Flask

from .app_config import configure as config_app

from .configs import config_migrate
from .configs import config_jwt
from .configs import config_login
from .configs import config_bootstrap

from .web.models import configure as config_database
from .web.api.views import configure as config_blueprints_api
from .web.admin.views import configure as config_blueprints_admin

from config import TEMPLATES_FOLDER, STATIC_FOLDER


def create_app(default_config='production'):
    app = Flask(
        __name__,
        template_folder=TEMPLATES_FOLDER,
        static_folder=STATIC_FOLDER
    )

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config_app(app, default_config)

    config_database(app)
    config_migrate(app, app.db)

    config_jwt(app)
    config_login(app)
    
    config_blueprints_api(app)
    config_bootstrap(app)
    
    config_blueprints_admin(app)

    return app
