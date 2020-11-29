from flask import Blueprint, render_template, current_app, jsonify
from datetime import datetime, timedelta


bp_admin = Blueprint('admin', __name__, url_prefix='/admin')


def suite_active_without_overnight_stay(entry_datetime, exit_datetime) -> int:
    now = datetime.now()

    reservation_passed = now > exit_datetime
    reservation_entry_passed = now > entry_datetime
    suite_in_use = not reservation_passed and reservation_entry_passed

    if suite_in_use:
        return 2

    if not reservation_passed:
        return 1

    return 0


def suite_active_overnight_stay(date_of_overnight_stay) -> int:
    now = datetime.now()

    reservation_passed = now > date_of_overnight_stay
    reservation_happn = date_of_overnight_stay + timedelta(hours=15) > now
    suite_in_use = reservation_passed and reservation_happn

    if suite_in_use:
        return 2

    if not reservation_passed:
        return 1

    return 0


def suite_active(date_of_overnight_stay, entry_datetime, exit_datetime):
    if not date_of_overnight_stay:
        return suite_active_without_overnight_stay(entry_datetime, exit_datetime)

    return suite_active_overnight_stay(date_of_overnight_stay)


def format_date(date):
    if not date:
        return None

    return date.strftime('%d/%m/%Y %H:%M:%S')


@bp_admin.route('/', methods=['GET'])
def index():
    try:
        session = current_app.db.session
        query = session.execute("""
        SELECT users.name as client_name, users.email, suites.suite_number,
        schedules.is_overnight_stay, schedules.date_of_overnight_stay,
        schedules.entry_datetime, schedules.exit_datetime
        FROM suites
        JOIN schedules ON schedules.suite_id=suites.id
        JOIN users ON users.id=schedules.user_id
        """)

        serialized_reservations = (
            {key: value for key, value in zip(query.keys(), row)}
            for row in query.fetchall()
        )

        reservation_active_list = [
            {
                **reservation,
                'active': suite_active(
                    reservation['date_of_overnight_stay'],
                    reservation['entry_datetime'],
                    reservation['exit_datetime']
                ),
                'date_of_overnight_stay': format_date(reservation['date_of_overnight_stay']),
                'entry_datetime': format_date(reservation['entry_datetime']),
                'exit_datetime': format_date(reservation['exit_datetime'])
            } for reservation in serialized_reservations
        ]

        return render_template('suites.html', reservation_list=reservation_active_list)

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Make Sure you have valid credentials'}), 401
