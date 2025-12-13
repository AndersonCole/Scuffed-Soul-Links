import requests
import json
import aiohttp
import asyncio

def sortFunction(e):
    return e['DexNum']

def generatePokemonGen(gen):
    pokemon = []

    multiple_method_mons = []

    response = requests.get(f'https://pokeapi.co/api/v2/generation/{gen}')
    response = response.json()
    response = response['pokemon_species']

    for species in response:
        species = requests.get(species['url'])
        species = species.json()
        evo_chain = requests.get(species['evolution_chain']['url'])
        evo_chain = evo_chain.json()
        
        if species['evolves_from_species'] is None:
            evolves_from = None
        else:
            evolves_from = int(species['evolves_from_species']['url'][42:].strip('/'))

        if len(evo_chain['chain']['evolves_to']) == 0:
            evolves_into = None
        elif species['name'] == 'phione':
            evolves_into = None
        else:
            evolves_into = []
            found = False
            if evo_chain['chain']['species']['name'] == species['name']:
                for evo in evo_chain['chain']['evolves_to']:
                    if len(evo['evolution_details']) > 1:
                        multiple_method_mons.append(f'{species["name"]} -> {evo["species"]["name"]}')
                    
                    if evo['species']['name'] == 'dipplin':
                        method = 'use-item'
                        value = 'syrupy-apple'
                    elif evo['species']['name'] == 'archaludon':
                        method = 'use-item'
                        value = 'metal-alloy'
                    elif evo['species']['name'] == 'sinistcha':
                        method = 'use-item'
                        value = 'unremarkable-teacup'
                    else:

                        method = evo['evolution_details'][0]['trigger']['name']

                        if method == 'level-up':
                            if evo['evolution_details'][0]['min_happiness'] is not None or evo['evolution_details'][0]['min_affection'] is not None:
                                method = 'happiness'
                                value = 'heart'
                            elif evo['evolution_details'][0]['known_move'] is not None or evo['evolution_details'][0]['party_species'] is not None:
                                method = 'default'
                                value = None
                            elif evo['evolution_details'][0]['location'] is not None:
                                method = 'use-item'
                                if species['name'] == 'nosepass':
                                    value = 'thunder-stone'
                                elif species['name'] == 'crabrawler':
                                    value = 'ice-stone'
                                else:
                                    value = evo['evolution_details'][-1]['item']['name']
                            elif evo['evolution_details'][0]['held_item'] is not None:
                                method = 'use-item'
                                value= evo['evolution_details'][0]['held_item']['name']
                            else:
                                if evo_chain['chain']['species']['name'] == 'feebas':
                                    method = 'happiness'
                                    value = 'heart'
                                else:
                                    value = int(evo['evolution_details'][0]['min_level'])
                        elif method == 'trade':
                            value = 'linking-cord'
                        elif method == 'use-item':
                            value = evo['evolution_details'][0]['item']['name']
                        elif method == 'agile-style-move' or method == 'strong-style-move':
                            method = 'use-item'
                            value = 'tm-normal'
                        else:
                            method = 'default'
                            value = None
                    
                    evolves_into.append({
                        'DexNum': int(evo['species']['url'][42:].strip('/')),
                        'Method': method,
                        'Value': value
                    })
            else:
                for evolution in evo_chain['chain']['evolves_to']:
                    if evolution['species']['name'] == species['name']:
                        found = True
                        for evo in evolution['evolves_to']:
                            if len(evo['evolution_details']) > 1:
                                multiple_method_mons.append(f'{evolution["species"]["name"]} -> {evo["species"]["name"]}')
                            
                            if evo['species']['name'] == 'hydrapple':
                                method = 'default'
                                value = None
                            else:
                                method = evo['evolution_details'][0]['trigger']['name']

                                if method == 'level-up':
                                    if evo['evolution_details'][0]['min_happiness'] is not None or evo['evolution_details'][0]['min_affection'] is not None:
                                        method = 'happiness'
                                        value = 'heart'
                                    if evo['evolution_details'][0]['min_happiness'] is not None or evo['evolution_details'][0]['min_affection'] is not None:
                                        method = 'happiness'
                                        value = 'heart'
                                    elif evo['evolution_details'][0]['known_move'] is not None:
                                        method = 'default'
                                        value = None
                                    elif evo['evolution_details'][0]['location'] is not None:
                                        method = 'use-item'
                                        value = evo['evolution_details'][-1]['item']['name']
                                    elif evo['evolution_details'][0]['held_item'] is not None:
                                        method = 'use-item'
                                        value= evo['evolution_details'][0]['held_item']['name']
                                    else:
                                        if evolution['species']['name'] == 'charjabug':
                                            method = 'use-item'
                                            value = 'thunder-stone'
                                        else:
                                            value = int(evo['evolution_details'][0]['min_level'])
                                elif method == 'trade':
                                    value = 'linking-cord'
                                elif method == 'use-item':
                                    value = evo['evolution_details'][0]['item']['name']
                                elif method == 'agile-style-move' or method == 'strong-style-move':
                                    method = 'use-item'
                                    value = 'tm-normal'
                                else:
                                    method = 'default'
                                    value = None

                                if evo_chain['chain']['species']['name'] == 'feebas':
                                    method = 'happiness'
                                    value = 'heart'
                            
                            evolves_into.append({
                                'DexNum': int(evo['species']['url'][42:].strip('/')),
                                'Method': method,
                                'Value': value
                            })
                if not found:
                    evolves_into = None
                    
        
        if species['varieties']:
            for varieties in species['varieties']:
                pokemon.append({
                    'Name': varieties['pokemon']['name'],
                    'DexNum': int(varieties['pokemon']['url'][34:].strip("/")),
                    'Nicknames': [],
                    'Evolves-Into': evolves_into,
                    'Evolves-From': evolves_from
                })
        else:
            pokemon.append({
                'Name': species['name'],
                'DexNum': int(species['id']),
                'Nicknames': [],
                'Evolves-Into': evolves_into,
                'Evolves-From': evolves_from
            })

    print(f'Gen {gen} done!')
  
    pokemon.sort(reverse=False, key=sortFunction)

    pokemon = fixNames(pokemon)

    for poke in pokemon:
        if poke['Evolves-Into'] == []:
            poke['Evolves-Into'] = None

    with open('new_pokemon.txt', 'w') as file:
        file.write(json.dumps(pokemon))

    with open('multiple_evo_mons.txt', 'w') as file:
        file.write(json.dumps(multiple_method_mons))

