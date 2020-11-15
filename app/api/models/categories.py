from ..models import db


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    suites = db.relationship(
        'Suites', lazy=True, backref=db.backref('category', lazy=False))

    def __repr__(self):
        return "<Suite Category Name %r>" % self.name
