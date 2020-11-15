from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..models import Schedules


class ScheduleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Schedules
        include_relationships = True
        load_instance = True
