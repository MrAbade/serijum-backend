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
    SQLALCHEMY_DATABASE_URI = 'postgres://inotqwmcewevsu:a3eb29a30d247ff51123a32810a0158999038351b412029b8cd0912b513670c5@ec2-34-200-106-49.compute-1.amazonaws.com:5432/da4oc91oglovo0'
