sharedFileLocations = {
    'BotToken': 'tokens/bot_token.txt',
    'ChatGPT': 'tokens/openai_key.txt',
    'Owner': 'text_files/shared/owner.txt',
    'Admins': 'text_files/shared/admins.txt',
    'Pokemon': 'text_files/shared/pokemon.txt',
    'PoGoPokemon': 'text_files/shared/pogo_pokemon.txt',
    'ShinyDays': 'text_files/shared/shiny_days.txt'
}

sharedImagePaths = {
    'Shuckle': 'https://i.imgur.com/N4RHrVQ.png',
    'ShinyShuckle': 'https://i.imgur.com/vwke1vY.png'
}

sharedEmbedColours = {
    'Default': 3553598
}

reactionEmojis = {
    'Shuckle': {
        'Normal': '<:SwoleShuckle:1187641763960205392>',
        'Shiny': '<:ShinySwoleShuckle:1188674339260878941>'
    },
    'Soul Links': {
        'Normal': '<:SwoleShuckle:1187641763960205392>',
        'Shiny': '<:ShinySwoleShuckle:1188674339260878941>'
    },
    'Routes': {
        'Normal': '<:Zygarde_Cell:1231761804032610384>',
        'Shiny': '<:Zygarde_Cell:1231761804032610384>'
    },
    'DPS': {
        'Normal': '<:SwoleShuckle:1187641763960205392>',
        'Shiny': '<:ShinySwoleShuckle:1188674339260878941>'
    },
    'Max': {
        'Normal': '<:SwoleShuckle:1187641763960205392>',
        'Shiny': '<:ShinySwoleShuckle:1188674339260878941>'
    },
    'PoGo': {
        'Normal': '<:SwoleShuckle:1187641763960205392>',
        'Shiny': '<:ShinySwoleShuckle:1188674339260878941>'
    },
    'PVP': {
        'Normal': '<:SwoleShuckle:1187641763960205392>',
        'Shiny': '<:ShinySwoleShuckle:1188674339260878941>'
    },
    'Minecraft': {
        'Normal': '<:AmberShuckle:1323169451033759745>',
        'Shiny': '<:AmberShinyShuckle:1323169482964996160>'
    },
    'Coins': {
        'Normal': '<:Gimmighoul:1386804101865668658>',
        'Shiny': '<:ShinyGimmighoul:1386804181670564032>'
    },
    'Mimikyu': {
        'Normal': '<:Mimikyu:1412302913715310695>',
        'Shiny': '<:ShinyMimikyu:1412302939447361616>'
    }
}

