""" 
Contains the functions relating to pogo pvp

Cole Anderson, Sep 2025
"""

import discord
import copy
import regex as re
import math
from diskcache import Cache
from dictionaries.pvp_dictionaries import pvpFileLocations, defaultPvpModifiers
from dictionaries.shared_dictionaries import sharedImagePaths, sharedEmbedColours, pogoCPMultipliers
from functions.shared_functions import (
    rollForShiny, getPoGoCPMultiplier, calcPoGoCP, calcPoGoStat, pogoRound, getDexNum, getPokeApiJsonData, calcPoGoStatsFromBaseStats, 
    getTypesFromPokeAPI, getTypeColour, getMonName, getPokeAPISpriteUrl, loadDataVariableFromFile, addPaginatedEmbedFields, formatTextForDisplay, pogoPokemon
)

pvpRanksCache = Cache('./cache/pvp_ranks')

fakeRankOnes = loadDataVariableFromFile(pvpFileLocations.get('FakeR1'))

async def pvpHelp():
    embed = discord.Embed(title=f'Shuckle\'s PvP Commands',
                                description='```$pvp check Medicham``` Shows the top ranks of a pokemon\n' +
                                            '```$pvp modifiers``` Lists out the available PvP modifiers\n\n' +
                                            '```$pvp add-mon Kartana, 323, 182, 139``` Registers a mons base stats in Atk/Def/HP order\n' +
                                            '```$pvp delete-mon Kartana``` Deletes a mon from the registered list\n' +
                                            '```$pvp list-mons``` Lists all the registered mons\n\n' +
                                            '```$pvp list-fakes GL``` Lists all the fake rank ones\nOptions are LL, Little, GL, Great, UL, Ultra\n' +
                                            '```$pvp img``` Gets the pvp rank reqs image',
                                color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))
    
    return embed

