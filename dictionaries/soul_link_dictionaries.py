soulLinksFileLocations = {
    'Runs': 'text_files/soul_links/runs.txt'
}

defaultRun = {
    'VersionGroup': '',
    'RunName': '',
}

gens = [
    {'Name': 1, 'Serebii-Link': '', 'Roman-Numeral': 'I', 'Version-Groups': [{'Name': 'red-blue'}, {'Name': 'yellow'}]},
    {'Name': 2, 'Serebii-Link': '-gs', 'Roman-Numeral': 'II', 'Version-Groups': [{'Name': 'gold-silver'}, {'Name': 'crystal'}]},
    {'Name': 3, 'Serebii-Link': '-rs', 'Roman-Numeral': 'III', 'Version-Groups': [{'Name': 'ruby-sapphire'}, {'Name': 'emerald'}, {'Name': 'firered-leafgreen'}]},
    {'Name': 4, 'Serebii-Link': '-dp', 'Roman-Numeral': 'IV', 'Version-Groups': [{'Name': 'diamond-pearl'}, {'Name': 'platinum'}, {'Name': 'heartgold-soulsilver'}]},
    {'Name': 5, 'Serebii-Link': '-bw', 'Roman-Numeral': 'V', 'Version-Groups': [{'Name': 'black-white'}, {'Name': 'black-2-white-2'}]},
    {'Name': 6, 'Serebii-Link': '-xy', 'Roman-Numeral': 'VI', 'Version-Groups': [{'Name': 'x-y'}, {'Name': 'omega-ruby-alpha-sapphire'}]},
    {'Name': 7, 'Serebii-Link': '-sm', 'Roman-Numeral': 'VII', 'Version-Groups': [{'Name': 'sun-moon'}, {'Name': 'ultra-sun-ultra-moon'}, {'Name': 'lets-go-pikachu-lets-go-eevee'}]},
    {'Name': 8, 'Serebii-Link': '-swsh', 'Roman-Numeral': 'VIII', 'Version-Groups': [{'Name': 'sword-shield'}, {'Name': 'the-isle-of-armor'}, {'Name': 'the-crown-tundra'}, {'Name': 'brilliant-diamond-and-shining-pearl'}, {'Name': 'legends-arceus'}]},
    {'Name': 9, 'Serebii-Link': '-swsh', 'Roman-Numeral': 'IX', 'Version-Groups': [{'Name': 'scarlet-violet'}, {'Name': 'the-teal-mask'}, {'Name': 'the-indigo-disk'}]}
]