def fixNames(pokemon):
    for poke in pokemon:
        match poke['Name']:
            case 'deoxys-normal':
                poke['Name'] = 'deoxys'
            case 'wormadam-plant':
                poke['Name'] = 'wormadam'
            case 'shaymin-land':
                poke['Name'] = 'shaymin'
            case 'giratina-altered':
                poke['Name'] = 'giratina'
            case 'basculin-red-striped':
                poke['Name'] = 'basculin'
            case 'darmanitan-standard':
                poke['Name'] = 'darmanitan'
            case 'tornadus-incarnate':
                poke['Name'] = 'tornadus'
            case 'thundurus-incarnate':
                poke['Name'] = 'thundurus'
            case 'landorus-incarante':
                poke['Name'] = 'landorus'
            case 'enamorus-incarnate':
                poke['Name'] = 'enamorus'
            case 'meloetta-aria':
                poke['Name'] = 'meloetta'
            case 'keldeo-ordinary':
                poke['Name'] = 'keldeo'
            case 'meowstic-male':
                poke['Name'] = 'meowstic'
            case 'aegislash-shield':
                poke['Name'] = 'aegislash'
            case 'pumpkaboo-average':
                poke['Name'] = 'pumpkaboo'
            case 'gourgeist-average':
                poke['Name'] = 'gourgeist'
            case 'zygarde-50':
                poke['Name'] = 'zygarde'
            case 'oricorio-baile':
                poke['Name'] = 'oricorio'
            case 'lycanroc-midday':
                poke['Name'] = 'lycanroc'
            case 'wishiwashi-school':
                poke['Name'] = 'wishiwashi'
            case 'minior-red-meteor':
                poke['Name'] = 'minior'
            case 'mimikyu-disguised':
                poke['Name'] = 'mimikyu'
            case 'toxtricity-amped':
                poke['Name'] = 'toxtricity'
            case 'eiscue-ice':
                poke['Name'] = 'eiscue'
            case 'indeedee-male':
                poke['Name'] = 'indeedee'
            case 'morpeko-full-belly':
                poke['Name'] = 'morpeko'
            case 'urshifu-single-strike':
                poke['Name'] = 'urshifu'
            case 'basculegion-male':
                poke['Name'] = 'basculegion'
            case 'darmanitan-galar-standard':
                poke['Name'] = 'darmanitan-galar'
            case 'tauros-paldea-combat-breed':
                poke['Name'] = 'tauros-paldea'

    return pokemon

