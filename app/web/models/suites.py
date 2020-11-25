from ..models import db


class Suites(db.Model):
    __tablename__ = "suites"

    id = db.Column(db.Integer, primary_key=True)
    suite_number = db.Column(db.SmallInteger, nullable=False)
    suite_name = db.Column(db.String(100), nullable=False)
    suite_description = db.Column(db.Text, nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    users_schedule = db.relationship('Users', secondary='schedules')

    def __repr__(self):
        return "<Suite %r>" % self.suite_name
