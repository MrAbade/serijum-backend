from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from ..forms.login_form import LoginForm

from ...models import Users

bp_auth = Blueprint('auth', __name__)


@bp_auth.route('/login', methods=['GET', 'POST']) 
def login():
    login_form = LoginForm(request.form)

    if not login_form.validate_on_submit():
        return render_template('login.html.j2', form=login_form)

    email = login_form.email.data
    password = login_form.password.data
    remember = login_form.remember_me.data

    found_user = Users.query.filter_by(email=email).first()
    invalid_credentials = not found_user or not found_user.password_verify(password)
    if invalid_credentials or not found_user.is_admin:
        flash(u'Email/Senha incorretos, ou sem permissão de acesso!', 'error')
        return render_template('login.html.j2', form=login_form)    

    login_user(found_user, remember)

    next_access = request.args.get('next')
    if not next_access or '/' in next_access:
        next_access = 'reservation.reserved_suites'
    
    return redirect(url_for(next_access))


@bp_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado(a)!')
    return redirect(url_for('auth.login'))
