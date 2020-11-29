from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta


bp_isbusy = Blueprint('isbusy', __name__, url_prefix='/api/v1/isbusy')


def reservation_is_overnigth_stay(reservation):
    del reservation['entry_datetime']
    del reservation['exit_datetime']
    return reservation


def reservation_is_not_overnigth_stay(reservation):
    del reservation['date_of_overnight_stay']
    return reservation


def normalize_reservation_attributes(reservation):
    if reservation['is_overnight_stay']:
        return reservation_is_overnigth_stay(reservation)

    return reservation_is_not_overnigth_stay(reservation)


@bp_isbusy.route('/<int:suite_id>', methods=['GET'])
@jwt_required
def busy_hours(suite_id):
    try:
        session = current_app.db.session

        max_date = datetime.now() + timedelta(days=7)
        today = datetime.now()

        query = session.execute("""
            SELECT schedules.is_overnight_stay, schedules.date_of_overnight_stay,
            schedules.entry_datetime, schedules.exit_datetime
            FROM schedules
            WHERE schedules.suite_id=:suite_id
            AND ((schedules.date_of_overnight_stay < :max_date
            AND schedules.date_of_overnight_stay > :today)
            OR (schedules.entry_datetime < :max_date
            AND schedules.exit_datetime > :today
            ))
        """, {
            'suite_id': suite_id,
            'max_date': max_date,
            'today': today
        })

        serialized_reservation_list = (
            {key: value for key, value in zip(query.keys(), row)}
            for row in query.fetchall()
        )

        reservation_list_parsed_datetime = [
            {
                **reservation,
                'date_of_overnight_stay': str(reservation['date_of_overnight_stay']),
                'entry_datetime': str(reservation['entry_datetime']),
                'exit_datetime':  str(reservation['exit_datetime']),
            }
            for reservation in serialized_reservation_list
        ]

        reservation_list = list()
        for reservation in reservation_list_parsed_datetime:
            normalized_reservation = normalize_reservation_attributes(
                reservation)
            reservation_list.append(normalized_reservation)

        return jsonify(reservation_list), 200

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Cannot find busy hours of that suite'}), 400
