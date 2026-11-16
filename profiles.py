"""
Notebook 1: profiles.

The notebook version saved profiles back into profile_data.ipynb. Vercel's
servers can't write files that stick around, so on the website each person's
profiles are kept in their own browser session (a signed cookie) instead.
To share profiles across phones, swap these two functions for a database.
"""

R_VALUES = {'male': 0.68, 'female': 0.55}


def load_profiles(session):
    return session.get('profiles', {})


def save_profiles(session, profiles):
    session['profiles'] = profiles


def new_profile(weight, sex):
    lower_sex = sex.lower()
    if lower_sex not in R_VALUES:
        raise ValueError('Invalid sex entered.')
    return {
        'weight': weight,
        'sex': lower_sex,
        'r': R_VALUES[lower_sex],
        'prior_bac': 0.0,
        'last_calculation': None,
    }


def valid_name(name):
    # Letters and spaces only (the original replace(' ', ' ') never removed the spaces)
    return bool(name) and name.replace(' ', '').isalpha()
