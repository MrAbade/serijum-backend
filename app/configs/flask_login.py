from flask import Flask
from flask_login import LoginManager


def configure(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Você precisa se autenticar antes!'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    
    from ..web.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
