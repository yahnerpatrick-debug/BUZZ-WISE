
RESTAURANTS = {
        'half-moon-bay-brewing-company': {
        'name': 'Half Moon Bay Brewing Company',
        'kind': 'Brewery and waterfront restaurant',
        'menu': {
            'kolsch': {'ounces': 16, 'abv_percent': 5.1},
            'saison': {'ounces': 16, 'abv_percent': 6.7},
            'mavericks amber ale': {'ounces': 16, 'abv_percent': 5.8},
            'half moon bay ipa': {'ounces': 16, 'abv_percent': 6.5},
        },
    },
    'blue-hive-lounge': {
        'name': 'Blue Hive Lounge',
        'kind': 'Cocktail bar',
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
        'menu': {
            'whiskey': {'ounces': 1.5, 'abv_percent': 50},
            'vodka': {'ounces': 1.5, 'abv_percent': 40},
            'rum': {'ounces': 1.5, 'abv_percent': 40},
            'beer': {'ounces': 12, 'abv_percent': 5},
            'brandy': {'ounces': 1.5, 'abv_percent': 35},
            'malibu': {'ounces': 1.5, 'abv_percent': 21},
        },
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

WATER = 'water / no drink'


def get_menu(place_id):
    if place_id not in RESTAURANTS:
        return None
    menu = dict(RESTAURANTS[place_id]['menu'])
    menu[WATER] = {'ounces': 8, 'abv_percent': 0}
    return menu
