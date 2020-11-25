from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


from ..models.users import Users
from ..models.categories import Categories
from ..models.suites import Suites
from ..models.schedules import Schedules
