sharedFileLocations = {
    'ChatGPT': 'tokens/openai_key.txt',
    'Pokemon': 'text_files/shared/pokemon.txt'
}

sharedImagePaths = {
    'Shuckle': 'https://i.imgur.com/N4RHrVQ.png',
    'ShinyShuckle': 'https://i.imgur.com/vwke1vY.png'
}

types = [
    {'Name': 'Normal', 'Colour': 9542306, 'Emoji': '<:_:1187545017695338576>', 'TypeChart': {
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
    {'Name': 'Fighting', 'Colour': 13581929, 'Emoji': '<:_:1187558808915025961>', 'TypeChart': {
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
    {'Name': 'Flying', 'Colour': 9480670, 'Emoji': '<:_:1187558754057723935>', 'TypeChart': {
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
    {'Name': 'Poison', 'Colour': 11299529, 'Emoji': '<:_:1187558708012662907>', 'TypeChart': {
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
    {'Name': 'Ground', 'Colour': 14317636, 'Emoji': '<:_:1187558659639738439>', 'TypeChart': {
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
    {'Name': 'Rock', 'Colour': 13154444, 'Emoji': '<:_:1187558613590495333>', 'TypeChart': {
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
    {'Name': 'Bug', 'Colour': 9552424, 'Emoji': '<:_:1187558577313939456>', 'TypeChart': {
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
    {'Name': 'Ghost', 'Colour': 5335470, 'Emoji': '<:_:1187558536008441916>', 'TypeChart': {
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
    {'Name': 'Steel', 'Colour': 5869474, 'Emoji': '<:_:1187558497836081152>', 'TypeChart': {
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
    {'Name': 'Grass', 'Colour': 6536283, 'Emoji': '<:_:1187558444941717604>', 'TypeChart': {
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
    {'Name': 'Fire', 'Colour': 16751955, 'Emoji': '<:_:1187544873251909674>', 'TypeChart': {
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
    {'Name': 'Water', 'Colour': 5018070, 'Emoji': '<:_:1187558409390784512>', 'TypeChart': {
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
    {'Name': 'Electric', 'Colour': 15979320, 'Emoji': '<:_:1187558371293933568>', 'TypeChart': {
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
    {'Name': 'Psychic', 'Colour': 16347767, 'Emoji': '<:_:1187558330705641532>', 'TypeChart': {
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
    {'Name': 'Ice', 'Colour': 7720897, 'Emoji': '<:_:1187558296824057876>', 'TypeChart': {
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
    {'Name': 'Dragon', 'Colour': 224709, 'Emoji': '<:_:1187558252758708234>', 'TypeChart': {
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
    {'Name': 'Dark', 'Colour': 5919334, 'Emoji': '<:_:1187558208760447066>', 'TypeChart': {
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
    {'Name': 'Fairy', 'Colour': 15569127, 'Emoji': '<:_:1187558167937294346>', 'TypeChart': {
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
    {'Name': '???', 'Colour': 6856848, 'Emoji': '<:_:1187590001970663526>', 'TypeChart': {
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
    {'Name': 'Stellar', 'Colour': 4187077, 'Emoji': '<:_:1374499968508755998>', 'TypeChart': {
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