# Profiles are saved in the browser's session cookie, since Vercel
# can't save files like the notebook version did.

R_VALUES = {'male': 0.68, 'female': 0.55}


def load_profiles(session):
    return session.get('profiles', {})


def save_profiles(session, profiles):
    session['profiles'] = profiles


def new_profile(weight, sex):
    lower_sex = sex.lower()
    if lower_sex not in R_VALUES:
        raise ValueError('Invalid sex entered.')

    return {'weight': weight, 'sex': lower_sex, 'r': R_VALUES[lower_sex],
            'prior_bac': 0.0, 'last_calculation': None}


def valid_name(name):
    return name.replace(' ', '').isalpha()
