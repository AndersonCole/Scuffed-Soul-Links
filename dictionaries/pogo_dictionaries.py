eventColours = {
    'event': 6148352,
    'pokemon-spotlight-hour': 15569998,
    'community-day': 1466537,
    'pokemon-go-tour': 115100,
    'pokemon-go-fest': 8135296,
    'wild-area': 14053170,
    'raid-hour': 6504051,
    'raid-battles': 5587029,
    'raid-day': 5666433,
    'raid-weekend': 5666433,
    'max-mondays': 13511011,
    'max-battles': 11866657,
    'go-battle-league': 3759832,

    'events': 6148352,
    'commdays': 1466537,
    'hourevents': 15569998,
    'raids': 6504051,
    'gbl': 3759832,
}

timezones = {
    'NZ': 'Pacific/Auckland',
    'Hawaii': 'Pacific/Honolulu'
}

filterLists = {
    'events': ['event', 'community-day', 'pokemon-go-tour', 'pokemon-go-fest', 'wild-area', 'raid-day', 'raid-weekend'],
    'commdays': ['community-day'],
    'hourevents': ['max-mondays', 'pokemon-spotlight-hour', 'raid-hour'],
    'raids': ['raid-day', 'raid-battles', 'raid-weekend', 'max-battles'],
    'gbl': ['go-battle-league']
}

defaultOddsModifiers = {
    'Ivs': {
        'Attack': 15,
        'Defence': 15,
        'Stamina': 15,
    },
    'Floor': 10,

    'BottleCap': False,
    'ShinyChance': None,
    'BackgroundChance': None,
    'ExtraChance': None,
    'LuckyChance': None
}