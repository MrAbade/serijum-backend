from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ...models import Categories


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categories
        include_relationships = True
        load_instance = True
