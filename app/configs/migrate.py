from flask_migrate import Migrate


def configure(app, db):
    Migrate(app, db)
