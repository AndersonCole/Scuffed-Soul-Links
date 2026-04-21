import asyncio
import json
import copy

from functions.pvp_functions import *
from functions.shared_functions import pokemon

defaultModifiers = {
    'Floor': 0,
    'MinLevel': 1.0,
    'MaxLevel': 50.0,

    'BaseStats': {
        'Attack': 0,
        'Defence': 0,
        'Stamina': 0
    },
    'StatText': '',
}

async def getFakeR1(leagueLimit):
    fakers = []

    modifiers = copy.deepcopy(defaultModifiers)

    for mon in pokemon:
        pogoMon = next((dpsMon for dpsMon in pogoPokemon if dpsMon['ImageDexNum'] == mon['DexNum']), None)

        if pogoMon is not None:
            modifiers['BaseStats']['Attack'] = pogoMon['Attack']
            modifiers['BaseStats']['Defence'] = pogoMon['Defence']
            modifiers['BaseStats']['Stamina'] = pogoMon['Stamina']
        else:
            monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{mon["DexNum"]}')

            if monData is None:
                return f'An error occured while checking the api!'

            stats = []

            for i in range(6):
                stats.append(int(monData['stats'][i]['base_stat']))

            modifiers['BaseStats']['Attack'], modifiers['BaseStats']['Defence'], modifiers['BaseStats']['Stamina'], nerfAmount = calcPoGoStatsFromBaseStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5])
        
        rankList = await calcPvpRanks(modifiers['BaseStats']['Attack'], modifiers['BaseStats']['Defence'], modifiers['BaseStats']['Stamina'],
                                      leagueLimit, modifiers['Floor'], modifiers['MinLevel'], modifiers['MaxLevel'])

        rankList.sort(key=lambda x:(
            x['StatProduct'],
            x['Stats']['Attack'],
            x['Stats']['Stamina'],
            x['CP'],
            x['Ivs']['Stamina']
        ), reverse=True)

        if rankList[0]['StatProduct'] == rankList[1]['StatProduct'] and not (rankList[0]['Ivs']['Attack'] == 15 and rankList[0]['Ivs']['Defence'] == 15 and rankList[0]['Ivs']['Stamina'] == 15):
            fakers.append(mon['Name'])
            print(mon['Name'])
        
    with open('fake_rank_ones.txt', 'w') as file:
        file.write(json.dumps(fakers))

#asyncio.run(getFakeR1(1500))