# -*- coding: utf-8 -*-
# quiz-orm/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField
from wtforms import StringField, HiddenField, IntegerField
from wtforms.validators import DataRequired, NumberRange

blad1 = 'To pole jest wymagane'


class KlasaForm(FlaskForm):
  id = HiddenField()
  nazwa = StringField('Nazwa dodawanej klasy: ', validators=[DataRequired(message=blad1)])
  rok_naboru = IntegerField('Rok naboru: ', validators=[DataRequired(message=blad1), NumberRange(min=2000, max=100)])
  rok_matury = IntegerField('Rok matury: ', validators=[DataRequired(message=blad1), NumberRange(min=2000, max=100)])


class UczenForm(FlaskForm):
  id = HiddenField()
  imie = StringField('Imię  dodawanego ucznia: ', validators=[DataRequired(message=blad1)])
  nazwisko = StringField('Nazwisko ucznia: ', validators=[DataRequired(message=blad1)])
  plec = BooleanField('Płeć ucznia: ', validators=[DataRequired(message=blad1)])
  klasa = SelectField('Klasa', coerce=int)