async def generateNewMegaPokemon(offset, limit):
    pokemon = []

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(f'https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}') as response:
            response.raise_for_status()

            data = await response.json()

            for mon in data['results']:
                pokemon.append({
                    'Name': mon['name'],
                    'DexNum': int(mon['url'][34:].strip('/')),
                    'Nicknames': [],
                    'Evolves-Into': [],
                    'Evolves-From': None
                })

    with open('new_pokemon.txt', 'w') as file:
        file.write(json.dumps(pokemon))

def fixEvolvesInto():
    with open('pokemon.txt', 'r') as file:
        pokemon = json.loads(file.read())
    
    '''
    output = ''
    for i in range(25):
        i += 145530
        output += pokemon[i]

    print(output)
    '''
    for poke in pokemon:
        if poke['Evolves-Into'] == None:
            poke['Evolves-Into'] = []

    with open('pokemon.txt', 'w') as file:
        file.write(json.dumps(pokemon))
    
def showPokemonWithMultipleEvos():
    with open('pokemon.txt', 'r') as file:
        pokemon = json.loads(file.read())

    multipleEvos = [obj for obj in pokemon if obj['Evolves-Into'] is not None and len(obj['Evolves-Into']) > 1]

    for evo in multipleEvos:
        evolutionsString = '['
        for evoInto in evo['Evolves-Into']:
            evolutionsString += [obj for obj in pokemon if obj['DexNum'] == int(evoInto)][0]['Name'] + ', '
        evolutionsString += ']'
        print(f'{evo["Name"]} evolves into {evolutionsString}')
        x = input('Delete any? y/n\n')
        while x == 'y':
            remove = input('Type a name to remove it\n')
            toRemove = [obj for obj in pokemon if obj['Name'] == remove][0]['DexNum']

            temp = [evoInto for evoInto in evo['Evolves-Into'] if int(toRemove) != int(evoInto)]

            evo['Evolves-Into'] = temp

            print(f'Removed {remove}')
            
            for idx, pkmn in enumerate(pokemon):
                if pkmn['DexNum'] == evo['DexNum']:
                    pokemon[idx]['Evolves-Into'] = temp
                    break

            x = input('Continue Removing? y/n\n')

    with open('pokemon.txt', 'w') as file:
        file.write(json.dumps(pokemon))


def fixRunTeams():
    with open('text_files/soul_links/runs.txt', 'r') as file:
        runs = json.loads(file.read())  

    for run in runs:
        for team in run['Teams']:
            try:
                for i, member in enumerate(team):
                    team[i] = member['Pokemon']
            except Exception as ex:
                continue

    with open('text_files/soul_links/runs.txt', 'w') as file:
        file.write(json.dumps(runs))


#generatePokemonGen()
asyncio.run(generateNewMegaPokemon(1328, 50))

#fixRunTeams()
#fixEvolvesInto()
#showPokemonWithMultipleEvos()

#with open('pokemon.txt', 'w') as file:
    #file.write(json.dumps(types))

#with open('pokemon.txt', 'r') as file:
    #pokemon = json.loads(file.read())

#Structure for Pokemon, generated from generate_pokemon_file.py
'''
pokemon = [
    {'Name': 'Bulbasaur', DexNum: 1, Nicknames: [], Evolves-Into: [{DexNum: 2, Method: 'level-up', Value: '16'}], Evolves-From: None},
    Evolves-Into: [{DexNum: 2, Method: 'use-item', Value: 'water-stone'}]
]

I changed the way pretty much every single regional variant's dex is pointing manually
'''

'''
Evo methods

actual methods
    level-up
    trade
    use-item

    happiness

default
    shed
    spin
    tower-of-darkness
    tower-of-waters
    three-critical-hits
    take-damage
    other
    agile-style-move
    strong-style-move
    recoil-damage
'''