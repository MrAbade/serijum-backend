from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from collections import namedtuple
from datetime import datetime

from ...error_handling import IdWasNotFound

from ..models import Schedules
from ..models import Suites

from ..schemas.schedules import ScheduleSchema


bp_schedule = Blueprint('schedule', __name__, url_prefix='/api/v1/schedule')


@bp_schedule.route('/<int:suite_id>', methods=['POST'])
@jwt_required
def create(suite_id):
    try:
        session = current_app.db.session

        user_id = get_jwt_identity()

        suite = Suites.query.get(suite_id)
        if not suite:
            raise IdWasNotFound()

        is_overnight_stay = request.json['is_overnight_stay']

        if is_overnight_stay:
            date_overnight = request.json['date_of_overnight_stay']

            date_overnight = datetime.strptime(
                date_overnight, '%Y-%m-%d %H-%M-%S')

            schedule = Schedules(
                is_overnight_stay=True,
                date_of_overnight_stay=date_overnight,
                user_id=user_id,
                suite_id=suite_id
            )

            session.add(schedule)
            session.commit()

            ss = ScheduleSchema()
            schedule_serialize = ss.dump(schedule)

            return schedule_serialize, 201

        entry_datetime = request.json['entry_datetime']
        exit_datetime = request.json['exit_datetime']

        entry_datetime = datetime.strptime(entry_datetime, '%Y-%m-%d %H-%M-%S')
        exit_datetime = datetime.strptime(exit_datetime, '%Y-%m-%d %H-%M-%S')

        schedule = Schedules(
            is_overnight_stay=False,
            entry_datetime=entry_datetime,
            exit_datetime=exit_datetime,
            user_id=user_id,
            suite_id=suite_id
        )

        session.add(schedule)
        session.commit()

        ss = ScheduleSchema()
        schedule_serialize = ss.dump(schedule)
        return schedule_serialize, 201

    except KeyError:
        return jsonify({'msg': 'Make sure the body of requisition has been filled out well'}), 400
    except IdWasNotFound:
        return jsonify({'msg': 'Make sure the suite id is correct'}), 400


@bp_schedule.route('/', methods=['GET'])
@jwt_required
def find_all():
    try:
        session = current_app.db.session
        user_id = get_jwt_identity()
        schedules = session.execute("""
            SELECT schedules.is_overnight_stay, schedules.date_of_overnight_stay,
                schedules.entry_datetime, schedules.exit_datetime, schedules.suite_id,
                suites.suite_name, suites.suite_number
            FROM users
            JOIN schedules ON users.id=schedules.user_id
            JOIN suites ON schedules.suite_id=suites.id
            WHERE schedules.user_id = :val
        """, {'val': user_id})

        schedules_serialized = [
            {
                key: value
                for key, value in zip(schedules.keys(), row)
            } for row in schedules.fetchall()]

        return jsonify(schedules_serialized), 200

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Make sure you passed correct informations'}), 400

