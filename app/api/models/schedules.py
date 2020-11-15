from ..models import db


class Schedules(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    is_overnight_stay = db.Column(db.Boolean, nullable=False)
    date_of_overnight_stay = db.Column(db.Date, nullable=True)
    entry_datetime = db.Column(db.DateTime, nullable=True)
    exit_datetime = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', onupdate='CASCADE', ondelete='SET NULL'))

    suite_id = db.Column(db.Integer, db.ForeignKey(
        'suites.id', onupdate='CASCADE', ondelete='SET NULL'))

    def __repr__(self):
        scheduling_datetime = self.date_of_overnight_stay or self.entry_datetime
        return '<Scheduling for %s>' % scheduling_datetime
