"""
Notebook 3: the BAC calculator, same math as main(), split into functions
so the website can call it instead of using input()/print().
"""

from datetime import datetime

ELIMINATION = 0.015  # BAC drop per hour

SYMPTOMS = [
    'Vomiting',
    'Seizures',
    'Irregular breathing',
    'Low body temperature',
    'Trouble staying awake',
    'Blue, gray, pale or clammy skin',
]


def hours_since_last(profile, now=None):
    """Hours since the last calculation. First calculation = infinity (all drinks count)."""
    if profile['last_calculation'] is None:
        return float('inf')
    now = now or datetime.now()
    last = datetime.fromisoformat(profile['last_calculation'])
    return (now - last).total_seconds() / 3600


def bac_now(profile, now=None):
    """Prior BAC minus what the body has burned off since then."""
    time_since = hours_since_last(profile, now)
    return max(0.0, profile['prior_bac'] - ELIMINATION * time_since)


def drink_bac(ounces, abv_percent, weight, r, hours_ago):
    pure_alc = ounces * (abv_percent / 100)
    bac = (pure_alc * 5.14) / (weight * r)
    bac -= ELIMINATION * hours_ago
    # A drink that has fully worn off adds 0; it shouldn't subtract from the others
    return max(0.0, bac)


def calculate(profile, drinks, menu, now=None):
    """
    Run one calculation, like one pass of main().
    drinks: list of {'name': str, 'hours_ago': float}
    Returns (new_bac, skipped_drink_names). Updates the profile in place.
    """
    now = now or datetime.now()
    time_since = hours_since_last(profile, now)
    current = bac_now(profile, now)
    skipped = []

    for d in drinks:
        item = menu.get(d['name'])
        if item is None:
            skipped.append(d['name'])
            continue
        if item['abv_percent'] == 0:
            # Water / no drink: adds nothing, but the calculation still
            # runs, so the time spent resting is subtracted
            continue
        if d['hours_ago'] > time_since:
            # Consumed before the previous calculation, already counted
            skipped.append(d['name'])
            continue
        current += drink_bac(item['ounces'], item['abv_percent'],
                             profile['weight'], profile['r'], d['hours_ago'])

    current = max(0.0, current)
    profile['prior_bac'] = current
    profile['last_calculation'] = now.isoformat()
    return current, skipped


def hours_until(bac, target=0.0):
    """Roughly how many hours until BAC falls to `target` at 0.015 per hour."""
    return max(0.0, (bac - target) / ELIMINATION)


def format_hours(hours):
    total_min = int(round(hours * 60))
    h, m = divmod(total_min, 60)
    if h and m:
        return f'{h} h {m} min'
    return f'{h} h' if h else f'{m} min'


def status(bac):
    if bac >= 0.30:
        return 'danger'
    if bac >= 0.08:
        return 'over'
    return 'estimate'
