soulLinksFileLocations = {
    'Runs': 'text_files/soul_links/runs.txt'
}

defaultRun = {
    'VersionGroup': '',
    'RunName': '',
}

gens = [
    {'Name': 1, 'SerebiiLink': '', 'RomanNumeral': 'i', 'VersionGroups': [{'Name': 'red-blue'}, {'Name': 'yellow'}, {'Name': 'red-green-japan'}, {'Name': 'blue-japan'}]},
    {'Name': 2, 'SerebiiLink': '-gs', 'RomanNumeral': 'ii', 'VersionGroups': [{'Name': 'gold-silver'}, {'Name': 'crystal'}]},
    {'Name': 3, 'SerebiiLink': '-rs', 'RomanNumeral': 'iii', 'VersionGroups': [{'Name': 'ruby-sapphire'}, {'Name': 'emerald'}, {'Name': 'firered-leafgreen'}, {'Name': 'colosseum'}, {'Name': 'xd'}]},
    {'Name': 4, 'SerebiiLink': '-dp', 'RomanNumeral': 'iv', 'VersionGroups': [{'Name': 'diamond-pearl'}, {'Name': 'platinum'}, {'Name': 'heartgold-soulsilver'}]},
    {'Name': 5, 'SerebiiLink': '-bw', 'RomanNumeral': 'v', 'VersionGroups': [{'Name': 'black-white'}, {'Name': 'black-2-white-2'}]},
    {'Name': 6, 'SerebiiLink': '-xy', 'RomanNumeral': 'vi', 'VersionGroups': [{'Name': 'x-y'}, {'Name': 'omega-ruby-alpha-sapphire'}]},
    {'Name': 7, 'SerebiiLink': '-sm', 'RomanNumeral': 'vii', 'VersionGroups': [{'Name': 'sun-moon'}, {'Name': 'ultra-sun-ultra-moon'}, {'Name': 'lets-go-pikachu-lets-go-eevee'}]},
    {'Name': 8, 'SerebiiLink': '-swsh', 'RomanNumeral': 'viii', 'VersionGroups': [{'Name': 'sword-shield'}, {'Name': 'the-isle-of-armor'}, {'Name': 'the-crown-tundra'}, {'Name': 'brilliant-diamond-shining-pearl'}, {'Name': 'legends-arceus'}]},
    {'Name': 9, 'SerebiiLink': '-sv', 'RomanNumeral': 'ix', 'VersionGroups': [{'Name': 'scarlet-violet'}, {'Name': 'the-teal-mask'}, {'Name': 'the-indigo-disk'}, {'Name': 'legends-za'}, {'Name': 'mega-dimension'}, {'Name': 'champions'}]}
]

