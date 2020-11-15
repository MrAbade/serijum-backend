from secrets import token_hex


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = token_hex(32)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://mrabade:pain321123@localhost/serijum'
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/serijum.db'
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://mrabade:pain321123@localhost/serijum'
