# -*- coding: utf-8 -*-
# quiz-orm/views.py


from flask import Flask
from flask import render_template, request, redirect, url_for, abort, flash
from playhouse.flask_utils import get_object_or_404

from modele import *
from forms import *


app = Flask(__name__)

plec = [(0, 'kobieta'), (1, 'mężczyzna')]


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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


@app.route('/lista_uczniow')
def lista_uczniow():
    uczniowie = Uczen.select().order_by(Uczen.klasa, Uczen.nazwisko, Uczen.imie)
    return render_template('lista_uczniow.html', uczniowie=uczniowie)


@app.route("/dodaj_ucznia", methods=['GET', 'POST'])
def dodaj_ucznia():
    form = UczenForm()
    form.plec.choices = plec
    form.klasa.choices = [(klasa.id, klasa.nazwa) for klasa in Klasa.select()]

    if form.validate_on_submit():
        klasa = get_object_or_404(Klasa, Klasa.id == form.klasa.data)
        Uczen(imie=form.imie.data, nazwisko=form.nazwisko.data,
              plec=form.plec.data, klasa=klasa.id).save()
        return redirect(url_for('lista_uczniow'))

    return render_template('dodaj_ucznia.html', form=form)


@app.route('/edytuj_ucznia/<int:u_id>', methods=['GET', 'POST'])
def edytuj_ucznia(u_id):
    uczen = get_object_or_404(Uczen, Uczen.id == u_id)
    klasa = get_object_or_404(Klasa, Klasa.nazwa == uczen.klasa.nazwa)
    form = UczenForm(imie=uczen.imie, nazwisko=uczen.nazwisko,
                     plec=uczen.plec, klasa=klasa.id)
    form.plec.choices = plec
    form.klasa.choices = [(klasa.id, klasa.nazwa) for klasa in Klasa.select()]

    if form.validate_on_submit():
        klasa = get_object_or_404(Klasa, Klasa.id == form.klasa.data)
        uczen.imie = form.imie.data
        uczen.nazwisko = form.nazwisko.data
        uczen.plec = form.plec.data
        uczen.klasa = klasa.id
        uczen.save()
        return redirect(url_for('lista_uczniow'))

    return render_template('edytuj_ucznia.html', form=form, uczen=uczen)
