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

pokemonClassifications = {
    'Regions': [
        {'Name': 'kanto', 'Gen': 1, 'DexNums': [(1, 151), (10033, 10044), 10071, 10073, (10080, 10085), 
                                                10090, (10094, 10099), 10148, (10158, 10160), (10195, 10206), (10278, 10281), 10304, 10305]},
        {'Name': 'johto', 'Gen': 2, 'DexNums': [(152, 251), (10045, 10049), 10072, (10282, 10284)]},
        {'Name': 'hoenn', 'Gen': 3, 'DexNums': [(252, 386), (10001, 10003), (10013, 10015), (10050, 10057), 
                                                (10062, 10067), 10070, 10074, (10076, 10079), 10087, 10089, 10306, 10307]},
        {'Name': 'sinnoh', 'Gen': 4, 'DexNums': [(387, 492), (10004, 10012), (10058, 10060), 10068, 10088, 10245, 10246, 10285, (10308, 10312)]},
        {'Name': 'unova', 'Gen': 5, 'DexNums': [(494, 649), (10016, 10024), 10069, 10207, (10286, 10291), 10313]},
        {'Name': 'kalos', 'Gen': 6, 'DexNums': [(650, 721), (10025, 10032), 10061, 10075, 10086, (10116, 10120), (10292, 10301), 10314]},
        {'Name': 'alola', 'Gen': 7, 'DexNums': [(722, 809), (10091, 10093), (10100, 10115), (10121, 10147), 
                                                (10149, 10157), 10208, 10302, (10315, 10319)]},
        {'Name': 'galar', 'Gen': 8, 'DexNums': [(810, 898), (10161, 10194), (10209, 10228), 10303]},
        {'Name': 'hisui', 'Gen': 8, 'DexNums': [(899, 905), (10229, 10244), (10247, 10249)]},
        {'Name': 'paldea', 'Gen': 9, 'DexNums': [(906, 1025), (10250, 10277), (10320, 10325)]}
    ],
    'PoGoRegional': [83, 115, 10039, 122, 128, 214, 10047, 222, 313, 314, 324, (335, 338), 
                     357, 369, 417, 422, 423, 439, 441, 455, (480, 482), (511, 516), 538, 539, 550, 10016, 
                     556, 561, 626, 631, 632, (669, 671), 701, 10300, 707, 741, (10123, 10125), 
                     764, (794, 798), 805, 806, 874, 931, 10260, (10250, 10252), 978, 10258, 10259, (10322, 10324)],
    'PoGoRare': [201, 235, 292, 327, 352, 442, 448, 10059, 10310, 479, (10008, 10012), (551, 553), 621, 636, 637, (679, 681),
                  744, 745, 10126, 10152, 749, 750, 757, 758, 776, 780, 781, 843, 844, 10218, 849, 10219, 10184, 10228, 10173, (845, 847), 864, 
                  10168, 866, 872, 873, 876, 10186, 877, 884, 10225, 1018, 899, 900, 10247, 902, 10248, 924, 925, 10257,
                  (935, 937), 944, 945, 950, 955, 956, 962, 965, 966, 968, 969, 970, 10321, 977, (10250, 10252), 
                  978, 10258, 10259, (10322, 10324), 10255, 1012, 1013, 10233, 10236, 10244, 10237, 10240, 10243],

    'Starters': [(1, 9), (10033, 10036), (10195, 10197), (152, 160), 10282, 10283, (252, 260), 10050, 10064, 10065, (387, 394), 
                 (495, 503), 10286, (650, 658), (10292, 10294), (722, 730), (810, 818), (10209, 10211), (906, 914), 10233, 10236, 10244],
    'Baby': [(172, 175), 236, (238, 240), 298, 360, 406, 433, (438, 440), 446, 447, 458, 848],
    'Legendary': [(144, 146), (10169, 10171), 150, 10043, 10044, (243, 245), 249, 250, (377, 384), 10062, 10063, 
                   (10077, 10079), (480, 488), 10245, 10246, 10007, 10311, (638, 646), (10019, 10023), 716, 717, (10118, 10120), 10301, 
                   772, 773, (785, 792), (10155, 10157), 800, (888, 892), (10188, 10191), 10226, 10227, (894, 898), 10193, 10194,
                   905, 10249, (1001, 1004), 1007, 1008, 1009, 1010, (1014, 1017), (1020, 1023), 1024, (10273, 10277)],
    'Mythical': [151, 251, 385, 386, (10001, 10003), (489, 494), 10006, 10312, (647, 649), 10018, 10024, 10061, 10296, (719, 721), 10075, 10086,
                  801, 802, 10147, (10317, 10319), (807, 809), 10208, 893, 10192, 1025],
    'UltraBeast': [(793, 799), (803, 806)],
    'Paradox': [(984, 995), 1005, 1006, 1009, 1010, (1020, 1023)],
    'Mega': [(10033, 10060), (10062, 10076), (10077, 10079), (10087, 10090), (10278, 10325)],
    'HasMega': [10118, 10119],
    'Gigantamax': [(10195, 10228), 10190],
    'HasGigantamax': [],
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

pogoLevels = {
    1.0:	{'PowerUp': {'Stardust': 200, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.0939999967813491},
    1.5:	{'PowerUp': {'Stardust': 200, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.135137430784308},
    2.0:	{'PowerUp': {'Stardust': 200, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.166397869586944},
    2.5:	{'PowerUp': {'Stardust': 200, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.192650914456886},
    3.0:	{'PowerUp': {'Stardust': 400, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.215732470154762},
    3.5:	{'PowerUp': {'Stardust': 400, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.236572655026622},
    4.0:	{'PowerUp': {'Stardust': 400, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.255720049142837},
    4.5:	{'PowerUp': {'Stardust': 400, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.273530381100769},
    5.0:	{'PowerUp': {'Stardust': 600, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.29024988412857},
    5.5:	{'PowerUp': {'Stardust': 600, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.306057381335773},
    6.0:	{'PowerUp': {'Stardust': 600, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.321087598800659},
    6.5:	{'PowerUp': {'Stardust': 600, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.335445032295077},
    7.0:	{'PowerUp': {'Stardust': 800, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.349212676286697},
    7.5:	{'PowerUp': {'Stardust': 800, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.36245774877879},
    8.0:	{'PowerUp': {'Stardust': 800, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.375235587358474},
    8.5:	{'PowerUp': {'Stardust': 800, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.387592411085168},
    9.0:	{'PowerUp': {'Stardust': 1000, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.399567276239395},
    9.5:	{'PowerUp': {'Stardust': 1000, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.41119354951725},
    10.0:	{'PowerUp': {'Stardust': 1000, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.422500014305114},
    10.5:	{'PowerUp': {'Stardust': 1000, 'Candy': 1, 'CandyXL': 0}, 'CPM': 0.432926413410414},
    11.0:	{'PowerUp': {'Stardust': 1300, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.443107545375824},
    11.5:	{'PowerUp': {'Stardust': 1300, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.453059953871985},
    12.0:	{'PowerUp': {'Stardust': 1300, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.46279838681221},
    12.5:	{'PowerUp': {'Stardust': 1300, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.472336077786704},
    13.0:	{'PowerUp': {'Stardust': 1600, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.481684952974319},
    13.5:	{'PowerUp': {'Stardust': 1600, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.490855810259008},
    14.0:	{'PowerUp': {'Stardust': 1600, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.499858438968658},
    14.5:	{'PowerUp': {'Stardust': 1600, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.508701756943992},
    15.0:	{'PowerUp': {'Stardust': 1900, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.517393946647644},
    15.5:	{'PowerUp': {'Stardust': 1900, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.525942508771329},
    16.0:	{'PowerUp': {'Stardust': 1900, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.534354329109191},
    16.5:	{'PowerUp': {'Stardust': 1900, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.542635762230353},
    17.0:	{'PowerUp': {'Stardust': 2200, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.550792694091796},
    17.5:	{'PowerUp': {'Stardust': 2200, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.558830599438087},
    18.0:	{'PowerUp': {'Stardust': 2200, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.566754519939422},
    18.5:	{'PowerUp': {'Stardust': 2200, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.574569148039264},
    19.0:	{'PowerUp': {'Stardust': 2500, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.582278907299041},
    19.5:	{'PowerUp': {'Stardust': 2500, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.589887911977272},
    20.0:	{'PowerUp': {'Stardust': 2500, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.59740000963211},
    20.5:	{'PowerUp': {'Stardust': 2500, 'Candy': 2, 'CandyXL': 0}, 'CPM': 0.604823657502073},
    21.0:	{'PowerUp': {'Stardust': 3000, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.61215728521347},
    21.5:	{'PowerUp': {'Stardust': 3000, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.61940411056605},
    22.0:	{'PowerUp': {'Stardust': 3000, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.626567125320434},
    22.5:	{'PowerUp': {'Stardust': 3000, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.633649181622743},
    23.0:	{'PowerUp': {'Stardust': 3500, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.640652954578399},
    23.5:	{'PowerUp': {'Stardust': 3500, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.647580963301656},
    24.0:	{'PowerUp': {'Stardust': 3500, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.654435634613037},
    24.5:	{'PowerUp': {'Stardust': 3500, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.661219263506722},
    25.0:	{'PowerUp': {'Stardust': 4000, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.667934000492096},
    25.5:	{'PowerUp': {'Stardust': 4000, 'Candy': 3, 'CandyXL': 0}, 'CPM': 0.674581899290818},
    26.0:	{'PowerUp': {'Stardust': 4000, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.681164920330047},
    26.5:	{'PowerUp': {'Stardust': 4000, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.687684905887771},
    27.0:	{'PowerUp': {'Stardust': 4500, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.694143652915954},
    27.5:	{'PowerUp': {'Stardust': 4500, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.700542893277978},
    28.0:	{'PowerUp': {'Stardust': 4500, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.706884205341339},
    28.5:	{'PowerUp': {'Stardust': 4500, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.713169102333341},
    29.0:	{'PowerUp': {'Stardust': 5000, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.719399094581604},
    29.5:	{'PowerUp': {'Stardust': 5000, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.725575616972598},
    30.0:	{'PowerUp': {'Stardust': 5000, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.731700003147125},
    30.5:	{'PowerUp': {'Stardust': 5000, 'Candy': 4, 'CandyXL': 0}, 'CPM': 0.734741011137376},
    31.0:	{'PowerUp': {'Stardust': 6000, 'Candy': 6, 'CandyXL': 0}, 'CPM': 0.737769484519958},
    31.5:	{'PowerUp': {'Stardust': 6000, 'Candy': 6, 'CandyXL': 0}, 'CPM': 0.740785574597326},
    32.0:	{'PowerUp': {'Stardust': 6000, 'Candy': 6, 'CandyXL': 0}, 'CPM': 0.743789434432983},
    32.5:	{'PowerUp': {'Stardust': 6000, 'Candy': 6, 'CandyXL': 0}, 'CPM': 0.746781208702482},
    33.0:	{'PowerUp': {'Stardust': 7000, 'Candy': 8, 'CandyXL': 0}, 'CPM': 0.749761044979095},
    33.5:	{'PowerUp': {'Stardust': 7000, 'Candy': 8, 'CandyXL': 0}, 'CPM': 0.752729105305821},
    34.0:	{'PowerUp': {'Stardust': 7000, 'Candy': 8, 'CandyXL': 0}, 'CPM': 0.75568550825119},
    34.5:	{'PowerUp': {'Stardust': 7000, 'Candy': 8, 'CandyXL': 0}, 'CPM': 0.758630366519684},
    35.0:	{'PowerUp': {'Stardust': 8000, 'Candy': 10, 'CandyXL': 0}, 'CPM': 0.761563837528228},
    35.5:	{'PowerUp': {'Stardust': 8000, 'Candy': 10, 'CandyXL': 0}, 'CPM': 0.764486065255226},
    36.0:	{'PowerUp': {'Stardust': 8000, 'Candy': 10, 'CandyXL': 0}, 'CPM': 0.767397165298461},
    36.5:	{'PowerUp': {'Stardust': 8000, 'Candy': 10, 'CandyXL': 0}, 'CPM': 0.77029727397159},
    37.0:	{'PowerUp': {'Stardust': 9000, 'Candy': 12, 'CandyXL': 0}, 'CPM': 0.77318650484085},
    37.5:	{'PowerUp': {'Stardust': 9000, 'Candy': 12, 'CandyXL': 0}, 'CPM': 0.776064945942412},
    38.0:	{'PowerUp': {'Stardust': 9000, 'Candy': 12, 'CandyXL': 0}, 'CPM': 0.778932750225067},
    38.5:	{'PowerUp': {'Stardust': 9000, 'Candy': 12, 'CandyXL': 0}, 'CPM': 0.781790064808426},
    39.0:	{'PowerUp': {'Stardust': 10000, 'Candy': 15, 'CandyXL': 0}, 'CPM': 0.784636974334716},
    39.5:	{'PowerUp': {'Stardust': 10000, 'Candy': 15, 'CandyXL': 0}, 'CPM': 0.787473583646825},
    40.0:	{'PowerUp': {'Stardust': 10000, 'Candy': 0, 'CandyXL': 10}, 'CPM': 0.790300011634826},
    40.5:	{'PowerUp': {'Stardust': 10000, 'Candy': 0, 'CandyXL': 10}, 'CPM': 0.792803950958807},
    41.0:	{'PowerUp': {'Stardust': 11000, 'Candy': 0, 'CandyXL': 10}, 'CPM': 0.795300006866455},
    41.5:	{'PowerUp': {'Stardust': 11000, 'Candy': 0, 'CandyXL': 10}, 'CPM': 0.79780392148697},
    42.0:	{'PowerUp': {'Stardust': 11000, 'Candy': 0, 'CandyXL': 12}, 'CPM': 0.800300002098083},
    42.5:	{'PowerUp': {'Stardust': 11000, 'Candy': 0, 'CandyXL': 12}, 'CPM': 0.802803892322847},
    43.0:	{'PowerUp': {'Stardust': 12000, 'Candy': 0, 'CandyXL': 12}, 'CPM': 0.805299997329711},
    43.5:	{'PowerUp': {'Stardust': 12000, 'Candy': 0, 'CandyXL': 12}, 'CPM': 0.807803863460723},
    44.0:	{'PowerUp': {'Stardust': 12000, 'Candy': 0, 'CandyXL': 15}, 'CPM': 0.81029999256134},
    44.5:	{'PowerUp': {'Stardust': 12000, 'Candy': 0, 'CandyXL': 15}, 'CPM': 0.812803834895026},
    45.0:	{'PowerUp': {'Stardust': 13000, 'Candy': 0, 'CandyXL': 15}, 'CPM': 0.815299987792968},
    45.5:	{'PowerUp': {'Stardust': 13000, 'Candy': 0, 'CandyXL': 15}, 'CPM': 0.817803806620319},
    46.0:	{'PowerUp': {'Stardust': 13000, 'Candy': 0, 'CandyXL': 17}, 'CPM': 0.820299983024597},
    46.5:	{'PowerUp': {'Stardust': 13000, 'Candy': 0, 'CandyXL': 17}, 'CPM': 0.822803778631297},
    47.0:	{'PowerUp': {'Stardust': 14000, 'Candy': 0, 'CandyXL': 17}, 'CPM': 0.825299978256225},
    47.5:	{'PowerUp': {'Stardust': 14000, 'Candy': 0, 'CandyXL': 17}, 'CPM': 0.827803750922782},
    48.0:	{'PowerUp': {'Stardust': 14000, 'Candy': 0, 'CandyXL': 20}, 'CPM': 0.830299973487854},
    48.5:	{'PowerUp': {'Stardust': 14000, 'Candy': 0, 'CandyXL': 20}, 'CPM': 0.832803753381377},
    49.0:	{'PowerUp': {'Stardust': 15000, 'Candy': 0, 'CandyXL': 20}, 'CPM': 0.835300028324127},
    49.5:	{'PowerUp': {'Stardust': 15000, 'Candy': 0, 'CandyXL': 20}, 'CPM': .837803755931569},
    50.0:	{'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.840300023555755},
    50.5:	{'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.842803729034748},
    51.0:	{'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.845300018787384},
    51.5:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.847803702398935},
    52.0:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.850300014019012},
    52.5:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': .852803676019539},
    53.0:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.85530000925064},
    53.5:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.857803649892077},
    54.0:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.860300004482269},
    54.5:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': 0.862803624012168},
    55.0:   {'PowerUp': {'Stardust': 0, 'Candy': 0, 'CandyXL': 0}, 'CPM': .865299999713897}
}