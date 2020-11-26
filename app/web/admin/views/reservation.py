from flask import Blueprint, render_template, current_app

from config import TEMPLATES_FOLDER, STATIC_FOLDER

bp_admin = Blueprint(
    'admin', __name__,
    url_prefix='/admin',
    template_folder=TEMPLATES_FOLDER,
    static_folder=STATIC_FOLDER
)


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

        serialized_reservations = [
            {key: value for key, value in zip(query.keys(), row)}
            for row in query.fetchall()
        ]


    except Exception as error:
        print(error)

    return render_template('index.html', reservation_list=serialized_reservations)
