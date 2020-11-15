from flask_jwt_extended import JWTManager


def configure(app):
    JWTManager(app)