def pvpModifiers():
    embed = discord.Embed(title='Shuckles PvP Modifiers',
                            description='```$pvp check Medicham, 5/15/15``` IVs: Compares the entered IV combo against the top ranks\n' +
                                        '```$pvp check Medicham, Rank1``` Rank: Compares the entered rank number against the top ranks\n' +
                                        '```$pvp check Medicham, Great``` League: Sets the max CP based on the league.\nOptions are LL, Little, GL, Great, UL, Ultra, ML, Master\n' +
                                        '```$pvp check Medicham, Min20``` MinLevel: Sets the min level for rank calculations\n' +
                                        '```$pvp check Medicham, Max51``` MaxLevel: Sets the max level for rank calculations\n' +
                                        '```$pvp check Medicham, Floor10``` Floor: Sets the iv floor\n' +
                                        '```$pvp check Medicham, SortAttack``` SortAttack: Sorts results by highest attack\n' +
                                        '```$pvp check Medicham, SortDefence``` SortDefence: Sorts results by highest defence\n\n' +
                                        'Everything should be case insensitive.\n',
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    return embed

async def getPvpRanksImg():
    return discord.File('images/pvp.png', filename='pvp.png')

#region pvpRanks
def getNerfText(nerfAmount):
    if nerfAmount == 0.91:
        return ', with a 9% nerf'
    return ''

def getRankSortOrderText(order):
    if order == 'ByStatProduct':
        return 'Overall Stat Product'
    elif order == 'ByAttack':
        return 'Attack and Stat Product'
    elif order == 'ByDefence':
        return 'Defence and Stat Product'
    return ''

async def listFakeRankOnes(extraInput=None):
    embeds = []

    leagueLimit, league = determineLeague(extraInput)

    if leagueLimit is None:
        return f'\'{extraInput}\'wasn\'t understood as a valid league!'
    
    embed = discord.Embed(title=f'Mons with tied R1&2 Stat Product under {leagueLimit}',
                            description='Excluding R1 hundos',
                            color=sharedEmbedColours.get('Default'))
    
    fieldTitles = ['']
    fieldContent = ['']
    pageCount = 15

    filteredFakeRankOnes = [obj for obj in fakeRankOnes if league in obj['Leagues']]

    for i, mon in enumerate(filteredFakeRankOnes, start=1):
        fieldContent[0] += f'{formatTextForDisplay(mon["Name"])}\n'
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['']
    
    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds

def determineLeague(extraInput):
    leagueLimit = 1500
    league = 'gl'

    try:
        if extraInput is None:
            raise Exception

        elif extraInput == 'll':
            leagueLimit = 500
            league = 'll'
        elif extraInput == 'little':
            leagueLimit = 500
            league = 'll'
        elif extraInput == 'gl':
            leagueLimit = 1500
            league = 'gl'
        elif extraInput == 'great':
            leagueLimit = 1500
            league = 'gl'
        elif extraInput == 'ul':
            leagueLimit = 2500
            league = 'ul'
        elif extraInput == 'ultra':
            leagueLimit = 2500
            league = 'ul'

        else:
            leagueLimit = None
            league = None
    finally:
        return leagueLimit, league
    
async def pvpRankCheck(monName, extraInputs=None):
    modifiers = copy.deepcopy(defaultPvpModifiers)

    if extraInputs != None:
        modifiers, errorText = determineModifierValues([str(i).strip().lower() for i in extraInputs], modifiers)
        if errorText != '':
            return errorText
        
    dexNum = getDexNum(monName)

    if dexNum == -1:
        return f'The pokemon \'{monName}\' was not recognized!'
    
    pogoMon = next((dpsMon for dpsMon in pogoPokemon if dpsMon['ImageDexNum'] == dexNum), None)

    if pogoMon is not None:
        modifiers['BaseStats']['Attack'] = pogoMon['Attack']
        modifiers['BaseStats']['Defence'] = pogoMon['Defence']
        modifiers['BaseStats']['Stamina'] = pogoMon['Stamina']
        modifiers['StatText'] = 'Using the stats we\'ve entered'
    else:
        monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{dexNum}')

        if monData is None:
            return f'An error occured while checking the api!'

        stats = []

        for i in range(6):
            stats.append(int(monData['stats'][i]['base_stat']))

        modifiers['BaseStats']['Attack'], modifiers['BaseStats']['Defence'], modifiers['BaseStats']['Stamina'], nerfAmount = calcPoGoStatsFromBaseStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5])
        modifiers['StatText'] = f'Using the most recent main series stats{getNerfText(nerfAmount)}'

    cacheKey = (f'{dexNum}:{modifiers["LeagueLimit"]}:Floor{modifiers["Floor"]}:{modifiers["MinLevel"]}-{modifiers["MaxLevel"]}:' +
               f'{modifiers["BaseStats"]["Attack"]}/{modifiers["BaseStats"]["Defence"]}/{modifiers["BaseStats"]["Stamina"]}')

    if cacheKey in pvpRanksCache:
        rankList = pvpRanksCache[cacheKey]
    
    else:
        rankList = await calcPvpRanks(modifiers['BaseStats']['Attack'], modifiers['BaseStats']['Defence'], modifiers['BaseStats']['Stamina'],
                                      modifiers['LeagueLimit'], modifiers['Floor'], modifiers['MinLevel'], modifiers['MaxLevel'])

        pvpRanksCache.set(cacheKey, rankList)
    
    rankList.sort(key=lambda x:(
        x['StatProduct'],
        x['Stats']['Attack'],
        x['Stats']['Stamina'],
        x['CP'],
        x['Ivs']['Stamina']
    ), reverse=True)

    for i, rank in enumerate(rankList, start=1):
        rank['Rank'] = i

    if modifiers['ResultSortOrder'] == 'ByAttack':
        rankList.sort(key=lambda x:(
            x['StatProduct'] * x['Stats']['Attack'] * x['Ivs']['Attack'],
            x['Stats']['Attack'],
            x['Stats']['Stamina'],
            x['CP'],
            x['Ivs']['Stamina']
        ), reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByDefence':
        rankList.sort(key=lambda x:(
            x['StatProduct'] * x['Stats']['Defence'],
            x['Stats']['Attack'],
            x['Stats']['Stamina'],
            x['CP'],
            x['Ivs']['Stamina']
        ), reverse=True)

    monTypes = await getTypesFromPokeAPI(dexNum)

    embed = discord.Embed(title=f'PvP Ranks for {getMonName(dexNum)} under {modifiers["LeagueLimit"]}',
                          description=f'Attack: {modifiers["BaseStats"]["Attack"]:g}\nDefence: {modifiers["BaseStats"]["Defence"]:g}\nStamina: {modifiers["BaseStats"]["Stamina"]:g}',
                          color=getTypeColour(monTypes[0]))
    
    embed.add_field(name=f'Ranks Prioritizing {getRankSortOrderText(modifiers["ResultSortOrder"])}',
                    value=f'Floor: {modifiers["Floor"]} | LvRange: {modifiers["MinLevel"]:g}-{modifiers["MaxLevel"]:g}',
                    inline=False)
    
    fieldContent = ['', '', '']

    for i, rank in enumerate(rankList, start=1):
        fieldContent[0] += f'R{rank["Rank"]} Lv{rank["Level"]:g}\n'
        fieldContent[1] += f'{rank["CP"]} CP | {rank["Ivs"]["Attack"]}/{rank["Ivs"]["Defence"]}/{rank["Ivs"]["Stamina"]}\n'
        fieldContent[2] += f'{pogoRound(rank["Stats"]["Attack"], 2)} / {pogoRound(rank["Stats"]["Defence"], 2)} / {rank["Stats"]["Stamina"]}\n'

        if i >= 10:
            break
    
    embed.add_field(name='Rank',
                    value=fieldContent[0],
                    inline=True)
    
    embed.add_field(name='CP & Ivs',
                    value=fieldContent[1],
                    inline=True)
    
    embed.add_field(name='Stats',
                    value=fieldContent[2],
                    inline=True)
    
    if modifiers['Compare']:
        fieldContent = ['', '', '']
        if modifiers['Rank'] != -1:
            rank = [rank for rank in rankList if rank['Rank'] == modifiers['Rank']]
            if rank is None:
                return 'The rank you\'re looking for wasn\'t found!'
            rank= rank[0]
            fieldContent[0] += f'R{rank["Rank"]} Lv{rank["Level"]:g}\n'
            fieldContent[1] += f'{rank["CP"]} CP | {rank["Ivs"]["Attack"]}/{rank["Ivs"]["Defence"]}/{rank["Ivs"]["Stamina"]}\n'
            fieldContent[2] += f'{pogoRound(rank["Stats"]["Attack"], 2)} / {pogoRound(rank["Stats"]["Defence"], 2)} / {rank["Stats"]["Stamina"]}\n'
        if modifiers['Ivs']['Attack'] != -1:
            rank = [rank for rank in rankList if rank['Ivs']['Attack'] == modifiers['Ivs']['Attack'] and rank['Ivs']['Defence'] == modifiers['Ivs']['Defence'] and rank['Ivs']['Stamina'] == modifiers['Ivs']['Stamina']]
            if rank is None:
                return 'The iv combo you\'re looking for wasn\'t found!'
            rank = rank[0]
            fieldContent[0] += f'R{rank["Rank"]} Lv{rank["Level"]:g}\n'
            fieldContent[1] += f'{rank["CP"]} CP | {rank["Ivs"]["Attack"]}/{rank["Ivs"]["Defence"]}/{rank["Ivs"]["Stamina"]}\n'
            fieldContent[2] += f'{pogoRound(rank["Stats"]["Attack"], 2)} / {pogoRound(rank["Stats"]["Defence"], 2)} / {rank["Stats"]["Stamina"]}\n'

        embed.add_field(name=fieldContent[0],
                    value='',
                    inline=True)
    
        embed.add_field(name=fieldContent[1],
                        value='',
                        inline=True)
        
        embed.add_field(name=fieldContent[2],
                        value='',
                        inline=True)
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(dexNum))

    embed.set_footer(text=modifiers['StatText'])

    return embed