games = [
    {'Name': 'red-blue', 'Games': ['Red', 'Blue'], 'Colour': [8978434, 2314131], 'Link-Emoji': ['<:_:1193403535954550885>', '<:_:1193403571983634463>'], 'Mascot': [6, 9], 'Progression': [{'Stage': 0, 'Name': 'Pre-Gym', 'Battle-Name': 'Brock', 'Level-Cap': 14, 'Encounters': ['Route 1', 'Route 2']}]},
    {'Name': 'yellow', 'Games': ['Yellow'], 'Colour': [15913776], 'Link-Emoji': ['<:_:1193403603981959188>'], 'Mascot': [25], 'Progression': []},
    {'Name': 'gold-silver', 'Games': ['Gold', 'Silver'], 'Colour': [12629117, 13422806], 'Link-Emoji': ['<:_:1193408037092864071>', '<:_:1193408117204070542>'], 'Mascot': [250, 249], 'Progression': []},
    {'Name': 'crystal', 'Games': ['Crystal'], 'Colour': [7107505], 'Link-Emoji': ['<:_:1193408169666420778>'], 'Mascot': [245], 'Progression': []},
    {'Name': 'ruby-sapphire', 'Games': ['Ruby', 'Sapphire'], 'Colour': [14305066, 2058149], 'Link-Emoji': ['<:_:1193408227296170065>', '<:_:1193408299203301507>'], 'Mascot': [383, 382], 'Progression': []},
    {'Name': 'emerald', 'Games': ['Emerald'], 'Colour': [42574], 'Link-Emoji': ['<:_:1193408566854418484>'], 'Mascot': [384], 'Progression': []},
    {'Name': 'firered-leafgreen', 'Games': ['FireRed', 'LeafGreen'], 'Colour': [15100211, 9947731], 'Link-Emoji': ['<:_:1193408619128029304>', '<:_:1193408671347114014>'], 'Mascot': [6, 3], 'Progression': []},
    {'Name': 'diamond-pearl', 'Games': ['Diamond', 'Pearl'], 'Colour': [5349551, 15576266], 'Link-Emoji': ['<:_:1193408726498029680>', '<:_:1193408782076743760>'], 'Mascot': [483, 484], 'Progression': [
                                            {'Stage': 0, 'Name': 'Start', 'Battle-Name': 'Roark', 'Level-Cap': 14, 'Encounters': ['Starter', 'Route 201', 'Lake Verity', 'Route 202', 'Route 203', 'Route 204', 'Ravaged Path', 'Route 218', 'Route 219', 'Twinleaf Town', 'Oreburgh Gate', 'Oreburgh Mine', 'Route 207']}, 
                                            {'Stage': 1, 'Name': 'Roark', 'Battle-Name': 'Gardenia', 'Level-Cap': 22, 'Encounters': ['Floaroma Meadow', 'Route 205', 'Valley Windworks', 'Drifloon Static', 'Eterna Forest', 'Eterna City', 'Route 211', 'Mt. Coronet']}, 
                                            {'Stage': 2, 'Name': 'Gardenia', 'Battle-Name': 'Maylene', 'Level-Cap': 30, 'Encounters': ['Old Chateau', 'Route 206', 'Wayward Cave', 'Route 208', 'Happiny Egg', 'Route 209', 'Lost Tower', 'Solaceon Ruins', 'Route 210', 'Route 215', 'Route 212', 'Trophy Garden', 'Pastoria City', 'Great Marsh', 'Route 213', 'Valor Lakefront', 'Route 214', 'Maniac Tunnel']}, 
                                            {'Stage': 3, 'Name': 'Maylene', 'Battle-Name': 'Crasher Wake', 'Level-Cap': 30, 'Encounters': []}, 
                                            {'Stage': 4, 'Name': 'Crasher Wake', 'Battle-Name': 'Fantina', 'Level-Cap': 36, 'Encounters': ['Celestic Town']}, 
                                            {'Stage': 5, 'Name': 'Fantina', 'Battle-Name': 'Byron', 'Level-Cap': 39, 'Encounters': ['Fuego Ironworks', 'Route 220', 'Route 221', 'Canalave City', 'Iron Island', 'Riolu Egg']},
                                            {'Stage': 6, 'Name': 'Byron', 'Battle-Name': 'Candice', 'Level-Cap': 42, 'Encounters': ['Route 216', 'Route 217', 'Acuity Lakefront']},
                                            {'Stage': 7, 'Name': 'Candice', 'Battle-Name': 'Volkner', 'Level-Cap': 49, 'Encounters': ['Lake Acuity', 'Legendary Static', 'Roaming Mesprit', 'Lake Valor', 'Azelf Static', 'Uxie Static', 'Route 222', 'Sunnyshore City', 'Route 223', 'Pokemon League']},
                                            {'Stage': 8, 'Name': 'Volkner', 'Battle-Name': 'Pokemon League', 'Level-Cap': 66, 'Encounters': ['Victory Road']}
                                        ]},
    {'Name': 'platinum', 'Games': ['Platinum'], 'Colour': [1911153], 'Link-Emoji': ['<:_:1193408835759644762>'], 'Mascot': [10007], 'Progression': [
                                            {'Stage': 0, 'Name': 'Start', 'Battle-Name': 'Roark', 'Level-Cap': 14, 'Encounters': ['Starter', 'Route 201', 'Lake Verity', 'Route 202', 'Route 203', 'Route 204', 'Ravaged Path', 'Route 218', 'Route 219', 'Twinleaf Town', 'Oreburgh Gate', 'Oreburgh Mine', 'Route 207']},
                                            {'Stage': 1, 'Name': 'Roark', 'Battle-Name': 'Gardenia', 'Level-Cap': 22, 'Encounters': ['Floaroma Meadow', 'Route 205', 'Valley Windworks', 'Drifloon Static', 'Eterna Forest', 'Eterna City', 'Route 211', 'Mt. Coronet']},
                                            {'Stage': 2, 'Name': 'Gardenia', 'Battle-Name': 'Fantina', 'Level-Cap': 26, 'Encounters': ['Old Chateau', 'Rotom Static', 'Togepi Egg', 'Route 206', 'Wayward Cave', 'Route 208', 'Eevee Gift']},
                                            {'Stage': 3, 'Name': 'Fantina', 'Battle-Name': 'Maylene', 'Level-Cap': 32, 'Encounters': ['Route 209', 'Lost Tower', 'Solaceon Ruins', 'Route 210', 'Route 215', 'Porygon Gift', 'Route 214', 'Maniac Tunnel', 'Valor Lakefront', 'Route 213', 'Pastoria City', 'Great Marsh', 'Route 212', 'Trophy Garden']},
                                            {'Stage': 4, 'Name': 'Maylene', 'Battle-Name': 'Crasher Wake', 'Level-Cap': 37, 'Encounters': []},
                                            {'Stage': 5, 'Name': 'Crasher Wake', 'Battle-Name': 'Byron', 'Level-Cap': 41, 'Encounters': ['Celestic Town', 'Fuego Ironworks', 'Route 220', 'Route 221', 'Canalave City', 'Iron Island', 'Riolu Egg']},
                                            {'Stage': 6, 'Name': 'Byron', 'Battle-Name': 'Candice', 'Level-Cap': 44, 'Encounters': ['Route 216', 'Route 217', 'Acuity Lakefront']},
                                            {'Stage': 7, 'Name': 'Candice', 'Battle-Name': 'Volkner', 'Level-Cap': 50, 'Encounters': ['Lake Acuity', 'Sendoff Spring', 'Roaming Mesprit', 'Lake Valor', 'Azelf Static', 'Uxie Static', 'Route 222', 'Sunnyshore City', 'Route 223', 'Pokemon League']},
                                            {'Stage': 8, 'Name': 'Volkner', 'Battle-Name': 'Pokemon League', 'Level-Cap': 62, 'Encounters': ['Victory Road']}
                                        ]},
    {'Name': 'heartgold-soulsilver', 'Games': ['HeartGold', 'SoulSilver'], 'Colour': [14398266, 11778238], 'Link-Emoji': ['<:_:1193408899198500876>', '<:_:1193409003661828178>'], 'Mascot': [250, 249], 'Progression': [
                                            {'Stage': 0, 'Name': 'Start', 'Battle-Name': 'Falkner', 'Level-Cap': 13, 'Encounters': ['Starter', 'Route 29', 'Route 46', 'Route 30', 'Route 31', 'Dark Cave', 'Sprout Tower', 'Ruins of Alph', 'Route 32', 'Mareep Egg', 'Wooper Egg', 'Slugma Egg']},
                                            {'Stage': 1, 'Name': 'Falkner', 'Battle-Name': 'Bugsy', 'Level-Cap': 17, 'Encounters': ['Togepi Egg', 'New Bark Town', 'Cherrygrove City', 'Violet City', 'Union Cave', 'Route 33', 'Ilex Forest', 'Slowpoke Well']},
                                            {'Stage': 2, 'Name': 'Bugsy', 'Battle-Name': 'Whitney', 'Level-Cap': 19, 'Encounters': ['Azalea Town', 'Route 34', 'Spearow Gift', 'Route 35', 'National Park', 'Route 36']},
                                            {'Stage': 3, 'Name': 'Whitney', 'Battle-Name': 'Morty', 'Level-Cap': 25, 'Encounters': ['Sudowoodo Static', 'Route 37', 'Ecruteak City', 'Burned Tower', 'Roaming Raikou', 'Roaming Entei', 'Eevee Gift', 'Route 42', 'Mt. Mortar', 'Route 38', 'Route 39', 'Olivine City', 'Route 40']},
                                            {'Stage': 4, 'Name': 'Morty', 'Battle-Name': 'Chuck', 'Level-Cap': 31, 'Encounters': ['Lapras Static', 'Route 41', 'Cianwood City', 'Shuckle Gift', 'Route 43', 'Lake of Rage', 'Gyarados Static', 'Rocket HQ', 'Electrode Static', 'Route 27', 'Tohjo Falls']},
                                            {'Stage': 5, 'Name': 'Chuck', 'Battle-Name': 'Pryce', 'Level-Cap': 34, 'Encounters': ['Route 47', 'Cliff Cave', 'Route 48', 'Safari Zone Gate', 'Safari Zone']},
                                            {'Stage': 6, 'Name': 'Pryce', 'Battle-Name': 'Jasmine', 'Level-Cap': 35, 'Encounters': []},
                                            {'Stage': 7, 'Name': 'Jasmine', 'Battle-Name': 'Claire', 'Level-Cap': 41, 'Encounters': ['Whirl Islands', 'Route 44', 'Ice Path', 'Blackthorn City', 'Route 45']},
                                            {'Stage': 8, 'Name': 'Claire', 'Battle-Name': 'Pokemon League', 'Level-Cap': 50, 'Encounters': ['Dragon\'s Den', 'Dratini Gift', 'Tyrogue Gift', 'Bell Tower', 'Legendary Static', 'Route 26', 'Victory Road']},
                                            {'Stage': 9, 'Name': 'Pokemon League', 'Battle-Name': 'Blue', 'Level-Cap': 60, 'Encounters': ['Pallet Town', 'Route 1', 'Viridian City', 'Route 2', 'Route 22', 'Viridian Forest', 'Diglett\'s Cave', 'Pewter City', 'Other Legendary Static', 'Route 3', 'Mt. Moon', 'Route 4', 'Cerulean City', 'Route 24', 'Route 25', 'Suicune Static', 'Route 5', 'Route 6', 'Vermillion City', 'Route 7', 'Celadon City', 'Route 8', 'Pokemon Tower', 'Route 9', 'Route 10', 'Power Plant', 'Rock Tunnel', 'Route 11', 'Snorlax Static', 'Route 12', 'Route 13', 'Route 14', 'Route 15', 'Fuchsia City', 'Safari Zone', 'Route 16', 'Route 17', 'Route 18', 'Route 19', 'Route 20', 'Seafoam Islands', 'Cinnabar Island', 'Route 21', 'Roaming Lati']},
                                            {'Stage': 10, 'Name': 'Blue', 'Battle-Name': 'Red', 'Level-Cap': 88, 'Encounters': ['Cliff Edge Gate', 'Articuno Static', 'Moltres Static', 'Zapdos Static', 'Mewtwo Static', 'Route 28', 'Mt. Silver', 'Mt. Silver Cave']}
                                       ]},
    {'Name': 'black-white', 'Games': ['Black', 'White'], 'Colour': [0, 16777215], 'Link-Emoji': ['<:_:1193409050709340192>', '<:_:1193409098058834011>'], 'Mascot': [644, 643], 'Progression': [
                                            {'Stage': 0, 'Name': 'Start', 'Battle-Name': 'Chilli/Cilan/Cress', 'Level-Cap': 14, 'Encounters': ['Starter', 'Route 1', 'Route 2', 'Monkey Gift']},
                                            {'Stage': 1, 'Name': 'Chilli/Cilan/Cress', 'Battle-Name': 'Lenora', 'Level-Cap': 20, 'Encounters': ['Dreamyard', 'Route 3', 'Wellspring Cave', 'Pinwheel Forest']},
                                            {'Stage': 2, 'Name': 'Lenora', 'Battle-Name': 'Burgh', 'Level-Cap': 23, 'Encounters': ['Route 4']},
                                            {'Stage': 3, 'Name': 'Burgh', 'Battle-Name': 'Elesa', 'Level-Cap': 27, 'Encounters': ['Desert Resort', 'Darmanitan Static', 'Relic Castle', 'Route 5', 'Rouet 16', 'Lostlorn Forest']},
                                            {'Stage': 4, 'Name': 'Elesa', 'Battle-Name': 'Clay', 'Level-Cap': 31, 'Encounters': ['Driftveil Drawbridge', 'Cold Storage', 'Route 6']},
                                            {'Stage': 5, 'Name': 'Clay', 'Battle-Name': 'Skyla', 'Level-Cap': 35, 'Encounters': ['Chargestone Cave', 'Route 7', 'Celestial Tower']},
                                            {'Stage': 6, 'Name': 'Skyla', 'Battle-Name': 'Brycen', 'Level-Cap': 39, 'Encounters': ['Route 17', 'P2 Lab', 'Route 18', 'Larvesta Egg', 'Striton City', 'Driftveil City', 'Mistralton Cave', 'Cobalion Static', 'Virizion Static', 'Twist Mountain', 'Icirrus City', 'Route 8', 'Moor of Icirrus']},
                                            {'Stage': 7, 'Name': 'Brycen', 'Battle-Name': 'Drayden/Iris', 'Level-Cap': 43, 'Encounters': ['Dragonspiral Tower', 'Route 9', 'Route 10']},
                                            {'Stage': 8, 'Name': 'Drayden/Iris', 'Battle-Name': 'Pokemon League', 'Level-Cap': 50, 'Encounters': ['Roaming Genie', 'Victory Road', 'Terrakion Static']},
                                            {'Stage': 9, 'Name': 'Pokemon League', 'Battle-Name': 'N\'s Castle', 'Level-Cap': 54, 'Encounters': ['Legendary Static']}
                                        ]},
    {'Name': 'black-2-white-2', 'Games': ['Black 2', 'White 2'], 'Colour': [4421539, 15960922], 'Link-Emoji': ['<:_:1193409150726713434>', '<:_:1193409195626741832>'], 'Mascot': [10022, 10023], 'Progression': [
                                            {'Stage': 0, 'Name': 'Start', 'Battle-Name': 'Cheren', 'Level-Cap': 13, 'Encounters': ['Starter', 'Route 19', 'Route 20', 'Floccesy Ranch']},
                                            {'Stage': 1, 'Name': 'Cheren', 'Battle-Name': 'Roxie', 'Level-Cap': 18, 'Encounters': ['Virbank Complex']},
                                            {'Stage': 2, 'Name': 'Roxie', 'Battle-Name': 'Burgh', 'Level-Cap': 24, 'Encounters': ['Castelia Sewers', 'Castelia City', 'Relic Passage', 'Route 4']},
                                            {'Stage': 3, 'Name': 'Burgh', 'Battle-Name': 'Elesa', 'Level-Cap': 30, 'Encounters': ['Bird Static', 'Desert Resort', 'Relic Castle', 'Route 16', 'Lostlorn Forest', 'Route 5']},
                                            {'Stage': 4, 'Name': 'Elesa', 'Battle-Name': 'Clay', 'Level-Cap': 33, 'Encounters': ['Driftveil Drawbridge', 'Route 6', 'Deerling Gift', 'Chargestone Cave']},
                                            {'Stage': 5, 'Name': 'Clay', 'Battle-Name': 'Skyla', 'Level-Cap': 39, 'Encounters': ['Aspertia City', 'Virbank City', 'Volcarona Static', 'Mistralton Cave', 'Route 7', 'Celestial Tower']},
                                            {'Stage': 6, 'Name': 'Skyla', 'Battle-Name': 'Drayden', 'Level-Cap': 48, 'Encounters': ['Reversal Mountain', 'Strange House', 'Undella Town', 'Undella Bay', 'Jellicent Static', 'Seaside Cave', 'Route 14', 'Route 13', 'Cobalion Static', 'Route 12', 'Village Bridge', 'Route 11', 'Virizion Static', 'Route 9']},
                                            {'Stage': 7, 'Name': 'Drayden', 'Battle-Name': 'Marlon', 'Level-Cap': 51, 'Encounters': ['Route 21', 'Humilau City', 'Route 22', 'Giant Chasm']},
                                            {'Stage': 8, 'Name': 'Marlon', 'Battle-Name': 'Pokemon League', 'Level-Cap': 59, 'Encounters': ['Terrakion Static', 'Crustle Static', 'Route 23', 'Victory Road', 'Abundant Shrine']}
                                        ]},
    {'Name': 'x-y', 'Games': ['X', 'Y'], 'Colour': [90013, 13839173], 'Link-Emoji': ['<:_:1193409239406870698>', '<:_:1193409280896933988>'], 'Mascot': [716, 717], 'Progression': []},
    {'Name': 'omega-ruby-alpha-sapphire', 'Games': ['Omega Ruby', 'Alpha Sapphire'], 'Colour': [12452683, 2568359], 'Link-Emoji': ['<:_:1193409326400929832>', '<:_:1193409376891969646>'], 'Mascot': [10078, 10077], 'Progression': []},
    {'Name': 'sun-moon', 'Games': ['Sun', 'Moon'], 'Colour': [16094243, 2205919], 'Link-Emoji': ['<:_:1193409452691423242>', '<:_:1193409503790633023>'], 'Mascot': [791, 792], 'Progression': []},
    {'Name': 'ultra-sun-ultra-moon', 'Games': ['Ultra Sun', 'Ultra Moon'], 'Colour': [11492140, 5188451], 'Link-Emoji': ['<:_:1193409578281488405>', '<:_:1193409621843529860>'], 'Mascot': [10155, 10156], 'Progression': [
                                            {'Stage': 0, 'Name': 'Start', 'Battle-Name': 'Normal Trial', 'Level-Cap': 12, 'Encounters': ['Starter', 'Route 1', 'Trainer\'s School', 'Hau\'oli City', 'Route 2', 'Hau\'oli Cemetery', 'Sandy Cave']},
                                            {'Stage': 1, 'Name': 'Normal Trial', 'Battle-Name': 'Kahuna Hala', 'Level-Cap': 16, 'Encounters': ['Verdant Cavern', 'Route 3', 'Melemele Meadow', 'Seaward Cave']},
                                            {'Stage': 2, 'Name': 'Kahuna Hala', 'Battle-Name': 'Water Trial', 'Level-Cap': 20, 'Encounters': ['Ten Carat Hill', 'Route 4', 'Paniola Ranch', 'Route 5', 'Brooklet Hill', 'Hau\'oli Beachfront', 'Melemele Sea', 'Kala\'e Bay']},
                                            {'Stage': 3, 'Name': 'Water Trial', 'Battle-Name': 'Fire Trial', 'Level-Cap': 22, 'Encounters': ['Paniola Town', 'Route 6', 'Route 7', 'Wela Volcano Park', 'Diglett\'s Tunnel']},
                                            {'Stage': 4, 'Name': 'Fire Trial', 'Battle-Name': 'Grass Trial', 'Level-Cap': 24, 'Encounters': ['Dividing Peak Tunnel', 'Route 8', 'Fossil Static']},
                                            {'Stage': 5, 'Name': 'Grass Trial', 'Battle-Name': 'Kahuna Olivia', 'Level-Cap': 28, 'Encounters': ['Lush Jungle', 'Route 9', 'Memorial Hill', 'Akala Outskirts']},
                                            {'Stage': 6, 'Name': 'Kahuna Olivia', 'Battle-Name': 'Electric Trial', 'Level-Cap': 33, 'Encounters': ['Hano Beach', 'Malie Garden', 'Malie City', 'Route 10', 'Route 11', 'Mount Hokulani']},
                                            {'Stage': 7, 'Name': 'Electric Trial', 'Battle-Name': 'Ghost Trial', 'Level-Cap': 35, 'Encounters': ['Route 12', 'Blush Mountain', 'Route 13', 'Tapu Village', 'Mount Lanakila', 'Route 14', 'Route 15']},
                                            {'Stage': 8, 'Name': 'Ghost Trial', 'Battle-Name': 'Kahuna Nanu', 'Level-Cap': 44, 'Encounters': ['Thrifty Megamart', 'Haina Desert', 'Route 16', 'Ula\'Ula Meadow', 'Route 17']},
                                            {'Stage': 9, 'Name': 'Kahuna Nanu', 'Battle-Name': 'Dragon Trial', 'Level-Cap': 49, 'Encounters': ['Seafolk Village', 'Aerodactyl Gift', 'Poni Wilds', 'Ancient Poni Path', 'Poni Breaker Coast', 'Vast Poni Canyon', 'Exeggutor Island']},
                                            {'Stage': 10, 'Name': 'Dragon Trial', 'Battle-Name': 'Fairy Trial', 'Level-Cap': 54, 'Encounters': ['Poipole Gift']},
                                            {'Stage': 11, 'Name': 'Fairy Trial', 'Battle-Name': 'Kahuna Hapu', 'Level-Cap': 54, 'Encounters': []},
                                            {'Stage': 12, 'Name': 'Kahuna Hapu', 'Battle-Name': 'Pokemon League', 'Level-Cap': 57, 'Encounters': ['Necrozma Static']},
                                            {'Stage': 13, 'Name': 'Pokemon League', 'Battle-Name': 'Rainbow Rocket', 'Level-Cap': 68, 'Encounters': ['Type:Null Gift', 'Poni Grove', 'Poni Plains', 'Poni Coast', 'Poni Gauntlet', 'Poni Meadow', 'Resolution Cave', 'Zygarde Static', 'Legendary Static', 'Tapu Koko Static', 'Tapu Lele Static', 'Tapu Bulu Static', 'Tapu Fini Static', 'Team Rocket Castle']}
    ]},
    {'Name': 'lets-go-pikachu-lets-go-eevee', 'Games': ['Lets Go Pikachu', 'Lets Go Eevee'], 'Colour': [16371533, 13342031], 'Link-Emoji': ['<:_:1193409693234761728>', '<:_:1193409732493447228>'], 'Mascot': [25, 133], 'Progression': []},
    {'Name': 'sword-shield', 'Games': ['Sword', 'Shield'], 'Colour': [44783, 15536485], 'Link-Emoji': ['<:_:1193411092509102130>', '<:_:1193411134577983498>'], 'Mascot': [888, 889], 'Progression': []},
    {'Name': 'brilliant-diamond-and-shining-pearl', 'Games': ['Brilliant Diamond', 'Shining Pearl'], 'Colour': [3048389, 13989256], 'Link-Emoji': ['<:_:1193409792459427962>', '<:_:1193409837476880476>'], 'Mascot': [483, 484], 'Progression': []},
    {'Name': 'legends-arceus', 'Games': ['Legends Arceus'], 'Colour': [15132131], 'Link-Emoji': ['<:_:1193409887955337286>'], 'Mascot': [493], 'Progression': []},
    {'Name': 'scarlet-violet', 'Games': ['Scarlet', 'Violet'], 'Colour': [14419990, 8465547], 'Link-Emoji': ['<:_:1193409945010450442>', '<:_:1193409983946170479>'], 'Mascot': [1007, 1008], 'Progression': []}
]

#Structure for Pokemon, generated from generate_pokemon_file.py
'''
pokemon = [
    {Name: 'Bulbasaur', DexNum: 1, Evolves-From: null, Evolves-Into: [{'DexNum': 2, 'Method': 'level-up', 'Value': 16}], Nickname: False},
    {Name: 'Venusaur', DexNum: 1, Evolves-From: 2, Evolves-Into: [], Nickname: False},
]

'''

#Structure for runs
'''
Players are an array of whatever discord comes back with with the @messages, something like <@341722760852013066>
Pokemon is an array of dex numbers, set up as -1 until each player specifies their encounter
Encounter is an array of encounters that have been encountered or still need to be encountered
runs = [
    {Name: 'HeartGold 3 Player Run', Game: 'HeartGold', Version-Group: 'heartgold-soulsilver', Current-Progress: 0, Players:[], Encounters: [{Name: 'Rt 1', Pokemon: []}], Teams: [{Name: 'Falkner', Links: ['Rt 1', 'Rt 2']}]}
]
'''

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