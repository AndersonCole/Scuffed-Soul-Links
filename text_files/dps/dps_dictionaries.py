defaultModifiers = {
    'EnemyDpsScaling': 4.0,
    'ExtraDpsValue': 0.5,

    'Level': {
        'raids': 50.0,
        'dmax': 40.0
    },
    'Ivs': {
        'Attack': 15,
        'Defence': 15,
        'Stamina': 15,
    },

    'FastEffectiveness': 1.0,
    'ChargedEffectiveness': 1.0,

    'ForceNoFastSTAB': False,
    'ForceFastSTAB': False,
    'FastSTABMultiplier': 1.0,

    'ForceNoChargedSTAB': False,
    'ForceChargedSTAB': False,
    'ChargedSTABMultiplier': 1.0,
    'ApplyEnergyPenalty': True,

    'ShadowMultiplier': 1.0,
    'ShadowText': '',
    
    'FriendMultiplier': 1.0,
    'WeatherMultiplier': 1.0,
    'MegaMultiplier': 1.0,
    'PartyPowerMultiplier': 1.0,
    'PowerSpotMultiplier': 1.0,
    'MushroomMultiplier': 1.0,
    'ZacianMultiplier': 1.0,
    'ZamazentaMultiplier': 1.0,


    'MaxEffectiveness': 1.0,
    'MaxSTABMultiplier': 1.2,
    'MaxMovePower': 300,
    'GMaxText': '',
    'MaxMoveText': 'Lv 2 DMax ',

    'ShowCycleDps': False,
    'CycleWillSwap': False,
    'CycleSwapMon': [],
    'CycleSwapMonLevel': 40.0,
    'CycleSwapMonIvs': {
        'Attack': 15,
        'Defence': 15,
        'Stamina': 15
    },

    'CyclePlayers': 1.0,

    'BossAttack': 200,
    'BossDefence': 70,
    'BossHealth': 15_000.0,

    'CpmMultiplier': 1.0,
    'UseCpmMultiplier': True,
    'SimFastAlone': True,
    'ApplyMaxOrb': True,

    'ShowMoveTimings': False,
    'ShowMoveChanges': False,
    'ApplyMoveChanges': True,

    'ShowOldDps': False,
    'ResultSortOrder': {
        'raids': 'ByNewDps',
        'dmax': 'ByMaxEps',
        'dmax-cycle': 'ByDps'
    }
}

activeModifiers = {
    'ShadowMultiplier': 1.2,

    'FriendMultiplier': 1.1,
    'WeatherMultiplier': 1.2,
    'MegaMultiplier': 1.3,

    'STABMultiplier': {
        'active': 1.2,
        'inactive': 1.0
    },

    'PowerSpotMultiplier': {
        '1': 1.1,
        '2': 1.15,
        '3': 1.188,
        '4': 1.2,
    },
    'MushroomMultiplier': 2.0,

    'MaxMovePower': {
        'dmax': {
            '1': 250,
            '2': 300,
            '3': 350
        },
        'gmax': {
            '1': 350,
            '2': 400,
            '3': 450
        }
    },

    #gives 10 energy, but to dodge into it loses time, therefore 9 energy is a better approx
    'MaxOrbEnergy': 9.0,

    'ZacianMultiplier': 1.2,
    'ZamazentaMultiplier': 1.2,
}