def determineModifierValues(extraInputs, modifiers):
    errorText = ''

    for input in extraInputs:
        if '/' in input:
            ivs = re.split(r'[/]+', input)
            try:
                for iv in ivs:
                    if 0 > int(iv) or int(iv) > 15:
                        raise Exception
                modifiers['Ivs']['Attack'] = int(ivs[0])
                modifiers['Ivs']['Defence'] = int(ivs[1])
                modifiers['Ivs']['Stamina'] = int(ivs[2])
                modifiers['Compare'] = True
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!\n'
        elif input.startswith('rank'):
            try:
                val = int(input[4:])
                if 0 > val or val > 4096:
                    raise Exception
                modifiers['Rank'] = val
                modifiers['Compare'] = True
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid rank! Keep it between 0-4096!\n'
        elif input.startswith('min'):
            try:
                if not re.fullmatch(r'\d+(\.5|\.0)?', input[3:]):
                    raise Exception
                val = float(input[3:])
                if 1.0 > val or val > 55.0:
                    raise Exception
                modifiers['MinLevel'] = float(val)
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid level! Keep it between 1 and 55!\n'
        elif input.startswith('max'):
            try:
                if not re.fullmatch(r'\d+(\.5|\.0)?', input[3:]):
                    raise Exception
                val = float(input[3:])
                if 1.0 > val or val > 55.0:
                    raise Exception
                modifiers['MaxLevel'] = float(val)
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid level! Keep it between 1 and 55!\n'
        elif input.startswith('floor'):
            try:
                floorIv = int(input[5:])
                if floorIv > 15 or floorIv < 0:
                    raise Exception
                modifiers['Floor'] = floorIv
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid floor iv! Keep it between 0-15!\n'
        elif input == 'll':
            modifiers['LeagueLimit'] = 500
        elif input == 'little':
            modifiers['LeagueLimit'] = 500
        elif input == 'gl':
            modifiers['LeagueLimit'] = 1500
        elif input == 'great':
            modifiers['LeagueLimit'] = 1500
        elif input == 'ul':
            modifiers['LeagueLimit'] = 2500
        elif input == 'ultra':
            modifiers['LeagueLimit'] = 2500
        elif input == 'ml':
            modifiers['LeagueLimit'] = 9999
        elif input == 'master':
            modifiers['LeagueLimit'] = 9999
        
        elif input == 'sortattack':
            modifiers['ResultSortOrder'] = 'ByAttack'
        elif input == 'sortdefence':
            modifiers['ResultSortOrder'] = 'ByDefence'
        elif input == 'sortdefense':
            modifiers['ResultSortOrder'] = 'ByDefence'
        
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if modifiers['MinLevel'] > modifiers['MaxLevel']:
        errorText += f'You can\'t have a minimum level higher than your maximum level!'

    return modifiers, errorText