types = [
    {'Name': 'Normal', 'Colour': 9542306, 'Emoji': {
                                                    'Physical': 1187545017695338576,
                                                    'Special': 1432948785041903667,
                                                    'Status': 1432948803031273664
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': set(),
                                                                        'NotVery': {'Rock', 'Steel'},
                                                                        'Immune': {'Ghost'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Fighting'},
                                                                        'NotVery': set(),
                                                                        'Immune': {'Ghost'}
                                                                    }}},
    {'Name': 'Fighting', 'Colour': 13581929, 'Emoji': {
                                                    'Physical': 1187558808915025961,
                                                    'Special': 1432948829304524930,
                                                    'Status': 1432948895465472175
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Normal', 'Rock', 'Steel', 'Ice', 'Dark'},
                                                                        'NotVery': {'Flying', 'Poison', 'Bug', 'Psychic', 'Fairy'},
                                                                        'Immune': {'Ghost'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Flying', 'Psychic', 'Fairy'},
                                                                        'NotVery': {'Rock', 'Bug', 'Dark'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Flying', 'Colour': 9480670, 'Emoji': {
                                                    'Physical': 1187558754057723935,
                                                    'Special': 1432948916579602534,
                                                    'Status': 1432948941955137657
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Fighting', 'Bug', 'Grass'},
                                                                        'NotVery': {'Rock', 'Electric', 'Steel'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Rock', 'Electric', 'Ice'},
                                                                        'NotVery': {'Fighting', 'Bug', 'Grass'},
                                                                        'Immune': {'Ground'}
                                                                    }}},
    {'Name': 'Poison', 'Colour': 11299529, 'Emoji': {
                                                    'Physical': 1187558708012662907,
                                                    'Special': 1432948999844794459,
                                                    'Status': 1432949020896264242
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Grass', 'Poison'},
                                                                        'NotVery': {'Poison', 'Ground', 'Rock', 'Ghost'},
                                                                        'Immune': {'Steel'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Ground', 'Psychic'},
                                                                        'NotVery': {'Fighting', 'Poison', 'Grass', 'Bug', 'Fairy'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Ground', 'Colour': 14317636, 'Emoji': {
                                                    'Physical': 1187558659639738439,
                                                    'Special': 1432949064164573195,
                                                    'Status': 1432949085861580831
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Poison', 'Rock', 'Fire', 'Electric', 'Steel'},
                                                                        'NotVery': {'Bug', 'Grass'},
                                                                        'Immune': {'Flying'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Water', 'Grass', 'Ice'},
                                                                        'NotVery': {'Poison', 'Rock'},
                                                                        'Immune': {'Electric'}
                                                                    }}},
    {'Name': 'Rock', 'Colour': 13154444, 'Emoji': {
                                                    'Physical': 1187558613590495333,
                                                    'Special': 1432949112176775218,
                                                    'Status': 1432949140903563366
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Flying', 'Bug', 'Fire', 'Ice'},
                                                                        'NotVery': {'Fighting', 'Ground', 'Steel'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Fighting', 'Ground', 'Water', 'Grass', 'Steel'},
                                                                        'NotVery': {'Normal', 'Flying', 'Poison', 'Fire'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Bug', 'Colour': 9552424, 'Emoji': {
                                                    'Physical': 1187558577313939456,
                                                    'Special': 1432949189897224283,
                                                    'Status': 1432949207509106791
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Grass', 'Psychic', 'Dark'},
                                                                        'NotVery': {'Fighting', 'Flying', 'Poison', 'Ghost', 'Steel', 'Fire', 'Fairy'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Flying', 'Rock', 'Fire'},
                                                                        'NotVery': {'Fighting', 'Ground', 'Grass'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Ghost', 'Colour': 5335470, 'Emoji': {
                                                    'Physical': 1187558536008441916,
                                                    'Special': 1432949239297740810,
                                                    'Status': 1432949260005019658
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Ghost', 'Psychic'},
                                                                        'NotVery': {'Dark'},
                                                                        'Immune': {'Normal'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Ghost', 'Dark'},
                                                                        'NotVery': {'Poison', 'Bug'},
                                                                        'Immune': {'Normal', 'Fighting'}
                                                                    }}},
    {'Name': 'Steel', 'Colour': 5869474, 'Emoji': {
                                                    'Physical': 1187558497836081152,
                                                    'Special': 1432949385800716298,
                                                    'Status': 1432949406528700526
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Rock', 'Ice', 'Fairy'},
                                                                        'NotVery': {'Steel', 'Fire', 'Water', 'Electric'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Fighting', 'Ground', 'Fire'},
                                                                        'NotVery': {'Normal', 'Flying', 'Rock', 'Bug', 'Steel', 'Grass', 'Psychic', 'Ice', 'Dragon', 'Fairy'},
                                                                        'Immune': {'Poison'}
                                                                    }}},
    {'Name': 'Grass', 'Colour': 6536283, 'Emoji': {
                                                    'Physical': 1187558444941717604,
                                                    'Special': 1432949424333525032,
                                                    'Status': 1432949455308456016
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Ground', 'Rock', 'Water'},
                                                                        'NotVery': {'Flying', 'Poison', 'Bug', 'Steel', 'Grass', 'Fire', 'Dragon'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Flying', 'Poison', 'Bug', 'Fire', 'Ice'},
                                                                        'NotVery': {'Ground', 'Grass', 'Water', 'Electric'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Fire', 'Colour': 16751955, 'Emoji': {
                                                    'Physical': 1187544873251909674,
                                                    'Special': 1432949504537002066,
                                                    'Status': 1432949526292861100
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Bug', 'Steel', 'Grass', 'Ice'},
                                                                        'NotVery': {'Rock', 'Fire', 'Water', 'Dragon'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Ground', 'Rock', 'Water'},
                                                                        'NotVery': {'Bug', 'Steel', 'Grass', 'Fire', 'Ice', 'Fairy'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Water', 'Colour': 5018070, 'Emoji': {
                                                    'Physical': 1187558409390784512,
                                                    'Special': 1432949547302129705,
                                                    'Status': 1432949569603240040
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Ground', 'Rock', 'Fire'},
                                                                        'NotVery': {'Grass', 'Water', 'Dragon'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Grass', 'Electric'},
                                                                        'NotVery': {'Steel', 'Fire', 'Water', 'Ice'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Electric', 'Colour': 15979320, 'Emoji': {
                                                    'Physical': 1187558371293933568,
                                                    'Special': 1432949632329318500,
                                                    'Status': 1432949657788747871
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Flying', 'Water'},
                                                                        'NotVery': {'Grass', 'Electric', 'Dragon'},
                                                                        'Immune': {'Ground'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Ground'},
                                                                        'NotVery': {'Flying', 'Steel', 'Electric'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Psychic', 'Colour': 16347767, 'Emoji': {
                                                    'Physical': 1187558330705641532,
                                                    'Special': 1432949692496482444,
                                                    'Status': 1432949704932724748
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Fighting', 'Poison'},
                                                                        'NotVery': {'Steel', 'Psychic'},
                                                                        'Immune': {'Dark'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Bug', 'Ghost', 'Dark'},
                                                                        'NotVery': {'Fighting', 'Psychic'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Ice', 'Colour': 7720897, 'Emoji': {
                                                    'Physical': 1187558296824057876,
                                                    'Special': 1432949718417145856,
                                                    'Status': 1432949734565347399
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Flying', 'Ground', 'Grass', 'Dragon'},
                                                                        'NotVery': {'Steel', 'Fire', 'Water', 'Ice'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Fighting', 'Rock', 'Steel', 'Fire'},
                                                                        'NotVery': {'Ice'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Dragon', 'Colour': 224709, 'Emoji': {
                                                    'Physical': 1187558252758708234,
                                                    'Special': 1432949763913027675,
                                                    'Status': 1432949785639260181
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Dragon'},
                                                                        'NotVery': {'Steel'},
                                                                        'Immune': {'Fairy'}
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Ice', 'Dragon', 'Fairy'},
                                                                        'NotVery': {'Grass', 'Fire', 'Water', 'Electric'},
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Dark', 'Colour': 5919334, 'Emoji': {
                                                    'Physical': 1187558208760447066,
                                                    'Special': 1432949812176752791,
                                                    'Status': 1432949830162059285
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Ghost', 'Psychic'},
                                                                        'NotVery': {'Fighting', 'Dark', 'Fairy'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Fighting', 'Bug', 'Fairy'},
                                                                        'NotVery': {'Ghost', 'Dark'},
                                                                        'Immune': {'Psychic'}
                                                                    }}},
    {'Name': 'Fairy', 'Colour': 15569127, 'Emoji': {
                                                    'Physical': 1187558167937294346,
                                                    'Special': 1432949875582173225,
                                                    'Status': 1432949888345444424
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': {'Fighting', 'Dragon', 'Dark'},
                                                                        'NotVery': {'Poison', 'Steel', 'Fire'},
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': {'Poison', 'Steel'},
                                                                        'NotVery': {'Fighting', 'Bug', 'Dark'},
                                                                        'Immune': {'Dragon'}
                                                                    }}},
    {'Name': '???', 'Colour': 6856848, 'Emoji': {
                                                    'Physical': 1187590001970663526,
                                                    'Special': 1187590001970663526,
                                                    'Status': 1187590001970663526
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': set(),
                                                                        'NotVery': set(),
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': set(),
                                                                        'NotVery': set(),
                                                                        'Immune': set()
                                                                    }}},
    {'Name': 'Stellar', 'Colour': 4187077, 'Emoji': {
                                                    'Physical': 1374499968508755998,
                                                    'Special': 1374499968508755998,
                                                    'Status': 1374499968508755998
                                                    },'TypeChart':{
                                                                    'Attacking': {
                                                                        'Super': set(),
                                                                        'NotVery': set(),
                                                                        'Immune': set()
                                                                    }, 
                                                                    'Defending': {
                                                                        'Super': set(),
                                                                        'NotVery': set(),
                                                                        'Immune': set()
                                                                    }}},
]

categories = [
    {'Name': 'Physical', 'Emoji': '<:_:1187586750139351100>'},
    {'Name': 'Special', 'Emoji': '<:_:1187586794242457703>'},
    {'Name': 'Status', 'Emoji': '<:_:1187586830539964426>'}
]

pogoCPMultipliers = {
    1.0:	0.0939999967813491,
    1.5:	0.135137430784308,
    2.0:	0.166397869586944,
    2.5:	0.192650914456886,
    3.0:	0.215732470154762,
    3.5:	0.236572655026622,
    4.0:	0.255720049142837,
    4.5:	0.273530381100769,
    5.0:	0.29024988412857,
    5.5:	0.306057381335773,
    6.0:	0.321087598800659,
    6.5:	0.335445032295077,
    7.0:	0.349212676286697,
    7.5:	0.36245774877879,
    8.0:	0.375235587358474,
    8.5:	0.387592411085168,
    9.0:	0.399567276239395,
    9.5:	0.41119354951725,
    10.0:	0.422500014305114,
    10.5:	0.432926413410414,
    11.0:	0.443107545375824,
    11.5:	0.453059953871985,
    12.0:	0.46279838681221,
    12.5:	0.472336077786704,
    13.0:	0.481684952974319,
    13.5:	0.490855810259008,
    14.0:	0.499858438968658,
    14.5:	0.508701756943992,
    15.0:	0.517393946647644,
    15.5:	0.525942508771329,
    16.0:	0.534354329109191,
    16.5:	0.542635762230353,
    17.0:	0.550792694091796,
    17.5:	0.558830599438087,
    18.0:	0.566754519939422,
    18.5:	0.574569148039264,
    19.0:	0.582278907299041,
    19.5:	0.589887911977272,
    20.0:	0.59740000963211,
    20.5:	0.604823657502073,
    21.0:	0.61215728521347,
    21.5:	0.61940411056605,
    22.0:	0.626567125320434,
    22.5:	0.633649181622743,
    23.0:	0.640652954578399,
    23.5:	0.647580963301656,
    24.0:	0.654435634613037,
    24.5:	0.661219263506722,
    25.0:	0.667934000492096,
    25.5:	0.674581899290818,
    26.0:	0.681164920330047,
    26.5:	0.687684905887771,
    27.0:	0.694143652915954,
    27.5:	0.700542893277978,
    28.0:	0.706884205341339,
    28.5:	0.713169102333341,
    29.0:	0.719399094581604,
    29.5:	0.725575616972598,
    30.0:	0.731700003147125,
    30.5:	0.734741011137376,
    31.0:	0.737769484519958,
    31.5:	0.740785574597326,
    32.0:	0.743789434432983,
    32.5:	0.746781208702482,
    33.0:	0.749761044979095,
    33.5:	0.752729105305821,
    34.0:	0.75568550825119,
    34.5:	0.758630366519684,
    35.0:	0.761563837528228,
    35.5:	0.764486065255226,
    36.0:	0.767397165298461,
    36.5:	0.77029727397159,
    37.0:	0.77318650484085,
    37.5:	0.776064945942412,
    38.0:	0.778932750225067,
    38.5:	0.781790064808426,
    39.0:	0.784636974334716,
    39.5:	0.787473583646825,
    40.0:	0.790300011634826,
    40.5:	0.792803950958807,
    41.0:	0.795300006866455,
    41.5:	0.79780392148697,
    42.0:	0.800300002098083,
    42.5:	0.802803892322847,
    43.0:	0.805299997329711,
    43.5:	0.807803863460723,
    44.0:	0.81029999256134,
    44.5:	0.812803834895026,
    45.0:	0.815299987792968,
    45.5:	0.817803806620319,
    46.0:	0.820299983024597,
    46.5:	0.822803778631297,
    47.0:	0.825299978256225,
    47.5:	0.827803750922782,
    48.0:	0.830299973487854,
    48.5:	0.832803753381377,
    49.0:	0.835300028324127,
    49.5:	0.837803755931569,
    50.0:	0.840300023555755,
    50.5:	0.842803729034748,
    51.0:	0.845300018787384,
    51.5:   0.847803702398935,
    52.0:   0.850300014019012,
    52.5:   0.852803676019539,
    53.0:   0.85530000925064,
    53.5:   0.857803649892077,
    54.0:   0.860300004482269,
    54.5:   0.862803624012168,
    55.0:   0.865299999713897
}