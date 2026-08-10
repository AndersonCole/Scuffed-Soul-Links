pvpFileLocations = {
    'FakeR1': 'text_files/pvp/fake_rank_ones.txt',
    'Scanners': 'text_files/pvp/scanner_systems.txt'
}

defaultPvpModifiers = {
    'LeagueLimit': 1500,
    
    'Floor': 0,
    'MinLevel': 1.0,
    'MaxLevel': 50.0,

    'BaseStats': {
        'Attack': 0,
        'Defence': 0,
        'Stamina': 0
    },
    'StatText': '',

    'Rank': -1,
    'Ivs': {
        'Attack': -1,
        'Defence': -1,
        'Stamina': -1,
    },
    'Compare': False,
    'ShowPreMegaCP': False,
    'EvoToSuperMega': False,

    'ResultSortOrder': 'ByStatProduct'
}

scannerSystems = {
    'poracle': {
        'Prefixes': {
            'Start': '!track',
            'Distance': 'd',
            'Percentage': 'iv',
            'MinLevel': 'level',
            'MaxLevel': 'maxlevel',
            'MinAttack': 'atk',
            'MaxAttack': 'maxatk',
            'MinDefence': 'def',
            'MaxDefence': 'maxdef',
            'MinStamina': 'sta',
            'MaxStamina': 'maxsta',
            'Size': '',
            'Gender': '',
            'LL': 'little',
            'GL': 'great',
            'UL': 'ultra'
        },
        'TrackBaseEvo': True,
        'Separator': ' '
    }
}