async def calcPvpRanks(baseAttack, baseDefence, baseStamina, leagueLimit, ivFloor, minLvl, maxLvl):
    initialLevelRange = [level for level in sorted(pogoCPMultipliers.keys()) if minLvl <= level <= maxLvl]

    rankList = []
    currentMaxLvl = maxLvl

    for attackIv in range(ivFloor, 16):
        for defenceIv in range(ivFloor, 16):
            for staminaIv in range(ivFloor, 16):
                best = None

                levelRange = [level for level in initialLevelRange if level <= currentMaxLvl]
                for level in reversed(levelRange):
                    cpMultiplier = getPoGoCPMultiplier(level)
                    attackStat = calcPoGoStat(baseAttack, attackIv, cpMultiplier)
                    defenceStat = calcPoGoStat(baseDefence, defenceIv, cpMultiplier)

                    staminaStat = calcPoGoStat(baseStamina, staminaIv, cpMultiplier)
                    realStaminaStat = max(10, math.floor(staminaStat))

                    statProduct = pogoRound(attackStat * defenceStat * realStaminaStat)
                    cp = calcPoGoCP(attackStat, defenceStat, staminaStat)

                    if cp <= leagueLimit:
                        best = {
                            'CP': cp,
                            'Level': level,
                            'StatProduct': statProduct,
                            'Ivs': {
                                'Attack': attackIv,
                                'Defence': defenceIv,
                                'Stamina': staminaIv
                            },
                            'Stats': {
                                'Attack': attackStat,
                                'Defence': defenceStat,
                                'Stamina': realStaminaStat
                            }
                        }
                        break
                
                if best is None:
                    continue

                if attackIv == ivFloor and defenceIv == ivFloor and staminaIv == ivFloor:
                    currentMaxLvl = best['Level']

                rankList.append(best)

    return rankList
#endregion