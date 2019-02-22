# -*- coding: utf-8 -*-
# quiz-orm/views.py


from flask import Flask
from flask import render_template, request, redirect, url_for, abort, flash
from playhouse.flask_utils import get_object_or_404

from modele import *
from forms import *


app = Flask(__name__)


@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')


@app.route("/dodaj_klase", methods=['GET', 'POST'])
def dodaj_klase():
    form = KlasaForm()

    if form.validate_on_submit():
        Klasa(nazwa=form.nazwa.data, rok_naboru=form.rok_naboru.data,
              rok_matury=form.rok_matury.data).save()
        return redirect(url_for('index'))

    return render_template('dodaj_klase.html', form=form)


@app.route("/lista_klas")
def lista_klas():
    klasy = Klasa.select().order_by(Klasa.rok_naboru, Klasa.nazwa)
    return render_template('lista_klas.html', klasy=klasy)


@app.route('/edytuj_klase/<int:k_id>', methods=['GET', 'POST'])
def edytuj_klase(k_id):
    klasa = get_object_or_404(Klasa, Klasa.id == k_id)
    form = KlasaForm(nazwa=klasa.nazwa,
                     rok_naboru=klasa.rok_naboru, rok_matury=klasa.rok_matury)

    if form.validate_on_submit():
        klasa.nazwa = form.nazwa.data
        klasa.rok_naboru = form.rok_naboru.data
        klasa.rok_matury = form.rok_matury.data
        klasa.save()

        return redirect(url_for('lista_klas'))

    return render_template('edytuj_klase.html', form=form, klasa=klasa)