'''
Gen 4, 5 and USUM are vetted to be accurate
The others are probably missing some static encounters here and there, should be double checked
'''
games = [
    {'Name': 'red-blue', 'Games': ['red', 'blue'], 'Colour': [8978434, 2314131], 'LinkEmoji': ['<:linkR:1193403535954550885>', '<:linkB:1193403571983634463>'], 'Mascot': [6, 9], 'Progression': [
            {'Stage': 0, 'BattleName': 'Brock', 'LevelCap': 14, 'Encounters': ['starter', 'pallet-town', 'route-1', 'viridian-city', 'route-22', 'route-2', 'viridian-forest']},
            {'Stage': 1, 'BattleName': 'Misty', 'LevelCap': 21, 'Encounters': ['route-3', 'route-4', 'mt-moon', 'cerulean-city']},
            {'Stage': 2, 'BattleName': 'Lt. Surge', 'LevelCap': 24, 'Encounters': ['route-24', 'route-25', 'route-5', 'route-6', 'vermillion-city']},
            {'Stage': 3, 'BattleName': 'Erika', 'LevelCap': 29, 'Encounters': ['route-11', 'digletts-cave', 'route-9', 'route-10', 'rock-tunnel', 'pokemon-tower', 'route-12', 'route-8', 'route-7', 'celadon-city']},
            {'Stage': 4, 'BattleName': 'Sabrina', 'LevelCap': 43, 'Encounters': ['saffron-city']},
            {'Stage': 5, 'BattleName': 'Koga', 'LevelCap': 43, 'Encounters': ['route-16', 'route-17', 'route-18', 'fuschia-city']},
            {'Stage': 6, 'BattleName': 'Blaine', 'LevelCap': 47, 'Encounters': ['safari-zone', 'route-15', 'route-14', 'route-13', 'power-plant', 'route-19', 'route-20', 'seafoam-islands', 'cinnabar-island', 'pokemon-mansion']},
            {'Stage': 7, 'BattleName': 'Giovanni', 'LevelCap': 50, 'Encounters': ['route-21']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 65, 'Encounters': ['route-23', 'victory-road']}
        ]},
    {'Name': 'yellow', 'Games': ['yellow'], 'Colour': [15913776], 'LinkEmoji': ['<:linkY:1193403603981959188>'], 'Mascot': [25], 'Progression': [
            {'Stage': 0, 'BattleName': 'Brock', 'LevelCap': 12, 'Encounters': ['starter', 'pallet-town', 'route-1', 'viridian-city', 'route-22', 'route-2', 'viridian-forest']},
            {'Stage': 1, 'BattleName': 'Misty', 'LevelCap': 21, 'Encounters': ['route-3', 'route-4', 'mt-moon', 'cerulean-city']},
            {'Stage': 2, 'BattleName': 'Lt. Surge', 'LevelCap': 28, 'Encounters': ['route-24', 'route-25', 'route-5', 'route-6', 'vermillion-city']},
            {'Stage': 3, 'BattleName': 'Erica', 'LevelCap': 32, 'Encounters': ['route-11', 'digletts-cave', 'route-9', 'route-10', 'rock-tunnel', 'pokemon-tower', 'route-12', 'route-8', 'route-7', 'celadon-city']},
            {'Stage': 4, 'BattleName': 'Sabrina', 'LevelCap': 50, 'Encounters': ['saffron-city']},
            {'Stage': 5, 'BattleName': 'Koga', 'LevelCap': 50, 'Encounters': ['route-16', 'route-17', 'route-18', 'fuschia-city']},
            {'Stage': 6, 'BattleName': 'Blaine', 'LevelCap': 54, 'Encounters': ['safari-zone', 'route-15', 'route-14', 'route-13', 'power-plant', 'route-19', 'route-20', 'seafoam-islands', 'cinnabar-island', 'pokemon-mansion']},
            {'Stage': 7, 'BattleName': 'Giovanni', 'LevelCap': 55, 'Encounters': ['route-21']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 65, 'Encounters': ['route-23', 'victory-road']},
        ]},
    {'Name': 'gold-silver', 'Games': ['gold', 'silver'], 'Colour': [12629117, 13422806], 'LinkEmoji': ['<:linkG:1193408037092864071>', '<:linkS:1193408117204070542>'], 'Mascot': [250, 249], 'Progression': [
            {'Stage': 0, 'BattleName': 'Falkner', 'LevelCap': 9, 'Encounters': ['starter', 'new-bark-town', 'route-29', 'cherrygrove-city', 'route-30', 'route-31', 'dark-cave', 'violet-city']},
            {'Stage': 1, 'BattleName': 'Bugsy', 'LevelCap': 16, 'Encounters': ['sprout-tower', 'route-32', 'ruins-of-alph', 'union-cave', 'route-33', 'azalea-town', 'slowpoke-well']},
            {'Stage': 2, 'BattleName': 'Whitney', 'LevelCap': 20, 'Encounters': ['ilex-forest', 'route-34', 'goldenrod-city']},
            {'Stage': 3, 'BattleName': 'Morty', 'LevelCap': 25, 'Encounters': ['route-35', 'national-park', 'route-36', 'route-37', 'ecruteak-city', 'burned-tower', 'tin-tower']},
            {'Stage': 4, 'BattleName': 'Chuck', 'LevelCap': 30, 'Encounters': ['route-38', 'route-39', 'olivine-city', 'route-40', 'route-41', 'whirl-islands', 'cianwood-city']},
            {'Stage': 5, 'BattleName': 'Jasmine', 'LevelCap': 35, 'Encounters': []},
            {'Stage': 6, 'BattleName': 'Pryce', 'LevelCap': 31, 'Encounters': ['route-42', 'mt-mortar', 'route-43', 'lake-of-rage', 'rocket-hideout']},
            {'Stage': 7, 'BattleName': 'Clair', 'LevelCap': 40, 'Encounters': ['route-44', 'ice-path', 'blackthorn-city', 'dragons-den']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 50, 'Encounters': ['route-45', 'route-46', 'route-27', 'tohjo-falls', 'route-26', 'victory-road', 'indigo-plateau']},
            {'Stage': 9, 'BattleName': 'Lt. Surge', 'LevelCap': 46, 'Encounters': ['vermillion-city']},
            {'Stage': 10, 'BattleName': 'Sabrina', 'LevelCap': 48, 'Encounters': []},
            {'Stage': 11, 'BattleName': 'Erika', 'LevelCap': 46, 'Encounters': ['route-5', 'route-7']},
            {'Stage': 12, 'BattleName': 'Misty', 'LevelCap': 47, 'Encounters': ['route-8', 'route-6', 'route-10', 'rock-tunnel', 'route-9', 'cerulean-city']},
            {'Stage': 13, 'BattleName': 'Janine', 'LevelCap': 39, 'Encounters': ['route-24', 'route-25', 'route-4', 'route-16', 'route-17', 'route-18', 'fuschia-city']},
            {'Stage': 14, 'BattleName': 'Brock', 'LevelCap': 44, 'Encounters': ['route-15', 'route-14', 'route-13', 'route-12', 'route-11', 'digletts-cave', 'route-2', 'pewter-city']},
            {'Stage': 15, 'BattleName': 'Blaine', 'LevelCap': 50, 'Encounters': ['route-3', 'mt-moon', 'viridian-city', 'route-1', 'pallet-town', 'route-21', 'cinnabar-island']},
            {'Stage': 16, 'BattleName': 'Blue', 'LevelCap': 58, 'Encounters': []},
            {'Stage': 17, 'BattleName': 'Red', 'LevelCap': 81, 'Encounters': []}
        ]},
    {'Name': 'crystal', 'Games': ['crystal'], 'Colour': [7107505], 'LinkEmoji': ['<:linkC:1193408169666420778>'], 'Mascot': [245], 'Progression': [
            {'Stage': 0, 'BattleName': 'Falkner', 'LevelCap': 9, 'Encounters': ['starter', 'new-bark-town', 'route-29', 'cherrygrove-city', 'route-30', 'route-31', 'dark-cave', 'violet-city']},
            {'Stage': 1, 'BattleName': 'Bugsy', 'LevelCap': 16, 'Encounters': ['sprout-tower', 'route-32', 'ruins-of-alph', 'union-cave', 'route-33', 'azalea-town', 'slowpoke-well']},
            {'Stage': 2, 'BattleName': 'Whitney', 'LevelCap': 20, 'Encounters': ['ilex-forest', 'route-34', 'goldenrod-city']},
            {'Stage': 3, 'BattleName': 'Morty', 'LevelCap': 25, 'Encounters': ['route-35', 'national-park', 'route-36', 'route-37', 'ecruteak-city', 'burned-tower', 'tin-tower']},
            {'Stage': 4, 'BattleName': 'Chuck', 'LevelCap': 30, 'Encounters': ['route-38', 'route-39', 'olivine-city', 'route-40', 'route-41', 'whirl-islands', 'cianwood-city']},
            {'Stage': 5, 'BattleName': 'Jasmine', 'LevelCap': 35, 'Encounters': []},
            {'Stage': 6, 'BattleName': 'Pryce', 'LevelCap': 31, 'Encounters': ['route-42', 'mt-mortar', 'route-43', 'lake-of-rage', 'rocket-hideout']},
            {'Stage': 7, 'BattleName': 'Clair', 'LevelCap': 40, 'Encounters': ['route-44', 'ice-path', 'blackthorn-city', 'dragons-den']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 50, 'Encounters': ['route-45', 'route-46', 'route-27', 'tohjo-falls', 'route-26', 'victory-road', 'indigo-plateau']},
            {'Stage': 9, 'BattleName': 'Lt. Surge', 'LevelCap': 46, 'Encounters': ['vermillion-city']},
            {'Stage': 10, 'BattleName': 'Sabrina', 'LevelCap': 48, 'Encounters': []},
            {'Stage': 11, 'BattleName': 'Erika', 'LevelCap': 46, 'Encounters': ['route-5', 'route-7']},
            {'Stage': 12, 'BattleName': 'Misty', 'LevelCap': 47, 'Encounters': ['route-8', 'route-6', 'route-10', 'rock-tunnel', 'route-9', 'cerulean-city']},
            {'Stage': 13, 'BattleName': 'Janine', 'LevelCap': 39, 'Encounters': ['route-24', 'route-25', 'route-4', 'route-16', 'route-17', 'route-18', 'fuschia-city']},
            {'Stage': 14, 'BattleName': 'Brock', 'LevelCap': 44, 'Encounters': ['route-15', 'route-14', 'route-13', 'route-12', 'route-11', 'digletts-cave', 'route-2', 'pewter-city']},
            {'Stage': 15, 'BattleName': 'Blaine', 'LevelCap': 50, 'Encounters': ['route-3', 'mt-moon', 'viridian-city', 'route-1', 'pallet-town', 'route-21', 'cinnabar-island']},
            {'Stage': 16, 'BattleName': 'Blue', 'LevelCap': 58, 'Encounters': []},
            {'Stage': 17, 'BattleName': 'Red', 'LevelCap': 81, 'Encounters': []}
        ]},
    {'Name': 'ruby-sapphire', 'Games': ['ruby', 'sapphire'], 'Colour': [14305066, 2058149], 'LinkEmoji': ['<:linkR:1193408227296170065>', '<:linkS:1193408299203301507>'], 'Mascot': [383, 382], 'Progression': [
            {'Stage': 0, 'BattleName': 'Roxanne', 'LevelCap': 15, 'Encounters': ['starter', 'littleroot-town', 'route-101', 'route-103', 'route-102', 'petalburg-city', 'route-104', 'petalburg-woods', 'rustboro-city']},
            {'Stage': 1, 'BattleName': 'Brawly', 'LevelCap': 18, 'Encounters': ['route-116', 'rusturf-tunnel', 'route-105', 'dewford-town']},
            {'Stage': 2, 'BattleName': 'Wattson', 'LevelCap': 23, 'Encounters': ['route-106', 'granite-cave', 'route-107', 'route-109', 'slateport-city', 'route-110', 'altering-cave', 'new-mauville']},
            {'Stage': 3, 'BattleName': 'Flannery', 'LevelCap': 28, 'Encounters': ['route-117', 'route-112', 'route-113', 'route-114', 'desert-underpass', 'meteor-falls', 'route-115', 'jagged-pass', 'lavaridge-town']},
            {'Stage': 4, 'BattleName': 'Norman', 'LevelCap': 31, 'Encounters': ['fiery-path', 'route-111', 'mirage-tower']},
            {'Stage': 5, 'BattleName': 'Winona', 'LevelCap': 33, 'Encounters': ['route-118', 'route-119', 'fortree-city']},
            {'Stage': 6, 'BattleName': 'Tate & Liza', 'LevelCap': 42, 'Encounters': ['route-120', 'route-121', 'safari-zone', 'route-122', 'mt-pyre', 'route-123', 'lilycove-city', 'route-124', 'mossdeep-city']},
            {'Stage': 7, 'BattleName': 'Wallace', 'LevelCap': 43, 'Encounters': ['route-125', 'shoal-cave', 'route-127', 'route-128', 'seafloor-cavern', 'route-126', 'sootopolis-city', 'cave-of-origin']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 58, 'Encounters': ['route-108', 'abandoned-ship', 'route-129', 'route-130', 'mirage-island', 'route-131', 'pacifidlog-town', 'route-132', 'route-133', 'route-134', 'ever-grande-city', 'victory-road']}
        ]},
    {'Name': 'emerald', 'Games': ['emerald'], 'Colour': [42574], 'LinkEmoji': ['<:linkE:1193408566854418484>'], 'Mascot': [384], 'Progression': [
            {'Stage': 0, 'BattleName': 'Roxanne', 'LevelCap': 15, 'Encounters': ['starter', 'littleroot-town', 'route-101', 'route-103', 'route-102', 'petalburg-city', 'route-104', 'petalburg-woods', 'rustboro-city']},
            {'Stage': 1, 'BattleName': 'Brawly', 'LevelCap': 19, 'Encounters': ['route-105', 'route-116', 'rusturf-tunnel', 'dewford-town']},
            {'Stage': 2, 'BattleName': 'Wattson', 'LevelCap': 24, 'Encounters': ['route-106', 'granite-cave', 'route-107', 'slateport-city', 'route-110', 'altering-cave']},
            {'Stage': 3, 'BattleName': 'Flannery', 'LevelCap': 29, 'Encounters': ['route-117', 'route-112', 'route-113', 'route-114', 'desert-underpass', 'meteor-falls', 'route-115', 'jagged-pass', 'lavaridge-town']},
            {'Stage': 4, 'BattleName': 'Norman', 'LevelCap': 31, 'Encounters': ['fiery-path', 'route-111', 'mirage-tower']},
            {'Stage': 5, 'BattleName': 'Winona', 'LevelCap': 33, 'Encounters': ['new-mauville', 'route-118', 'route-119', 'fortree-city', 'route-120']},
            {'Stage': 6, 'BattleName': 'Tate & Liza', 'LevelCap': 42, 'Encounters': ['route-121', 'safari-zone', 'route-122', 'mt-pyre', 'route-123', 'team-magma-hideout', 'lilycove-city', 'route-124', 'mossdeep-city']},
            {'Stage': 7, 'BattleName': 'Juan', 'LevelCap': 46, 'Encounters': ['route-125', 'shoal-cave', 'route-127', 'route-128', 'seafloor-cavern', 'route-126', 'sootopolis-city']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 58, 'Encounters': ['cave-of-origin', 'route-129', 'route-130', 'route-131', 'sky-pillar', 'pacifidlog-town', 'mirage-island', 'route-108', 'abandoned-ship', 'route-109', 'route-132', 'route-133', 'route-134', 'ever-grande-city', 'victory-road']},
            {'Stage': 9, 'BattleName': 'Steven', 'LevelCap': 78, 'Encounters': []}
        ]},
    {'Name': 'firered-leafgreen', 'Games': ['fire-red', 'leaf-green'], 'Colour': [15100211, 9947731], 'LinkEmoji': ['<:linkF:1193408619128029304>', '<:linkL:1193408671347114014>'], 'Mascot': [6, 3], 'Progression': [
            {'Stage': 0, 'BattleName': 'Brock', 'LevelCap': 14, 'Encounters': ['starter', 'pallet-town', 'route-1', 'viridian-city', 'route-22', 'route-2', 'viridian-forest']},
            {'Stage': 1, 'BattleName': 'Misty', 'LevelCap': 21, 'Encounters': ['route-3', 'route-4', 'mt-moon', 'cerulean-city']},
            {'Stage': 2, 'BattleName': 'Lt. Surge', 'LevelCap': 24, 'Encounters': ['route-24', 'route-25', 'route-5', 'route-6', 'vermillion-city']},
            {'Stage': 3, 'BattleName': 'Erika', 'LevelCap': 29, 'Encounters': ['route-11', 'digletts-cave', 'route-9', 'route-10', 'rock-tunnel', 'pokemon-tower', 'route-12', 'route-8', 'route-7', 'celadon-city']},
            {'Stage': 4, 'BattleName': 'Sabrina', 'LevelCap': 43, 'Encounters': ['saffron-city']},
            {'Stage': 5, 'BattleName': 'Koga', 'LevelCap': 43, 'Encounters': ['route-16', 'route-17', 'route-18', 'fuschia-city']},
            {'Stage': 6, 'BattleName': 'Blaine', 'LevelCap': 47, 'Encounters': ['safari-zone', 'route-15', 'route-14', 'route-13', 'power-plant', 'route-19', 'route-20', 'seafoam-islands', 'cinnabar-island', 'pokemon-mansion']},
            {'Stage': 7, 'BattleName': 'Giovanni', 'LevelCap': 50, 'Encounters': ['one-island', 'two-island', 'three-island', 'route-21']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 63, 'Encounters': ['route-23', 'victory-road']}
        ]},
    {'Name': 'diamond-pearl', 'Games': ['diamond', 'pearl'], 'Colour': [5349551, 15576266], 'LinkEmoji': ['<:linkD:1193408726498029680>', '<:linkP:1193408782076743760>'], 'Mascot': [483, 484], 'Progression': [
            {'Stage': 0, 'BattleName': 'Roark', 'LevelCap': 14, 'Encounters': ['starter', 'route-201', 'lake-verity', 'route-202', 'route-203', 'route-204', 'ravaged-path', 'route-218', 'route-219', 'twinleaf-town', 'oreburgh-gate', 'oreburgh-mine', 'route-207']}, 
            {'Stage': 1, 'BattleName': 'Gardenia', 'LevelCap': 22, 'Encounters': ['floaroma-meadow', 'route-205', 'valley-windworks', 'drifloon-static', 'eterna-forest', 'eterna-city', 'route-211', 'mt-coronet']}, 
            {'Stage': 2, 'BattleName': 'Maylene', 'LevelCap': 30, 'Encounters': ['old-chateau', 'route-206', 'wayward-cave', 'route-208', 'happiny-egg', 'route-209', 'lost-tower', 'solaceon-ruins', 'route-210', 'route-215', 'route-212', 'trophy-garden', 'pastoria-city', 'great-marsh', 'route-213', 'valor-lakefront', 'route-214', 'maniac-tunnel']}, 
            {'Stage': 3, 'BattleName': 'Crasher Wake', 'LevelCap': 30, 'Encounters': []}, 
            {'Stage': 4, 'BattleName': 'Fantina', 'LevelCap': 36, 'Encounters': ['celestic-town']}, 
            {'Stage': 5, 'BattleName': 'Byron', 'LevelCap': 39, 'Encounters': ['fuego-ironworks', 'route-220', 'route-221', 'canalave-city', 'iron-island', 'riolu-egg']},
            {'Stage': 6, 'BattleName': 'Candice', 'LevelCap': 42, 'Encounters': ['route-216', 'route-217', 'acuity-lakefront']},
            {'Stage': 7, 'BattleName': 'Volkner', 'LevelCap': 49, 'Encounters': ['lake-acuity', 'legendary-static', 'roaming-mesprit', 'lake-valor', 'azelf-static', 'uxie-static', 'route-222', 'sunnyshore-city', 'route-223', 'pokemon-league']},
            {'Stage': 8, 'BattleName': 'Pokemon League', 'LevelCap': 66, 'Encounters': ['victory-road']}
        ]},
    {'Name': 'platinum', 'Games': ['platinum'], 'Colour': [1911153], 'LinkEmoji': ['<:linkPt:1193408835759644762>'], 'Mascot': [10007], 'Progression': [
            {'Stage': 0, 'BattleName': 'Roark', 'LevelCap': 14, 'Encounters': ['starter', 'route-201', 'lake-verity', 'route-202', 'route-203', 'route-204', 'ravaged-path', 'route-218', 'route-219', 'twinleaf-town', 'oreburgh-gate', 'oreburgh-mine', 'route-207']},
            {'Stage': 1, 'BattleName': 'Gardenia', 'LevelCap': 22, 'Encounters': ['floaroma-meadow', 'route-205', 'valley-windworks', 'drifloon-static', 'eterna-forest', 'eterna-city', 'route-211', 'mt-coronet']},
            {'Stage': 2, 'BattleName': 'Fantina', 'LevelCap': 26, 'Encounters': ['old-chateau', 'rotom-static', 'togepi-egg', 'route-206', 'wayward-cave', 'route-208', 'eevee-gift']},
            {'Stage': 3, 'BattleName': 'Maylene', 'LevelCap': 32, 'Encounters': ['route-209', 'lost-tower', 'solaceon-ruins', 'route-210', 'route-215', 'porygon-gift', 'route-214', 'maniac-tunnel', 'valor-lakefront', 'route-213', 'pastoria-city', 'great-marsh', 'route-212', 'trophy-garden']},
            {'Stage': 4, 'BattleName': 'Crasher Wake', 'LevelCap': 37, 'Encounters': []},
            {'Stage': 5, 'BattleName': 'Byron', 'LevelCap': 41, 'Encounters': ['celestic-town', 'fuego-ironworks', 'route-220', 'route-221', 'canalave-city', 'iron-island', 'riolu-egg']},
            {'Stage': 6, 'BattleName': 'Candice', 'LevelCap': 44, 'Encounters': ['route-216', 'route-217', 'acuity-lakefront']},
            {'Stage': 7, 'BattleName': 'Volkner', 'LevelCap': 50, 'Encounters': ['lake-acuity', 'sendoff-spring', 'roaming-mesprit', 'lake-valor', 'azelf-static', 'uxie-static', 'route-222', 'sunnyshore-city', 'route-223', 'pokemon-league']},
            {'Stage': 8, 'BattleName': 'Pokemon League', 'LevelCap': 62, 'Encounters': ['victory-road']}
        ]},
    {'Name': 'heartgold-soulsilver', 'Games': ['heart-gold', 'soul-silver'], 'Colour': [14398266, 11778238], 'LinkEmoji': ['<:linkHG:1193408899198500876>', '<:linkSS:1193409003661828178>'], 'Mascot': [250, 249], 'Progression': [
            {'Stage': 0, 'BattleName': 'Falkner', 'LevelCap': 13, 'Encounters': ['starter', 'route-29', 'route-46', 'route-30', 'route-31', 'dark-cave', 'sprout-tower', 'ruins-of-alph', 'route-32', 'mareep-egg', 'wooper-egg', 'slugma-egg']},
            {'Stage': 1, 'BattleName': 'Bugsy', 'LevelCap': 17, 'Encounters': ['togepi-egg', 'new-bark-town', 'cherrygrove-city', 'violet-city', 'union-cave', 'route-33', 'ilex-forest', 'slowpoke-well']},
            {'Stage': 2, 'BattleName': 'Whitney', 'LevelCap': 19, 'Encounters': ['azalea-town', 'route-34', 'spearow-gift', 'route-35', 'national-park', 'route-36']},
            {'Stage': 3, 'BattleName': 'Morty', 'LevelCap': 25, 'Encounters': ['sudowoodo-static', 'route-37', 'ecruteak-city', 'burned-tower', 'roaming-raikou', 'roaming-entei', 'eevee-gift', 'route-42', 'mt-mortar', 'route-38', 'route-39', 'olivine-city', 'route-40']},
            {'Stage': 4, 'BattleName': 'Chuck', 'LevelCap': 31, 'Encounters': ['lapras-static', 'route-41', 'cianwood-city', 'shuckle-gift', 'route-43', 'lake-of-rage', 'gyarados-static', 'rocket-hq', 'electrode-static', 'route-27', 'tohjo-falls']},
            {'Stage': 5, 'BattleName': 'Pryce', 'LevelCap': 34, 'Encounters': ['route-47', 'cliff-cave', 'route-48', 'safari-zone-gate', 'safari-zone']},
            {'Stage': 6, 'BattleName': 'Jasmine', 'LevelCap': 35, 'Encounters': []},
            {'Stage': 7, 'BattleName': 'Claire', 'LevelCap': 41, 'Encounters': ['whirl-islands', 'route-44', 'ice-path', 'blackthorn-city', 'route-45']},
            {'Stage': 8, 'BattleName': 'Pokemon League', 'LevelCap': 50, 'Encounters': ['dragons-den', 'dratini-gift', 'tyrogue-gift', 'bell-tower', 'legendary-static', 'route-26', 'victory-road']},
            {'Stage': 9, 'BattleName': 'Blue', 'LevelCap': 60, 'Encounters': ['vermillion-city', 'route-6', 'route-7', 'route-5', 'route-8', 'celadon-city', 'route-16', 'route-17', 'route-18', 'fuchsia-city', 'route-15', 'route-14', 'route-13', 'route-12', 'route-11', 'rock-tunnel', 'route-9', 'route-10', 'cerulean-city', 'route-4', 'route-24', 'route-25', 'suicune-static', 'snorlax-static', 'digletts-cave', 'route-2', 'pewter-city', 'route-3', 'mt-moon', 'viridian-forest', 'viridian-city', 'route-22', 'route-1', 'pallet-town', 'route-21', 'cinnabar-island', 'seafoam-islands', 'articuno-static', 'route-20', 'route-19', 'roaming-lati']},
            {'Stage': 10, 'BattleName': 'Red', 'LevelCap': 84, 'Encounters': ['cliff-edge-gate', 'zapdos-static', 'moltres-static', 'cerulean-cave', 'mewtwo-static', 'other-legendary-static', 'route-28', 'mt-silver', 'mt-silver-cave']}
        ]},
    {'Name': 'black-white', 'Games': ['black', 'white'], 'Colour': [0, 16777215], 'LinkEmoji': ['<:linkB:1193409050709340192>', '<:linkW:1193409098058834011>'], 'Mascot': [644, 643], 'Progression': [
            {'Stage': 0, 'BattleName': 'Chilli/Cilan/Cress', 'LevelCap': 14, 'Encounters': ['starter', 'route-1', 'route-2', 'monkey-gift']},
            {'Stage': 1, 'BattleName': 'Lenora', 'LevelCap': 20, 'Encounters': ['dreamyard', 'route-3', 'wellspring-cave', 'pinwheel-forest']},
            {'Stage': 2, 'BattleName': 'Burgh', 'LevelCap': 23, 'Encounters': ['route-4']},
            {'Stage': 3, 'BattleName': 'Elesa', 'LevelCap': 27, 'Encounters': ['desert-resort', 'darmanitan-static', 'relic-castle', 'route-5', 'rouet-16', 'lostlorn-forest']},
            {'Stage': 4, 'BattleName': 'Clay', 'LevelCap': 31, 'Encounters': ['driftveil-drawbridge', 'cold-storage', 'route-6']},
            {'Stage': 5, 'BattleName': 'Skyla', 'LevelCap': 35, 'Encounters': ['chargestone-cave', 'route-7', 'celestial-tower']},
            {'Stage': 6, 'BattleName': 'Brycen', 'LevelCap': 39, 'Encounters': ['route-17', 'p2-lab', 'route-18', 'larvesta-egg', 'striton-city', 'driftveil-city', 'mistralton-cave', 'cobalion-static', 'virizion-static', 'twist-mountain', 'icirrus-city', 'route-8', 'moor-of-icirrus']},
            {'Stage': 7, 'BattleName': 'Drayden/Iris', 'LevelCap': 43, 'Encounters': ['dragonspiral-tower', 'route-9', 'route-10']},
            {'Stage': 8, 'BattleName': 'Pokemon League', 'LevelCap': 50, 'Encounters': ['roaming-genie', 'victory-road', 'terrakion-static']},
            {'Stage': 9, 'BattleName': 'N\'s Castle', 'LevelCap': 54, 'Encounters': ['legendary-static']}
        ]},
    {'Name': 'black-2-white-2', 'Games': ['black-2', 'white-2'], 'Colour': [4421539, 15960922], 'LinkEmoji': ['<:linkB2:1193409150726713434>', '<:linkW2:1193409195626741832>'], 'Mascot': [10022, 10023], 'Progression': [
            {'Stage': 0, 'BattleName': 'Cheren', 'LevelCap': 13, 'Encounters': ['starter', 'route-19', 'route-20', 'floccesy-ranch']},
            {'Stage': 1, 'BattleName': 'Roxie', 'LevelCap': 18, 'Encounters': ['virbank-complex']},
            {'Stage': 2, 'BattleName': 'Burgh', 'LevelCap': 24, 'Encounters': ['castelia-sewers', 'castelia-city', 'relic-passage', 'route-4']},
            {'Stage': 3, 'BattleName': 'Elesa', 'LevelCap': 30, 'Encounters': ['bird-static', 'desert-resort', 'relic-castle', 'route-16', 'lostlorn-forest', 'route-5']},
            {'Stage': 4, 'BattleName': 'Clay', 'LevelCap': 33, 'Encounters': ['driftveil-drawbridge', 'route-6', 'deerling-gift', 'chargestone-cave']},
            {'Stage': 5, 'BattleName': 'Skyla', 'LevelCap': 39, 'Encounters': ['aspertia-city', 'virbank-city', 'volcarona-static', 'mistralton-cave', 'route-7', 'celestial-tower']},
            {'Stage': 6, 'BattleName': 'Drayden', 'LevelCap': 48, 'Encounters': ['reversal-mountain', 'strange-house', 'undella-town', 'undella-bay', 'jellicent-static', 'seaside-cave', 'route-14', 'route-13', 'cobalion-static', 'route-12', 'village-bridge', 'route-11', 'virizion-static', 'route-9']},
            {'Stage': 7, 'BattleName': 'Marlon', 'LevelCap': 51, 'Encounters': ['route-21', 'humilau-city', 'route-22', 'giant-chasm']},
            {'Stage': 8, 'BattleName': 'Pokemon League', 'LevelCap': 59, 'Encounters': ['terrakion-static', 'crustle-static', 'route-23', 'victory-road', 'abundant-shrine']}
        ]},
    {'Name': 'x-y', 'Games': ['x', 'y'], 'Colour': [90013, 13839173], 'LinkEmoji': ['<:linkX:1193409239406870698>', '<:linkY:1193409280896933988>'], 'Mascot': [716, 717], 'Progression': [
            {'Stage': 0, 'BattleName': 'Viola', 'LevelCap': 12, 'Encounters': ['starter', 'route-2', 'santalune-forest']},
            {'Stage': 1, 'BattleName': 'Grant', 'LevelCap': 25, 'Encounters': ['route-3', 'route-22', 'route-4', 'lumiose-city', 'route-5', 'route-6', 'parfum-palace', 'route-7', 'connecting-cave', 'route-8', 'ambrette-town', 'route-9', 'glittering-cave', 'cyllage-city']},
            {'Stage': 2, 'BattleName': 'Korrina', 'LevelCap': 32, 'Encounters': ['route-10', 'route-11', 'reflection-cave', 'shalour-city', 'tower-of-mystery']},
            {'Stage': 3, 'BattleName': 'Ramos', 'LevelCap': 34, 'Encounters': ['route-12', 'azure-bay']},
            {'Stage': 4, 'BattleName': 'Clemont', 'LevelCap': 37, 'Encounters': ['route-13']},
            {'Stage': 5, 'BattleName': 'Valerie', 'LevelCap': 42, 'Encounters': ['route-14', 'laverre-city']},
            {'Stage': 6, 'BattleName': 'Olympia', 'LevelCap': 48, 'Encounters': ['route-15', 'lost-hotel', 'route-16', 'frost-cavern', 'route-17']},
            {'Stage': 7, 'BattleName': 'Wulfric', 'LevelCap': 59, 'Encounters': ['team-flare-secret-hq', 'route-18', 'couriway-town', 'route-19', 'route-20', 'pokã©mon-village']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 68, 'Encounters': ['route-21', 'victory-road']}
        ]},
    {'Name': 'omega-ruby-alpha-sapphire', 'Games': ['omega-ruby', 'alpha-sapphire'], 'Colour': [12452683, 2568359], 'LinkEmoji': ['<:linkOR:1193409326400929832>', '<:linkAS:1193409376891969646>'], 'Mascot': [10078, 10077], 'Progression': [
            {'Stage': 0, 'BattleName': 'Roxanne City', 'LevelCap': 14, 'Encounters': ['starter', 'route-101', 'route-102', 'route-103', 'petalburg-city', 'route-104', 'petalburg-woods', 'rustboro-city']},
            {'Stage': 1, 'BattleName': 'Brawly', 'LevelCap': 16, 'Encounters': ['route-105', 'route-116', 'rusturf-tunnel', 'dewford-town']},
            {'Stage': 2, 'BattleName': 'Wattson', 'LevelCap': 21, 'Encounters': ['route-106', 'granite-cave', 'route-107', 'slateport-city', 'route-110', 'new-mauville']},
            {'Stage': 3, 'BattleName': 'Flannery', 'LevelCap': 28, 'Encounters': ['route-117', 'verdanturf-town', 'route-111', 'route-112', 'fiery-path', 'route-113', 'fallarbor-town', 'route-114', 'meteor-falls', 'route-115', 'jagged-pass', 'lavaridge-town']},
            {'Stage': 4, 'BattleName': 'Norman', 'LevelCap': 30, 'Encounters': []},
            {'Stage': 5, 'BattleName': 'Winona', 'LevelCap': 35, 'Encounters': ['route-118', 'southern-island', 'route-119', 'fortree-city']},
            {'Stage': 6, 'BattleName': 'Tate & Liza', 'LevelCap': 45, 'Encounters': ['route-120', 'scorched-slab', 'route-121', 'route-122', 'mt-pyre', 'route-123', 'safari-zone', 'lilycove-city', 'team-magma-hideout', 'route-124', 'mossdeep-city']},
            {'Stage': 7, 'BattleName': 'Wallace', 'LevelCap': 46, 'Encounters': ['route-125', 'shoal-cave', 'route-127', 'route-128', 'seafloor-cavern', 'route-126', 'sootopolis-city']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 59, 'Encounters': ['cave-of-origin', 'soaring', 'route-129', 'route-130', 'route-131', 'sky-pillar', 'edge-of-space', 'pacifidlog-town', 'mirage-island', 'route-108', 'sea-mauville', 'route-109', 'route-132', 'route-133', 'route-134', 'ever-grande-city', 'victory-road']}
        ]},
    {'Name': 'sun-moon', 'Games': ['sun', 'moon'], 'Colour': [16094243, 2205919], 'LinkEmoji': ['<:linkSu:1193409452691423242>', '<:linkMo:1193409503790633023>'], 'Mascot': [791, 792], 'Progression': [
            {'Stage': 0, 'BattleName': 'Ilima', 'LevelCap': 10, 'Encounters': ['starter', 'hau-oli-outskirts', 'route-1', 'trainers-school', 'hau-oli-city']},
            {'Stage': 1, 'BattleName': 'Normal Trial', 'LevelCap': 12, 'Encounters': ['route-2', 'verdant-cavern', 'berry-fields']},
            {'Stage': 2, 'BattleName': 'Kahuna Hala', 'LevelCap': 15, 'Encounters': ['hau-oli-cemetery', 'route-3', 'melemele-meadow', 'seaward-cave']},
            {'Stage': 3, 'BattleName': 'Water Trial', 'LevelCap': 20, 'Encounters': ['hau-oli-city', 'kala-e-bay', 'ten-carat-hill', 'route-4', 'paniola-town', 'paniola-ranch', 'route-5', 'brooklet-hill']},
            {'Stage': 4, 'BattleName': 'Fire Trial', 'LevelCap': 22, 'Encounters': ['route-6', 'route-7', 'wela-volcano-park']},
            {'Stage': 5, 'BattleName': 'Grass Trial', 'LevelCap': 24, 'Encounters': ['melemele-sea', 'route-8', 'fossil-restoration-center', 'lush-jungle']},
            {'Stage': 6, 'BattleName': 'Kahuna Olivia', 'LevelCap': 26, 'Encounters': ['digletts-tunnel', 'route-9', 'konikoni-city', 'memorial-hill', 'akala-outskirts']},
            {'Stage': 7, 'BattleName': 'Electric Trial', 'LevelCap': 29, 'Encounters': ['hano-beach', 'malie-city', 'malie-garden', 'route-10', 'mount-hokulani']},
            {'Stage': 8, 'BattleName': 'Ghost Trial', 'LevelCap': 33, 'Encounters': ['route-11', 'route-12', 'secluded-shore', 'blush-mountain', 'route-13', 'tapu-village', 'route-15', 'aether-house', 'route-14', 'thrify-megamart']},
            {'Stage': 9, 'BattleName': 'Kahuna Nanu', 'LevelCap': 39, 'Encounters': ['route-16', 'ula-ula-meadow', 'lake-of-the-moone', 'route-17']},
            {'Stage': 10, 'BattleName': 'Kahuna Hapu', 'LevelCap': 48, 'Encounters': ['haina-desert', 'seafolk-village', 'poni-wilds', 'ancient-poni-path', 'poni-breaker-coast', 'exeggutor-island']},
            {'Stage': 11, 'BattleName': 'Dragon Trial', 'LevelCap': 45, 'Encounters': ['vast-poni-canyon']},
            {'Stage': 12, 'BattleName': 'Elite Four', 'LevelCap': 58, 'Encounters': ['altar-of-the-sunne', 'mount-lanakila']}
        ]},
    {'Name': 'ultra-sun-ultra-moon', 'Games': ['ultra-sun', 'ultra-moon'], 'Colour': [11492140, 5188451], 'LinkEmoji': ['<:linkUS:1193409578281488405>', '<:linkUM:1193409621843529860>'], 'Mascot': [10155, 10156], 'Progression': [
            {'Stage': 0, 'BattleName': 'Normal Trial', 'LevelCap': 12, 'Encounters': ['starter', 'route-1', 'trainers-school', 'hau-oli-city', 'route-2', 'hau-oli-cemetery', 'sandy-cave']},
            {'Stage': 1, 'BattleName': 'Kahuna Hala', 'LevelCap': 16, 'Encounters': ['verdant-cavern', 'route-3', 'melemele-meadow', 'seaward-cave']},
            {'Stage': 2, 'BattleName': 'Water Trial', 'LevelCap': 20, 'Encounters': ['ten-carat-hill', 'route-4', 'paniola-ranch', 'route-5', 'brooklet-hill', 'melemele-sea', 'kala-e-bay']},
            {'Stage': 3, 'BattleName': 'Fire Trial', 'LevelCap': 22, 'Encounters': ['paniola-town', 'route-6', 'route-7', 'wela-volcano-park', 'digletts-tunnel']},
            {'Stage': 4, 'BattleName': 'Grass Trial', 'LevelCap': 24, 'Encounters': ['dividing-peak-tunnel', 'route-8', 'fossil-static']},
            {'Stage': 5, 'BattleName': 'Kahuna Olivia', 'LevelCap': 28, 'Encounters': ['lush-jungle', 'route-9', 'memorial-hill', 'akala-outskirts']},
            {'Stage': 6, 'BattleName': 'Electric Trial', 'LevelCap': 33, 'Encounters': ['hano-beach', 'malie-garden', 'malie-city', 'route-10', 'route-11', 'mount-hokulani']},
            {'Stage': 7, 'BattleName': 'Ghost Trial', 'LevelCap': 35, 'Encounters': ['route-12', 'blush-mountain', 'route-13', 'tapu-village', 'mount-lanakila', 'route-14', 'route-15']},
            {'Stage': 8, 'BattleName': 'Kahuna Nanu', 'LevelCap': 44, 'Encounters': ['thrifty-megamart', 'haina-desert', 'route-16', 'ula-ula-meadow', 'route-17']},
            {'Stage': 9, 'BattleName': 'Dragon Trial', 'LevelCap': 49, 'Encounters': ['seafolk-village', 'aerodactyl-gift', 'poni-wilds', 'ancient-poni-path', 'poni-breaker-coast', 'vast-poni-canyon', 'exeggutor-island']},
            {'Stage': 10, 'BattleName': 'Fairy Trial', 'LevelCap': 54, 'Encounters': ['poipole-gift']},
            {'Stage': 11, 'BattleName': 'Kahuna Hapu', 'LevelCap': 54, 'Encounters': []},
            {'Stage': 12, 'BattleName': 'Pokemon League', 'LevelCap': 57, 'Encounters': ['necrozma-static']},
            {'Stage': 13, 'BattleName': 'Rainbow Rocket', 'LevelCap': 68, 'Encounters': ['type-null-gift', 'poni-grove', 'poni-plains', 'poni-coast', 'poni-gauntlet', 'poni-meadow', 'resolution-cave', 'zygarde-static', 'nebby-static', 'tapu-koko-static', 'tapu-lele-static', 'tapu-bulu-static', 'tapu-fini-static', 'team-rocket-castle']}
        ]},
    {'Name': 'lets-go-pikachu-lets-go-eevee', 'Games': ['lets-go-pikachu', 'lets-go-eevee'], 'Colour': [16371533, 13342031], 'LinkEmoji': ['<:linkLGP:1193409693234761728>', '<:linkLGE:1193409732493447228>'], 'Mascot': [25, 133], 'Progression': [
            {'Stage': 0, 'BattleName': 'Brock', 'LevelCap': 14, 'Encounters': ['starter', 'pallet-town', 'route-1', 'viridian-city', 'route-22', 'route-2', 'viridian-forest']},
            {'Stage': 1, 'BattleName': 'Misty', 'LevelCap': 21, 'Encounters': ['route-3', 'route-4', 'mt-moon', 'cerulean-city']},
            {'Stage': 2, 'BattleName': 'Lt. Surge', 'LevelCap': 24, 'Encounters': ['route-24', 'route-25', 'route-5', 'route-6', 'vermillion-city']},
            {'Stage': 3, 'BattleName': 'Erika', 'LevelCap': 29, 'Encounters': ['route-11', 'digletts-cave', 'route-9', 'route-10', 'rock-tunnel', 'pokemon-tower', 'route-12', 'route-8', 'route-7', 'celadon-city']},
            {'Stage': 4, 'BattleName': 'Sabrina', 'LevelCap': 43, 'Encounters': ['saffron-city']},
            {'Stage': 5, 'BattleName': 'Koga', 'LevelCap': 43, 'Encounters': ['route-16', 'route-17', 'route-18', 'fuschia-city']},
            {'Stage': 6, 'BattleName': 'Blaine', 'LevelCap': 47, 'Encounters': ['safari-zone', 'route-15', 'route-14', 'route-13', 'power-plant', 'route-19', 'route-20', 'seafoam-islands', 'cinnabar-island', 'pokemon-mansion']},
            {'Stage': 7, 'BattleName': 'Giovanni', 'LevelCap': 50, 'Encounters': ['route-21']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 65, 'Encounters': ['route-23', 'victory-road']}
        ]},
    {'Name': 'sword-shield', 'Games': ['sword', 'shield'], 'Colour': [44783, 15536485], 'LinkEmoji': ['<:linkSw:1193411092509102130>', '<:LinkSh:1193411134577983498>'], 'Mascot': [888, 889], 'Progression': [
            {'Stage': 0, 'BattleName': 'Milo', 'LevelCap': 20, 'Encounters': ['starter', 'slumbering-weald', 'route-1', 'wedgehurst', 'route-2', 'rolling-fields', 'dappled-grove', 'west-lake-axewell', 'watchtower-ruins', 'east-lake-axewell', 'south-lake-miloch', 'giants-seat', 'north-lake-miloch', 'motostoke', 'route-3', 'galar-mine', 'route-4']},
            {'Stage': 1, 'BattleName': 'Nessa', 'LevelCap': 24, 'Encounters': ['route-5', 'hulbury']},
            {'Stage': 2, 'BattleName': 'Kabu', 'LevelCap': 27, 'Encounters': ['galar-mine-no-2', 'motostoke-outskirts', 'motostoke-stadium']},
            {'Stage': 3, 'BattleName': 'Bea', 'LevelCap': 36, 'Encounters': ['motostoke-riverbank', 'bridge-field', 'stony-wilderness', 'giants-mirror', 'dusty-bowl', 'giants-cap', 'hammerlocke-hills', 'lake-of-outrage', 'route-6']},
            {'Stage': 4, 'BattleName': 'Opal', 'LevelCap': 38, 'Encounters': ['glimwood-tangle']},
            {'Stage': 5, 'BattleName': 'Gordie', 'LevelCap': 42, 'Encounters': ['route-7', 'route-8']},
            {'Stage': 6, 'BattleName': 'Piers', 'LevelCap': 46, 'Encounters': ['route-9']},
            {'Stage': 7, 'BattleName': 'Raihan', 'LevelCap': 48, 'Encounters': []},
            {'Stage': 8, 'BattleName': 'Wyndon Semi Finals', 'LevelCap': 49, 'Encounters': ['route-10', 'axews-eye']},
            {'Stage': 9, 'BattleName': 'Wyndon Championship Match', 'LevelCap': 55, 'Encounters': []},
            {'Stage': 10, 'BattleName': 'Champion Leon', 'LevelCap': 65, 'Encounters': []},
            {'Stage': 11, 'BattleName': 'Master Mustard', 'LevelCap': 80, 'Encounters': ['fields-of-honor', 'soothing-wetlands', 'forest-of-focus', 'challenge-beach', 'brawlers-cave', 'challenge-road', 'courageous-cavern', 'loop-lagoon', 'training-lowlands', 'warm-up-tunnel', 'potbottom-desert', 'workout-sea', 'stepping-stone-sea', 'insular-sea', 'honeycalm-sea', 'honeycalm-island']},
            {'Stage': 12, 'BattleName': 'Peony', 'LevelCap': 74, 'Encounters': ['slippery-slope', 'freezington']}
        ]},
    {'Name': 'brilliant-diamond-shining-pearl', 'Games': ['brilliant-diamond', 'shining-pearl'], 'Colour': [3048389, 13989256], 'LinkEmoji': ['<:linkBD:1193409792459427962>', '<:linkSP:1193409837476880476>'], 'Mascot': [483, 484], 'Progression': [
            {'Stage': 0, 'BattleName': 'Roark', 'LevelCap': 14, 'Encounters': ['starter', 'twinleaf-town', 'route-201', 'lake-verity', 'route-202', 'route-203', 'oreburgh-gate', 'oreburgh-city']},
            {'Stage': 1, 'BattleName': 'Gardenia', 'LevelCap': 22, 'Encounters': ['oreburgh-mine', 'route-207', 'route-204', 'ravaged-path', 'floaroma-meadow', 'route-205', 'valley-windworks', 'eterna-forest', 'the-old-chateau', 'eterna-city']},
            {'Stage': 2, 'BattleName': 'Maylene', 'LevelCap': 30, 'Encounters': ['underground:-spacious-cave', 'underground:-grassland-cave', 'underground:-fountainspring-cave', 'underground:-rocky-cave', 'underground:-swampy-cave', 'underground:-dazzling-cave', 'underground:-whiteout-cave', 'underground:-icy-cave', 'underground:-riverbank-cave', 'underground:-sandsear-cave', 'underground:-still-water-cave', 'underground:-sunlit-cavern', 'underground:-big-bluff-cavern', 'underground:-stargleam-cavern', 'underground:-volcanic-cave', 'underground:-glacial-cavern', 'underground:-bogsunk-cavern', 'route-206', 'wayward-cave', 'mt-coronet', 'route-208', 'hearthome-city', 'route-209', 'the-lost-tower', 'solaceon-ruins', 'route-210', 'route-215']},
            {'Stage': 3, 'BattleName': 'Crasher Wake', 'LevelCap': 30, 'Encounters': ['trophy-garden', 'pastoria-city', 'great-marsh']},
            {'Stage': 4, 'BattleName': 'Fantina', 'LevelCap': 36, 'Encounters': ['route-212', 'route-213', 'valor-lakefront', 'lake-valor', 'route-214', 'ruin-maniacs-cave', 'celestic-town']},
            {'Stage': 5, 'BattleName': 'Byron', 'LevelCap': 39, 'Encounters': ['fuego-ironworks', 'routes-219', 'route-220', 'route-221', 'route-218', 'canalave-city', 'iron-island']},
            {'Stage': 6, 'BattleName': 'Candice', 'LevelCap': 42, 'Encounters': ['route-211', 'route-216', 'route-217', 'acuity-lakefront', 'lake-acuity', 'snowpoint-temple']},
            {'Stage': 7, 'BattleName': 'Volkner', 'LevelCap': 49, 'Encounters': ['route-222', 'sunyshore-city']},
            {'Stage': 8, 'BattleName': 'Elite Four', 'LevelCap': 66, 'Encounters': ['route-223', 'victory-road', 'pokã©mon-league']}
        ]},
    {'Name': 'legends-arceus', 'Games': ['legends-arceus'], 'Colour': [15132131], 'LinkEmoji': ['<:linkPLA:1193409887955337286>'], 'Mascot': [493], 'Progression': []},
    {'Name': 'scarlet-violet', 'Games': ['scarlet', 'violet'], 'Colour': [14419990, 8465547], 'LinkEmoji': ['<:linkS:1193409945010450442>', '<:linkV:1193409983946170479>'], 'Mascot': [1007, 1008], 'Progression': [
            {'Stage': 0, 'BattleName': 'Katy', 'LevelCap': 15, 'Encounters': ['starter', 'poco-path', 'south-area-1', 'inlet-grotto', 'south-area-4', 'south-area-2']},
            {'Stage': 1, 'BattleName': 'Titan Klawf', 'LevelCap': 16, 'Encounters': ['south-area-5', 'east-area-1', 'south-area-3']},
            {'Stage': 2, 'BattleName': 'Brassius', 'LevelCap': 17, 'Encounters': []},
            {'Stage': 3, 'BattleName': 'Titan Bombirdier', 'LevelCap': 20, 'Encounters': ['west-area-1']},
            {'Stage': 4, 'BattleName': 'Team Star Giacomo', 'LevelCap': 21, 'Encounters': []},
            {'Stage': 5, 'BattleName': 'Iono', 'LevelCap': 24, 'Encounters': ['east-area-2']},
            {'Stage': 6, 'BattleName': 'Team Star Mela', 'LevelCap': 27, 'Encounters': []},
            {'Stage': 7, 'BattleName': 'Titan Orthworm', 'LevelCap': 29, 'Encounters': ['east-area-3']},
            {'Stage': 8, 'BattleName': 'Kofu', 'LevelCap': 30, 'Encounters': ['west-area-2']},
            {'Stage': 9, 'BattleName': 'Team Star Atticus', 'LevelCap': 33, 'Encounters': ['west-area-3', 'glaseado-mountain-south', 'dalizapa-passagea', 'tagree-thicket']},
            {'Stage': 10, 'BattleName': 'Larry', 'LevelCap': 36, 'Encounters': []},
            {'Stage': 11, 'BattleName': 'Ryme', 'LevelCap': 42, 'Encounters': ['glaseado-mountain-north']},
            {'Stage': 12, 'BattleName': 'Titan Great Tusk', 'LevelCap': 45, 'Encounters': ['south-area-6', 'asado-desert']},
            {'Stage': 13, 'BattleName': 'Tulip', 'LevelCap': 45, 'Encounters': ['alfornada-cavern']},
            {'Stage': 14, 'BattleName': 'Grusha', 'LevelCap': 48, 'Encounters': []},
            {'Stage': 15, 'BattleName': 'Team Star Ortega', 'LevelCap': 51, 'Encounters': ['north-area-3']},
            {'Stage': 16, 'BattleName': 'Titan Tatsugiri', 'LevelCap': 57, 'Encounters': ['casseroya-lake']},
            {'Stage': 17, 'BattleName': 'Team Star Eri', 'LevelCap': 56, 'Encounters': ['north-area-1', 'north-area-2']},
            {'Stage': 18, 'BattleName': 'Arven', 'LevelCap': 63, 'Encounters': ['west-paldean-sea', 'south-paldean-sea', 'east-paldean-sea', 'north-paldean-sea', 'socarrat-trail', 'pokemon-league']},
            {'Stage': 19, 'BattleName': 'Director Clavell', 'LevelCap': 61, 'Encounters': []},
            {'Stage': 20, 'BattleName': 'Team Star Penny', 'LevelCap': 63, 'Encounters': []},
            {'Stage': 21, 'BattleName': 'Elite Four', 'LevelCap': 62, 'Encounters': []},
            {'Stage': 22, 'BattleName': 'Nemona', 'LevelCap': 66, 'Encounters': []},
            {'Stage': 23, 'BattleName': 'Professor Sada', 'LevelCap': 67, 'Encounters': ['area-zero']}
        ]},
    {'Name': 'legends-za', 'Games': ['legends-za'], 'Colour': [8702355], 'LinkEmoji': ['<:linkPLZA:1431931150863175801>'], 'Mascot': [10120], 'Progression': []}
]

#Amount of encounters checker, to see overall balance
'''
for game in games:
    encounter_count = 0
    if len(game['Progression']) > 0:
        for stage in game['Progression']:
            for encounter in stage['Encounters']:
                encounter_count += 1
    print(f'{game["Name"]} has {encounter_count} encounters')
'''