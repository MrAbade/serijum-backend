from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField, TimeField
from wtforms.validators import InputRequired, Email, Length


class BookForm(FlaskForm):
    name = StringField('Nome:', validators=[InputRequired()])
    email = EmailField('Email:', validators=[InputRequired(), Email(), Length(1, 64)])
    suite_number = IntegerField('Número da Suíte:', validators=[InputRequired()])
    entry_hour = TimeField('Entrada:', validators=[InputRequired()])
    hours_amount = IntegerField('Horas:', validators=[InputRequired()])
    is_overnight_stay = BooleanField('Pernoite')

    submit = SubmitField('Enviar')
