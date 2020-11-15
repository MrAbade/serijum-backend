from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..models import Users


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        exclude = ('id', 'password',)
        include_relationships = False
        load_instance = True
