from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ...models import Suites


class SuiteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Suites
        exclude = ('users_schedule',)
        include_relationships = True
        load_instance = True

