from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, Length, InputRequired


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField('Senha:', validators=[InputRequired()])
    remember_me = BooleanField('Lembrar-me')

    submit = SubmitField('Login')
