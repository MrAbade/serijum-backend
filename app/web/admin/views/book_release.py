from flask import Blueprint, request, render_template, current_app, jsonify, flash, url_for
from flask_login import login_required
from datetime import datetime, date, timedelta

from werkzeug.utils import redirect

from ..forms.book_suite_form import BookForm

from ...models import Suites
from ...models import Users
from ...models import Schedules


bp_book_release = Blueprint('book_release', __name__)

@bp_book_release.route('/book', methods=['GET', 'POST'])
@login_required
def book_suite():
    book_suite_form = BookForm()
    
    if request.method == 'GET':
        return render_template('book_suite.html.j2', form=book_suite_form)

    try:
        session = current_app.db.session
        
        name = book_suite_form.name.data
        email = book_suite_form.email.data
        suite_number = book_suite_form.suite_number.data
        entry_hour = book_suite_form.entry_hour.data
        hours_amount = book_suite_form.hours_amount.data
        is_overnight_stay = book_suite_form.is_overnight_stay.data
        
        found_suite = Suites.query.filter_by(suite_number=suite_number).first()
        if not found_suite:
            flash('O número de suíte informado não existe', 'error')
            return redirect(url_for('book_release.book_suite', form=book_suite_form))

        motel_client = Users.query.filter_by(email=email).first()
        if not motel_client:
            motel_client = Users(name=name, email=email, password='senha123', is_admin=False)
            motel_client.gen_hash()

        session.add(motel_client)
        session.commit()

        entry_datetime = datetime.combine(date.today(), entry_hour)
        
        exit_datetime = None
        if not is_overnight_stay:
            exit_datetime = entry_datetime + timedelta(hours=hours_amount)

        booking_informations = {
            'is_overnight_stay': is_overnight_stay,
            'date_of_overnight_stay': entry_datetime,
            'entry_datetime': entry_datetime,
            'exit_datetime': exit_datetime,
            'user_id': motel_client.id,
            'suite_id': found_suite.id
        }

        new_schedule = Schedules(**booking_informations)
        
        session.add(new_schedule)
        session.commit()

        flash('Suíte marcada com sucesso!', 'info')
        return redirect(url_for('reservation.reserved_suites'))

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Make sure you have permission to access this route'})


@bp_book_release.route('/release', methods=['GET', 'POST'])
@login_required
def release():
    ...