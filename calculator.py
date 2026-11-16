from datetime import datetime

BURN_RATE = 0.015  # how much BAC goes down per hour

SYMPTOMS = [
    'Vomiting',
    'Seizures',
    'Irregular breathing',
    'Low body temperature',
    'Trouble staying awake',
    'Blue, gray, pale or clammy skin',
]


def get_time_since(profile, now):
    # first calculation counts every drink
    if profile['last_calculation'] is None:
        return float('inf')
    last_calculation = datetime.fromisoformat(profile['last_calculation'])
    return (now - last_calculation).total_seconds() / 3600


def get_current_bac(profile, now=None):
    now = now or datetime.now()
    time_since = get_time_since(profile, now)
    return max(0, profile['prior_bac'] - BURN_RATE * time_since)


def get_drink_bac(ounces, abv_percent, weight, r, hours_ago):
    abv_decimal = abv_percent / 100
    pure_alc = ounces * abv_decimal
    drink_bac = (pure_alc * 5.14) / (weight * r)
    drink_bac -= BURN_RATE * hours_ago
    # a drink that already wore off shouldn't take away from the others
    return max(0, drink_bac)


def calculate(profile, drinks, menu, now=None):
    now = now or datetime.now()
    time_since = get_time_since(profile, now)
    current_bac = get_current_bac(profile, now)
    skipped = []

    # water / no drink means resting, so its hours lower the BAC.
    # only count the hours that haven't already passed since last time
    rest_hours = 0
    for drink in drinks:
        if menu[drink['name']]['abv_percent'] == 0:
            rest_hours = max(rest_hours, drink['hours_ago'])

    if rest_hours > 0 and time_since != float('inf'):
        extra_hours = max(0, rest_hours - time_since)
        current_bac = max(0, current_bac - BURN_RATE * extra_hours)

    for drink in drinks:
        info = menu[drink['name']]
        if info['abv_percent'] == 0:
            continue

        # already counted in an earlier calculation
        if drink['hours_ago'] > time_since:
            skipped.append(drink['name'])
            continue

        current_bac += get_drink_bac(info['ounces'], info['abv_percent'],
                                     profile['weight'], profile['r'], drink['hours_ago'])

    current_bac = max(0, current_bac)
    profile['prior_bac'] = current_bac
    profile['last_calculation'] = now.isoformat()
    return current_bac, skipped


def hours_until_zero(bac):
    return bac / BURN_RATE


def format_hours(hours):
    h, m = divmod(round(hours * 60), 60)
    if h and m:
        return f'{h} h {m} min'
    if h:
        return f'{h} h'
    return f'{m} min'


def get_status(bac):
    if bac >= 0.30:
        return 'danger'
    if bac >= 0.08:
        return 'over'
    return 'ok'