battleTierStats = {
    '1': {
        'raids':  {
            'bossHealth': 600.0,
            'cpmMultiplier': 0.5974
        },
        'dmax': {
            'bossHealth': 1700.0,
            'cpmMultiplier': 0.15
        }
    },
    '2': {
        'dmax': {
            'bossHealth': 5000.0,
            'cpmMultiplier': 0.38
        }
    },
    '3': {
        'raids':  {
            'bossHealth': 3600.0,
            'cpmMultiplier': 0.73
        },
        'dmax': {
            'bossHealth': 10_000.0,
            'cpmMultiplier': 0.5
        }
    },
    '4': {
        'raids':  {
            'bossHealth': 9000.0,
            'cpmMultiplier': 0.73
        },
        'dmax': {
            'bossHealth': 20_000.0,
            'cpmMultiplier': 0.6
        }
    },
    '5': {
        'raids':  {
            'bossHealth': 15_000.0,
            'cpmMultiplier': 0.79
        },
        'dmax': {
            'bossHealth': 17_500.0,
            'cpmMultiplier': 0.699
        }
    },
    '6': {
        'raids':  {
            'bossHealth': 20_000.0,
            'cpmMultiplier': 0.79
        },
        'dmax': {
            'bossHealth': 60_000.0,
            'cpmMultiplier': 0.85
        }
    },
    'mega': {
        'raids':  {
            'bossHealth': 20_000.0,
            'cpmMultiplier': 0.79
        }
    },
    'gmax': {
        'dmax': {
            'bossHealth': 90_000.0,
            'cpmMultiplier': 0.85
        }
    }
}

cpMultipliers = {
    1.0:	0.094,
    1.5:	0.135137432,
    2.0:	0.16639787,
    2.5:	0.192650919,
    3.0:	0.21573247,
    3.5:	0.236572661,
    4.0:	0.25572005,
    4.5:	0.273530381,
    5.0:	0.29024988,
    5.5:	0.306057378,
    6.0:	0.3210876,
    6.5:	0.335445036,
    7.0:	0.34921268,
    7.5:	0.362457751,
    8.0:	0.3752356,
    8.5:	0.387592416,
    9.0:	0.39956728,
    9.5:	0.411193551,
    10.0:	0.4225,
    10.5:	0.432926409,
    11.0:	0.44310755,
    11.5:	0.453059959,
    12.0:	0.4627984,
    12.5:	0.472336093,
    13.0:	0.48168495,
    13.5:	0.4908558,
    14.0:	0.49985844,
    14.5:	0.508701765,
    15.0:	0.51739395,
    15.5:	0.525942511,
    16.0:	0.5343543,
    16.5:	0.542635738,
    17.0:	0.5507927,
    17.5:	0.558830586,
    18.0:	0.5667545,
    18.5:	0.574569133,
    19.0:	0.5822789,
    19.5:	0.589887907,
    20.0:	0.5974,
    20.5:	0.604823665,
    21.0:	0.6121573,
    21.5:	0.619404122,
    22.0:	0.6265671,
    22.5:	0.633649143,
    23.0:	0.64065295,
    23.5:	0.647580967,
    24.0:	0.65443563,
    24.5:	0.661219252,
    25.0:	0.667934,
    25.5:	0.674581896,
    26.0:	0.6811649,
    26.5:	0.687684904,
    27.0:	0.69414365,
    27.5:	0.70054287,
    28.0:	0.7068842,
    28.5:	0.713169109,
    29.0:	0.7193991,
    29.5:	0.725575614,
    30.0:	0.7317,
    30.5:	0.734741009,
    31.0:	0.7377695,
    31.5:	0.740785594,
    32.0:	0.74378943,
    32.5:	0.746781211,
    33.0:	0.74976104,
    33.5:	0.752729087,
    34.0:	0.7556855,
    34.5:	0.758630368,
    35.0:	0.76156384,
    35.5:	0.764486065,
    36.0:	0.76739717,
    36.5:	0.770297266,
    37.0:	0.7731865,
    37.5:	0.776064962,
    38.0:	0.77893275,
    38.5:	0.781790055,
    39.0:	0.784637,
    39.5:	0.787473608,
    40.0:	0.7903,
    40.5:	0.792803968,
    41.0:	0.79530001,
    41.5:	0.797800015,
    42.0:	0.8003,
    42.5:	0.802799995,
    43.0:	0.8053,
    43.5:	0.8078,
    44.0:	0.81029999,
    44.5:	0.812799985,
    45.0:	0.81529999,
    45.5:	0.81779999,
    46.0:	0.82029999,
    46.5:	0.82279999,
    47.0:	0.82529999,
    47.5:	0.82779999,
    48.0:	0.83029999,
    48.5:	0.83279999,
    49.0:	0.83529999,
    49.5:	0.83779999,
    50.0:	0.84029999,
    50.5:	0.84279999,
    51.0:	0.84529999
}