dpsFileLocations = {
    'Moves': 'text_files/dps/moves.txt',
    'Notes': 'text_files/dps/notes.txt',
    'UserModifiers': 'text_files/dps/user_modifiers.txt'
}

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
    'CalculateFastEffectiveness': True,
    'CalculateChargedEffectiveness': True,

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

    'WeatherTypes': [],
    'FastWeatherMultiplier': 1.0,
    'ChargedWeatherMultiplier': 1.0,

    'ApplyMegaBoost': False,
    'MegaTypes': [],
    'FastMegaMultiplier': 1.0,
    'ChargedMegaMultiplier': 1.0,

    'PartyPowerGain': 0.0,
    'PowerSpotMultiplier': 1.0,
    'MushroomMultiplier': 1.0,

    'UsingAdventureEffect': False,
    'ZacianMultiplier': 1.0,
    'ZamazentaMultiplier': 1.0,

    'MaxEffectiveness': 1.0,
    'MaxSTABMultiplier': 1.2,
    'MaxMovePower': 300,
    'GMaxText': '',
    'MaxMoveText': 'Lv 2 DMax ',

    'CyclePlayers': 1.0,
    'ShowCycleDps': False,
    'CycleWillSwap': False,
    'CycleSwapMon': {
        'Name': '',
        'ImageDexNum': -1,
        'Level': 40.0,
        'Stats': {
            'Attack': 0,
            'Defence': 0,
            'Stamina': 0
        },
        'Ivs': {
            'Attack': 15,
            'Defence': 15,
            'Stamina': 15
        }
    },

    'Boss': {
        'DexNum': -1,
        'Tier': -1,
        
        'Stats': {
            'Attack': 200,
            'Defence': 70,
            'Health': 15_000.0
        },

        'Cpm': 1.0,
        'UseCpmMultiplier': True,
        'AttackMultiplier': 1.0,
        'EnergyMultiplier': 1.0
    },

    'SimFastAlone': True,
    'ApplyMaxOrb': True,
    'UseNewMaxFormula': True,
    
    'UsingFunnyMove50': False,
    'UsingFunnyMove100': False,

    'ResultSortOrder': {
        'raids': 'ByDps',
        'dmax': 'ByMaxEps',
        'dmax-cycle': 'ByDps'
    }
}

activeModifiers = {
    'TypeEffectiveness': {
        'Super': 1.6,
        'NotVery': 0.625
    },

    'STABMultiplier': {
        'active': 1.2,
        'inactive': 1.0
    },
    
    'ShadowMultiplier': 1.2,

    'FriendMultiplier': 1.12,
    'WeatherMultiplier': {
        'active': 1.2,
        'inactive': 1.0
    },
    'MegaMultiplier': {
        'SameType': 1.3,
        'DiffType': 1.1
    },

    'PartyPowerReadyAt': 36.0,
    #amount of energy each fast move gives towards party power energy
    'PartyPowerGain': {
        '2': 2.0, #18 atks
        '3': 4.0, #9 atks
        '4': 6.0 #6  atks
    },

    'PowerSpotMultiplier': {
        '1': 1.1,
        '2': 1.15,
        '3': 1.188,
        '4': 1.2,
    },
    'MushroomMultiplier': 2.0,

    #4 is exclusive to eternatus' adventure effect
    'MaxMovePower': {
        'dmax': {
            '1': 250,
            '2': 300,
            '3': 350,
            '4': 450
        },
        'gmax': {
            '1': 350,
            '2': 400,
            '3': 450,
            '4': 550
        }
    },

    #gives 10 energy, but to dodge into it loses time, therefore 9 energy is a better approx
    'MaxOrbEnergy': 9.0,

    'ZacianMultiplier': {
        'raids': 1.1,
        'dmax': 1.05
    },
    'ZamazentaMultiplier': {
        'raids': 1.1,
        'dmax': 1.05
    },

    #beak blast clone
    'ModeratelyFunnyMove': {
        'Name': 'funny-move-50',
        'Type': 'Charged',
        'Damage': 125,
        'Energy': 50,
        'Duration': 2.5,
        'DamageWindow': 1.5,
        'MoveType': '???'
    },
    #dynamax cannon clone
    'VeryFunnyMove': {
        'Name': 'funny-move-100',
        'Type': 'Charged',
        'Damage': 215,
        'Energy': 100,
        'Duration': 1.5,
        'DamageWindow': 0.9,
        'MoveType': '???'
    }
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
            'cpmMultiplier': 0.79
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
            'bossHealth': 20_000.0,
            'attackMultiplier': 2.0,
            'energyMultiplier': 2.0,
            'cpmMultiplier': 0.699
        }
    },
    '6': {
        'raids':  {
            'bossHealth': 22_500.0,
            'cpmMultiplier': 0.79
        },
        'dmax': {
            'bossHealth': 60_000.0,
            'cpmMultiplier': 0.85
        }
    },
    'mega': {
        'raids':  {
            'bossHealth': 9000.0,
            'cpmMultiplier': 0.79
        }
    },
    'gmax': {
        'dmax': {
            'bossHealth': 90_000.0,
            'attackMultiplier': 0.9,
            'energyMultiplier': 15.0,
            'cpmMultiplier': 0.85
        }
    }
}

