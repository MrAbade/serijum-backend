from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..models import Users


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_relationships = True
        load_instance = True
