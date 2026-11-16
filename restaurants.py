"""
Places and their drink menus. These are placeholder names; swap in real
restaurants and bars. Each drink is {'ounces': ..., 'abv_percent': ...},
the same format as drink_menu.py.

Water is added to every menu automatically, so don't list it here.
"""

from drink_menu import DRINK_MENU

WATER = {'ounces': 8, 'abv_percent': 0}
WATER_NAME = 'water / no drink'

RESTAURANTS = {
    'honeycomb-taproom': {
        'name': 'The Honeycomb Taproom',
        'kind': 'Brewery and taproom',
        'menu': {
            'house lager': {'ounces': 16, 'abv_percent': 4.8},
            'hazy ipa': {'ounces': 16, 'abv_percent': 6.8},
            'double ipa': {'ounces': 12, 'abv_percent': 8.5},
            'hard seltzer': {'ounces': 12, 'abv_percent': 5},
            'cider': {'ounces': 12, 'abv_percent': 6},
        },
    },
    'blue-hive-lounge': {
        'name': 'Blue Hive Lounge',
        'kind': 'Cocktail bar',
        # 'ounces' is the whole drink; abv_percent is for the mixed drink
        'menu': {
            'margarita': {'ounces': 4, 'abv_percent': 20},
            'old fashioned': {'ounces': 3, 'abv_percent': 32},
            'mojito': {'ounces': 6, 'abv_percent': 13},
            'espresso martini': {'ounces': 4, 'abv_percent': 22},
            'long island iced tea': {'ounces': 8, 'abv_percent': 22},
        },
    },
    'stingers-sports-grill': {
        'name': "Stinger's Sports Grill",
        'kind': 'Sports bar and grill',
        # Your original drink menu
        'menu': DRINK_MENU,
    },
    'meadow-wine-kitchen': {
        'name': 'Meadow Wine Kitchen',
        'kind': 'Restaurant and wine bar',
        'menu': {
            'red wine': {'ounces': 5, 'abv_percent': 13.5},
            'white wine': {'ounces': 5, 'abv_percent': 12},
            'rosé': {'ounces': 5, 'abv_percent': 12},
            'prosecco': {'ounces': 5, 'abv_percent': 11},
            'sangria': {'ounces': 8, 'abv_percent': 9},
        },
    },
}


def menu_for(restaurant_id):
    """The place's drinks with water listed last."""
    place = RESTAURANTS.get(restaurant_id)
    if place is None:
        return None
    return {**place['menu'], WATER_NAME: WATER}