battleStatOverrides = {
    '5': {
        'dmax': {
            'articuno': {
                'bossHealth': 17_500.0
            },
            'zapdos': {
                'bossHealth': 13_000.0
            },
            'raikou': {
                'cpmMultiplier': 0.8
            },
            'entei': {
                'bossHealth': 27_000.0,
                'cpmMultiplier': 0.75
            },
            'suicune': {
                'bossHealth': 22_000.0,
                'cpmMultiplier': 0.9
            },
            'lugia': {
                'bossHealth': 18_000.0,
                'cpmMultiplier': 0.75
            },
            'ho-oh': {
                'bossHealth': 25_000.0
            },
            'latias': {
                'bossHealth': 25_000.0
            },
            'latios': {
                'bossHealth': 23_000.0,
                'cpmMultiplier': 0.75
            }
        }
    },
    'gmax': {
        'dmax': {
            'charizard': {
                'bossHealth': 70_000.0
            },
            'blastoise': {
                'bossHealth': 75_000.0
            },
            'butterfree': {
                'bossHealth': 100_000.0
            },
            'pikachu': {
                'bossHealth': 80_000.0,
                'cpmMultiplier': 1.7
            },
            'meowth': {
                'bossHealth': 80_000.0,
                'cpmMultiplier': 3.0
            },
            'machamp': {
                'bossHealth': 100_000.0,
                'cpmMultiplier': 0.8
            },
            'gengar': {
                'bossHealth': 70_000.0
            },
            'kingler': {
                'bossHealth': 100_000.0
            },
            'snorlax': {
                'bossHealth': 135_000.0,
                'cpmMultiplier': 0.65
            },
            'garbodor': {
                'bossHealth': 100_000.0,
                'cpmMultiplier': 1.4
            },
            'rillaboom': {
                'bossHealth': 120_000.0,
                'cpmMultiplier': 1.0
            },
            'cinderace': {
                'bossHealth': 80_000.0,
                'cpmMultiplier': 0.8
            },
            'inteleon': {
                'bossHealth': 100_000.0,
                'cpmMultiplier': 0.9
            },
            'toxtricity': {
                'bossHealth': 100_000.0,
                'cpmMultiplier': 0.9
            },
            'grimmsnarl': {
                'bossHealth': 120_000.0,
                'cpmMultiplier': 1.2
            },
            'eternatus': {
                'bossHealth': 60_000.0,
                'cpmMultiplier': 0.75
            },
            'eternatus-eternamax': {
                'bossHealth': 60_000.0,
                'cpmMultiplier': 0.75
            }
        }
    }
}

weather = {
    'sunny': ['Ground', 'Grass', 'Fire'],
    'clear': ['Ground', 'Grass', 'Fire'],
    'partly-cloudy': ['Normal', 'Rock'],
    'cloudy': ['Fighting', 'Poison', 'Fairy'],
    'wind': ['Flying', 'Psychic', 'Dragon'],
    'windy': ['Flying', 'Psychic', 'Dragon'],
    'rain': ['Bug', 'Water', 'Electric'],
    'rainy': ['Bug', 'Water', 'Electric'],
    'fog': ['Ghost', 'Dark'],
    'foggy': ['Ghost', 'Dark'],
    'snow': ['Ice', 'Steel'],
    'snowy': ['Ice', 'Steel']
}