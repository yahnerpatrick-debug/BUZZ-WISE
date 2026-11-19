
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
        'cali-brews-mexican-grill': {
        'name': 'Cali Brews Mexican Grill',
        'kind': 'Mexican restaurant and bar',
        'menu': {
             'michelob ultra': {'ounces': 16, 'abv_percent': 4.4},
                'bud light': {'ounces': 16, 'abv_percent': 4.4},
                'modelo especial': {'ounces': 16, 'abv_percent': 5.4},
                'corona extra': {'ounces': 16, 'abv_percent': 4.6},
                'pacifico clara': {'ounces': 16, 'abv_percent': 4.4},
                'guinness': {'ounces': 16, 'abv_percent': 4.2},
        },
    },
        'darbys-american-cantina': {
        'name': "Darby's American Cantina",
        'kind': 'Restaurant and bar',
        'menu': {
                'bud light': {'ounces': 16, 'abv_percent': 4.2},
                'coors banquet': {'ounces': 16, 'abv_percent': 5.0},
                'modelo especial': {'ounces': 16, 'abv_percent': 4.6},
                'blue moon belgian white': {'ounces': 16, 'abv_percent': 5.4},
                'stone ipa': {'ounces': 16, 'abv_percent': 6.9},
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
