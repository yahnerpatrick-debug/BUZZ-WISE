"""BUZZ-WISE: the website. Routes only; the math lives in calculator.py."""

import os
import sys
from datetime import date

from flask import Flask, redirect, render_template_string, request, session, url_for

sys.path.insert(0, os.path.dirname(__file__))  # lets Vercel find the files next to this one
from calculator import SYMPTOMS, bac_now, calculate, status  # noqa: E402
from drink_menu import DRINK_MENU  # noqa: E402
from profiles import load_profiles, new_profile, save_profiles, valid_name  # noqa: E402
import templates  # noqa: E402

app = Flask(__name__)
# Set SECRET_KEY in Vercel > Project > Settings > Environment Variables
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')


def render(body, **ctx):
    ctx.setdefault('error', request.args.get('error'))
    return render_template_string(templates.LAYOUT.replace('__BODY__', body), **ctx)


def back(endpoint, error=None):
    return redirect(url_for(endpoint, error=error) if error else url_for(endpoint))


def age_on(dob, today):
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


@app.get('/')
def home():
    if not session.get('verified'):
        return render(templates.VERIFY)
    name = session.get('current')
    profiles = load_profiles(session)
    if not name or name not in profiles:
        return render(templates.PROFILE, names=[n.title() for n in profiles])
    p = profiles[name]
    bac = bac_now(p)
    return render(templates.METER, name=name, bac=bac, state=status(bac),
                  level=min(bac / 0.30, 1.0), last=p['last_calculation'],
                  menu=DRINK_MENU, round=session.get('round', []),
                  skipped=session.pop('skipped', []), symptoms=SYMPTOMS)


@app.post('/verify')
def verify():
    photo = request.files.get('id_photo')
    if not photo or not photo.filename:
        return back('home', 'Upload a photo of your ID to continue.')
    # The photo is read here and thrown away. To read the birthday off the ID
    # automatically, pass photo.read() to an OCR service at this point.
    try:
        dob = date.fromisoformat(request.form.get('dob', ''))
    except ValueError:
        return back('home', 'Enter your date of birth.')
    if age_on(dob, date.today()) < 21:
        return back('home', 'BUZZ-WISE is only for people 21 and older.')
    session['verified'] = True
    return back('home')


@app.post('/profile')
def profile():
    name = request.form.get('name', '').lower().strip()
    if not valid_name(name):
        return back('home', 'Use only letters and spaces in your name.')
    profiles = load_profiles(session)
    if name not in profiles:
        try:
            weight = float(request.form.get('weight') or 0)
            if weight <= 0:
                raise ValueError
            profiles[name] = new_profile(weight, request.form.get('sex', ''))
        except ValueError:
            return back('home', 'New profiles need a body weight and sex.')
        save_profiles(session, profiles)
    session['current'] = name
    session['round'] = []
    return back('home')


@app.post('/round/add')
def add_to_round():
    drink = request.form.get('drink', '')
    try:
        hours_ago = float(request.form.get('hours_ago') or 0)
    except ValueError:
        return back('home', 'Enter hours ago as a number, like 1.25 for 1 hour 15 minutes.')
    if hours_ago < 0:
        return back('home', "Hours ago can't be negative.")
    if drink not in DRINK_MENU:
        return back('home', 'Pick a drink from the menu.')
    session['round'] = session.get('round', []) + [{'name': drink, 'hours_ago': hours_ago}]
    return back('home')


@app.post('/round/remove/<int:i>')
def remove_from_round(i):
    r = session.get('round', [])
    if 0 <= i < len(r):
        r.pop(i)
    session['round'] = r
    return back('home')


@app.post('/calculate')
def calculate_bac():
    name = session.get('current')
    profiles = load_profiles(session)
    if name not in profiles:
        return back('home')
    _, skipped = calculate(profiles[name], session.get('round', []), DRINK_MENU)
    save_profiles(session, profiles)
    session['round'] = []
    session['skipped'] = skipped
    return back('home')


@app.get('/switch')
def switch():
    session.pop('current', None)
    session['round'] = []
    return back('home')


if __name__ == '__main__':
    app.run(debug=True)
