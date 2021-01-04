from flask import Blueprint, render_template, current_app, jsonify
from flask_login import login_required

from .scripts import format_date
from .scripts import suite_active


bp_reservation = Blueprint('reservation', __name__)

@bp_reservation.route('/list', methods=['GET'])
@login_required
def reserved_suites():
    try:
        session = current_app.db.session
        query = lambda: session.execute("""
        SELECT users.name as client_name, users.email, suites.suite_number,
        schedules.is_overnight_stay, schedules.date_of_overnight_stay,
        schedules.entry_datetime, schedules.exit_datetime
        FROM suites
        JOIN schedules ON schedules.suite_id=suites.id
        JOIN users ON users.id=schedules.user_id
        """)

        if not query().fetchall():
            empty = list()
            return jsonify(empty)

        serialized_reservations = lambda query: (
            {key: value for key, value in zip(query.keys(), row)}
            for row in query.fetchall()
        )

        reservation_active_list = lambda reservation_list: (
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
            } for reservation in reservation_list
        )

        reservation_filter = lambda time_type, reservation_list: [
            reservation
            for reservation in reservation_list
            if reservation['active'] == time_type
        ]

        reservation_with_active = lambda: reservation_active_list(serialized_reservations(query()))

        reservation_list = [
            reservation_filter(2, reservation_with_active()),
            reservation_filter(1, reservation_with_active()),
            reservation_filter(0, reservation_with_active())
        ]

        return render_template('suites.html.j2', reservation_categories=reservation_list)

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Make Sure you have valid credentials'}), 401

