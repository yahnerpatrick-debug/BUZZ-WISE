import os
import sys
from datetime import date

from flask import Flask, redirect, render_template_string, request, send_file, session, url_for

# lets Python find the other files in this folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)

import pages
from calculator import SYMPTOMS, calculate, format_hours, get_current_bac, get_status, hours_until_zero
from profiles import load_profiles, new_profile, save_profiles, valid_name
from restaurants import RESTAURANTS, WATER, get_menu

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')  # real key is set on Vercel


def show(page, **info):
    info['error'] = request.args.get('error')
    info['message'] = session.pop('message', None)
    html = pages.LAYOUT.replace('{{ page }}', page)
    return render_template_string(html, **info)


def go_home(error=None):
    if error:
        return redirect(url_for('home', error=error))
    return redirect(url_for('home'))


def get_age(birthday):
    today = date.today()
    had_birthday = (today.month, today.day) >= (birthday.month, birthday.day)
    return today.year - birthday.year - (0 if had_birthday else 1)


@app.get('/bee.png')
def bee_image():
    return send_file(os.path.join(HERE, 'bee.png'), mimetype='image/png', max_age=86400)


@app.get('/')
def home():
    if not session.get('verified'):
        return show(pages.VERIFY)

    profiles = load_profiles(session)
    name = session.get('name')
    if name not in profiles:
        return show(pages.PROFILE, names=[n.title() for n in profiles])

    place_id = session.get('place')
    if place_id not in RESTAURANTS:
        return show(pages.PLACES, places=RESTAURANTS)

    bac = get_current_bac(profiles[name])
    return show(pages.TRACKER,
                name=name,
                bac=bac,
                status=get_status(bac),
                fill=min(bac / 0.30, 1),
                time_left=format_hours(hours_until_zero(bac)),
                has_calculated=profiles[name]['last_calculation'] is not None,
                place=RESTAURANTS[place_id],
                menu=get_menu(place_id),
                water=WATER,
                drinks=session.get('drinks', []),
                skipped=session.pop('skipped', []),
                symptoms=SYMPTOMS)


@app.post('/verify')
def verify():
    photo = request.files.get('id_photo')
    if not photo or not photo.filename:
        return go_home('Upload a photo of your ID to continue.')

    # the photo isn't saved. reading the birthday off the ID would need an OCR service
    try:
        birthday = date.fromisoformat(request.form.get('birthday', ''))
    except ValueError:
        return go_home('Enter your date of birth.')

    if get_age(birthday) < 21:
        return go_home('BUZZ-WISE is only for people 21 and older.')

    session['verified'] = True
    return go_home()


@app.post('/profile')
def profile():
    name = request.form.get('name', '').lower().strip()
    if not valid_name(name):
        return go_home('Use only letters and spaces in your name.')

    profiles = load_profiles(session)
    if name in profiles:
        session['message'] = f'Welcome back, {name.title()}!'
    else:
        try:
            weight = float(request.form.get('weight') or 0)
            if weight <= 0:
                raise ValueError
            profiles[name] = new_profile(weight, request.form.get('sex', ''))
        except ValueError:
            return go_home('New profiles need a body weight and sex.')
        save_profiles(session, profiles)

    session['name'] = name
    session['drinks'] = []
    return go_home()


@app.post('/place/<place_id>')
def pick_place(place_id):
    if place_id not in RESTAURANTS:
        return go_home('Pick a place from the list.')
    session['place'] = place_id
    session['drinks'] = []
    return go_home()


@app.get('/place/change')
def change_place():
    session.pop('place', None)
    session['drinks'] = []
    return go_home()


@app.post('/drinks/add')
def add_drink():
    menu = get_menu(session.get('place'))
    drink = request.form.get('drink', '')
    if not menu or drink not in menu:
        return go_home('Pick a drink from the menu.')

    try:
        hours = float(request.form.get('hours') or 0)
    except ValueError:
        return go_home('Enter hours as a number, like 1.25 for 1 hour 15 minutes.')
    if hours < 0:
        return go_home("Hours can't be negative.")

    session['drinks'] = session.get('drinks', []) + [{'name': drink, 'hours_ago': hours}]
    return go_home()


@app.post('/drinks/remove/<int:index>')
def remove_drink(index):
    drinks = session.get('drinks', [])
    if 0 <= index < len(drinks):
        drinks.pop(index)
    session['drinks'] = drinks
    return go_home()


@app.post('/calculate')
def calculate_bac():
    profiles = load_profiles(session)
    name = session.get('name')
    menu = get_menu(session.get('place'))
    if name not in profiles or not menu:
        return go_home()

    bac, skipped = calculate(profiles[name], session.get('drinks', []), menu)
    save_profiles(session, profiles)
    session['drinks'] = []
    session['skipped'] = skipped
    return go_home()


@app.get('/switch')
def switch_person():
    session.pop('name', None)
    session['drinks'] = []
    return go_home()


if __name__ == '__main__':
    app.run(debug=True)
