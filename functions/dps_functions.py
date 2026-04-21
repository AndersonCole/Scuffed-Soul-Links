""" 
Contains the functions relating to PoGO dps. 
Usually returns data in a discord embed

Cole Anderson, Sept 2024
"""

import discord
import openai
import random
import regex as re
import math
import copy
from PIL import Image, ImageDraw
from io import BytesIO
from functions.shared_functions import (loadDataVariableFromFile, saveDataVariableToFile, 
                                        getPokeAPISpriteUrl, openHttpImage,
                                        checkForNickname, verifyMoveType, 
                                        formatCapitalize, formatTextForBackend, formatTextForDisplay,
                                        getTypesFromPokeAPI, getTypeColour, 
                                        getPoGoCPMultiplier, calcPoGoCP, calcPoGoStat, checkDuplicatePoGoMon, pogoRound, addPaginatedEmbedFields,
                                        loadShucklePersonality, rollForShiny, pokemon, pogoPokemon)
from dictionaries.shared_dictionaries import sharedFileLocations, sharedImagePaths, sharedEmbedColours, types
from dictionaries.dps_dictionaries import dpsFileLocations, defaultModifiers, activeModifiers, battleTierStats, battleStatOverrides, weather

openai.api_key = loadDataVariableFromFile(sharedFileLocations.get('ChatGPT'), False)

dpsNotes = loadDataVariableFromFile(dpsFileLocations.get('Notes'), False)

moves = loadDataVariableFromFile(dpsFileLocations.get('Moves'))

userModifiers = loadDataVariableFromFile(dpsFileLocations.get('UserModifiers'))

#dev command $dps symbol {num}
#region help commands
async def getSharedHelp(commandText):
    embed = discord.Embed(title=f'Shuckles PoGo DPS Shared Commands',
                            description=f'```{commandText} add-mon Kartana, 323, 182, 139``` Registers a mons base stats in Atk/Def/HP order\n' +
                                        f'```{commandText} delete-mon Kartana``` Deletes a mon from the registered list\n' +
                                        f'```{commandText} add-move Razor Leaf, 13, 7, 1000, Grass``` For fast moves, list their damage, energy gain, duration and type\n' +
                                        f'```{commandText} add-move Leaf Blade, 70, 33, 2400, 1250, Grass``` For charged moves, list their damage, energy cost, duration, damage window start, and type\n' +
                                        f'```{commandText} delete-move Razor Leaf``` Deletes a move from the registered list\n' +
                                        f'```{commandText} add-moveset Kartana, Razor Leaf, Leaf Blade, etc...``` Adds every move listed to a registered mon\n' +
                                        f'```{commandText} remove-moveset Kartana, Razor Leaf, Leaf Blade, etc...``` Removes every move listed from a registered mon\n' +
                                        f'```{commandText} list-mons``` Lists all the registered mons\n' +
                                        f'```{commandText} list-moves``` Lists all the registered moves\n\n' +
                                        'Everything should be case insensitive\nAlways assume stats are listed in Attack/Defence/HP order\nTimes should be enerted in milliseconds\nhttps://db.pokemongohub.net is good for checking move data.',
                            color=sharedEmbedColours.get('Default'))
    
    randNum = random.randint(0, 100)

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle'), randNum=randNum))

    return embed, randNum

async def dpsHelp():
    commandText = '$dps'
    sharedEmbed, randNum = await getSharedHelp(commandText)

    embeds = []

    embed = discord.Embed(title='Shuckles PoGo Raid DPS Commands',
                            description=f'```{commandText} check Kartana``` Calcs the dps based on the mons moveset\n' +
                                        f'```{commandText} batch-check Kartana, Meowscarada, Abomasnow``` Calcs the dps for all the listed mons, with the default modifiers\n' +
                                        f'```{commandText} modifiers``` Lists out the available DPS modifers\n' +
                                        f'```{commandText} set-modifiers``` Allows you to set default modifiers that will be used for every raid dps check\n' +
                                        f'```{commandText} reset-modifiers``` Resets your custom modifiers back to default\n\n' +
                                        f'```{commandText} add-note Necrozma Dusk Mane does way too much damage``` Adds a note to be processed by Shuckle.\n' +
                                        f'```{commandText} delete-notes``` Deletes all saved notes.\n' +
                                        f'```{commandText} check-notes How good is Necrozma Dusk``` Asks shuckle to understand what you\'ve written in the notes.\n\n' +
                                        'Everything should be case insensitive\nAlways assume stats are listed in Attack/Defence/HP order', 
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle'), randNum=randNum))
    
    embeds.append(embed)
    embeds.append(sharedEmbed)

    return embeds

async def dynamaxHelp():
    commandText = '$max'
    sharedEmbed, randNum = await getSharedHelp(commandText)

    embeds = []

    embed = discord.Embed(title=f'Shuckles PoGo Dynamax DPS Commands',
                            description=f'```{commandText} check Charizard``` Calcs the dps and max eps for the moveset for the mon\n' +
                                        f'```{commandText} batch-check Charizard, Zacian, Zamazenta``` Calcs the dps and max eps for all the listed mons, with the default modifiers\n' +
                                        f'```{commandText} modifiers``` Lists out the available Dynamax modifers\n' +
                                        f'```{commandText} set-modifiers``` Allows you to set default modifiers that will be used for every max dps check\n' +
                                        f'```{commandText} reset-modifiers``` Resets your custom modifiers back to default\n\n' +
                                        'Everything should be case insensitive\nAlways assume stats are listed in Attack/Defence/HP order',
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle'), randNum=randNum))
    
    embeds.append(embed)
    embeds.append(sharedEmbed)

    return embeds
    
async def getSharedModifiers(commandText):
    embed = discord.Embed(title='Shuckles PoGo DPS Shared Modifiers',
                            description=f'```{commandText}, Shadow, 51``` Any modifier can be applied in any order, as shown\n\n' +
                                        f'```{commandText}, 51``` Level: Calcs DPS at the specified level\n' +
                                        f'```{commandText}, 14/15/15``` IVs: Calcs from the given IVs\nAlways assume stats are listed in Attack/Defence/HP order\n\n' +
                                        f'```{commandText}, NoFastSTAB``` NoFastSTAB: Removes STAB from all the mons fast attack\n' +
                                        f'```{commandText}, NoChargedSTAB``` NoChargedSTAB: Removes STAB from all the mons charged attack\n' +
                                        f'```{commandText}, ForceFastSTAB``` ForceFastSTAB: Forces STAB on all the mons fast attacks\n' +
                                        f'```{commandText}, ForceChargedSTAB``` ForceChargedSTAB: Forces STAB on all the mons charged attacks\n' +
                                        f'```{commandText}, FastEffective1.6x``` FastEffectiveness: Applies type effectivity damage bonuses to fast moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        f'```{commandText}, ChargedEffective1.6x``` ChargedEffectiveness: Applies type effectivity damage bonuses to charged moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n\n' +
                                        f'```{commandText}, NoEnergyPenalty``` NoEnergyPenalty: Removes the penalty to 100 energy moves, which required them overcharge slightly\n' +
                                        f'```{commandText}, Shadow``` Shadow: Gives the mon a 1.2x atk boost and def nerf\n' +
                                        f'```{commandText}, FriendBoost``` FriendBoost: Adds a 1.1x boost to all attacks\n' +
                                        f'```{commandText}, WeatherBoost``` WeatherBoost: Adds a 1.2x boost to all attacks\n' +
                                        f'```{commandText}, WindyWeatherBoost``` WeatherBoost: Adds a 1.2x boost to all attacks matching the weather\n' +
                                        f'```{commandText}, MegaBoost``` MegaBoost: Adds a 1.3x boost to all attacks\n' +
                                        f'```{commandText}, PrimalBoost``` PrimalBoost: Adds a 1.1x boost to all attacks\n' +
                                        f'```{commandText}, Rayquaza MegaBoost``` MegaBoost: Adds a 1.3x or 1.1x boost to all attacks, depending on type.\n' +
                                        f'```{commandText}, BehemothBlade``` BehemothBlade: Adds a boost to all attacks\n' +
                                        f'```{commandText}, BehemothBash``` BehemothBash: Adds a boost to your defence\n\n' +
                                        f'```{commandText}, BossAtk200``` BossAtk: Sets the enemy boss attack to the specified value. The default is 200\n' +
                                        f'```{commandText}, BossDef70``` BossDef: Sets the enemy boss defence to the specified value. The default is 70\n' +
                                        f'```{commandText}, BossKyogre``` Boss: Sets the enemy boss attack and defence to that of the specified mon\n' +
                                        f'```{commandText}, Tier3``` Tier: Sets the tier of the battle. Also sets the CPM value\n' +
                                        f'```{commandText}, NoCPM``` NoCPM: If the tier is set, ignores the CPM values\n\n' +
                                        f'```{commandText}, FunnyMove``` FunnyMove: Adds a 50 energy STAB funny move, just for the one dps check.\n' +
                                        f'```{commandText}, VeryFunnyMove``` VeryFunnyMove: Adds a 100 energy STAB funny move, just for the one dps check\n\n' +
                                        f'```{commandText}, SortByFastMoves``` SortByFast: Orders the output by fast moves\n' +
                                        f'```{commandText}, SortByChargedMoves``` SortByCharged: Orders the output by charged moves\n\n' +
                                        'Everything should be case insensitive\nThese modifiers will work for both raid and dynamax dps calculations',
                            color=sharedEmbedColours.get('Default'))

    randNum = random.randint(0, 100)

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle'), randNum=randNum))

    return embed, randNum

async def raidModifiers():
    commandText = '$dps check Kartana'
    sharedEmbed, randNum = await getSharedModifiers(commandText)

    embeds = []

    embeds.append(sharedEmbed)

    embed = discord.Embed(title='Shuckles PoGo Raid Specific Modifiers',
                            description=f'```{commandText}, PartySize2``` PartySize: Calculates the party power boost based on the trainers in the party.\n' +
                                        '2 = Every 18 Attacks\n3 = Every 9 Attacks\n4 = Every 6 Attacks\n\n' +
                                        'Everything should be case insensitive\nThese modifiers will only work for raid calculations\nDefault check assumes Lv50, Hundo, Not Shadow, calculates STAB, Neutral effectiveness, No Special Boosts, Sorted by Dps',
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle'), randNum=randNum))

    embeds.append(embed)

    return embeds

async def dynamaxModifiers():
    commandText = '$max check Charizard'
    sharedEmbed, randNum = await getSharedModifiers(commandText)

    embeds = []

    embeds.append(sharedEmbed)

    embed = discord.Embed(title='Shuckles PoGo Dynamax Specific Modifiers',
                            description=f'```{commandText}, NoMaxSTAB``` NoMaxSTAB: Removes STAB from the mons max attack\n' +
                                        f'```{commandText}, MaxEffective1.6x``` MaxEffectiveness: Applies type effectivity damage bonuses to max moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        f'```{commandText}, DMax3``` DMax: Sets the level of a dynamax move\n' +
                                        f'```{commandText}, GMax3``` GMax: Sets the level of a gigantamax move\n' +
                                        f'```{commandText}, ShowCycleDps``` ShowCycleDps: Averages your dps between the charging and max phases\n' +
                                        f'```{commandText}, CycleSwapToBlastoise``` CycleSwapTo: Averages the dps between a charging mon and max move mon\n' +
                                        f'```{commandText}, CycleSwapLevel50``` CycleSwapLevel: Sets the level of the max move swap mon\n' +
                                        f'```{commandText}, CycleSwapIvs15/15/15``` CycleSwapIvs: Sets the ivs of the max move swap mon\n' +
                                        f'```{commandText}, Players2``` Players: Only for max cycles, increases the calculated stats as if there were multiple players using the same setups\n' +
                                        f'```{commandText}, PowerSpotBoost4``` PowerSpotBoost: Sets the power spot boost percentage\nLv 1 (1 helper) = +10%, Lv 2 (2-3 helpers) = +15%\nLv 3 (4-14 helpers) = +18.8%, Lv 4 (15+ helpers) = +20%\n' +
                                        f'```{commandText}, MushroomBoost``` MushroomBoost: Adds the 2x max mushroom damage multiplier\n' +
                                        f'```{commandText}, OldEnergyCalc``` OldEnergyCalc: Uses the old max energy formula\n' +
                                        f'```{commandText}, NoFastMoveCalc``` NoFastMoveCalc: Turns off the fast move only calcs\n' +
                                        f'```{commandText}, NoMaxOrb``` NoMaxOrb: Removes the extra energy gain from the max orb\n' +
                                        f'```{commandText}, SortByDps``` SortByDps: Orders the output by the dps\n' +
                                        f'```{commandText}, SortByCycleTime``` SortByCycleTime: Orders the output by the cycle time\n\n' +
                                        'Everything should be case insensitive\nThese modifiers will only work for dynamax calculations\nDefault check assumes Lv40, Hundo, calculates STAB, Assumes STAB on max moves, Neutral effectiveness, No Special Boosts, Sorted by Max Eps',
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle'), randNum=randNum))

    embeds.append(embed)

    return embeds
#endregion

#region parsing funcs
def checkDuplicateMove(moveName):
    moveName = formatTextForBackend(moveName)

    if len([obj for obj in moves if obj['Name'] == moveName]) >= 1:
        return True
    return False

def determineSTAB(forcedNone, forced, move, monTypes):
    if move['Name'].startswith('funny-move'):
        return activeModifiers.get('STABMultiplier').get('active')
    
    if forcedNone:
        return activeModifiers.get('STABMultiplier').get('inactive')
    elif forced:
        return activeModifiers.get('STABMultiplier').get('active')
    else:
        if move['MoveType'] in monTypes:
            return activeModifiers.get('STABMultiplier').get('active')
        else:
            return activeModifiers.get('STABMultiplier').get('inactive')
        
def determineWeatherMultiplier(weatherTypes, fastMove):
    if fastMove['MoveType'] in weatherTypes:
        return activeModifiers.get('WeatherMultiplier').get('active')
    return activeModifiers.get('WeatherMultiplier').get('inactive')

def determineMegaMultiplier(megaTypes, fastMove):
    if fastMove['MoveType'] in megaTypes:
        return activeModifiers.get('MegaMultiplier').get('SameType')
    return activeModifiers.get('MegaMultiplier').get('DiffType')
#endregion

#region dps moves add read delete
async def dpsAddFastMove(moveName, damage, energy, duration, moveType):
    if checkDuplicateMove(moveName):
        return 'That move is already registered!'
    
    if (1000 < damage or damage <= 0) or (100 < energy or energy <= 0) or (10000 < duration or duration <= 0):
        return 'Make sure the damage is between 1 and 1000, the energy between 1 and 100, and the duration between 1 and 10,000 ms!'

    if not verifyMoveType(moveType):
        return f'The entered type {moveType} was not recognized!'

    moveName = formatTextForBackend(moveName)

    moveType = formatCapitalize(moveType)

    duration = duration/1000

    moves.append({
        'Name': moveName,
        'Type': 'Fast',
        'Damage': damage,
        'Energy': energy,
        'Duration': duration,
        'MoveType': moveType
    })

    await saveDataVariableToFile(dpsFileLocations.get('Moves'), moves)

    return f'Fast move \'{formatTextForDisplay(moveName)}\' added successfully!'

async def dpsAddChargedMove(moveName, damage, energyDelta, duration, damageWindow, moveType):
    if checkDuplicateMove(moveName):
        return 'That move is already registered!'
    
    if (1000 < damage or damage <= 0) or (100 < energyDelta or energyDelta <= 0) or (10000 < duration or duration <= 0):
        return 'Make sure the damage is between 1 and 1000, the energy cost between 1 and 100, and the duration between 1 and 10,000 ms!'

    if  0 >= damageWindow > duration:
        return 'Make sure the damage window starts before the move ends, or is at least 1!'
    
    if not verifyMoveType(moveType):
        return f'The entered type {moveType} was not recognized!'
    
    moveName = formatTextForBackend(moveName)
    
    moveType = formatCapitalize(moveType)

    duration = duration/1000
    damageWindow = damageWindow/1000

    moves.append({
        'Name': moveName,
        'Type': 'Charged',
        'Damage': damage,
        'Energy': energyDelta,
        'Duration': duration,
        'DamageWindow': damageWindow,
        'MoveType': moveType
    })

    await saveDataVariableToFile(dpsFileLocations.get('Moves'), moves)

    return f'Charged move \'{formatTextForDisplay(moveName)}\' added successfully!'

async def dpsDeleteMove(moveName):
    if not checkDuplicateMove(moveName):
        return 'That move is not even registered yet!'
    
    moveName = formatTextForBackend(moveName)

    for mon in pogoPokemon:
        for move in mon['Moves']:
            if move['Name'] == moveName:
                mon['Moves'].remove(move)
                break

    for move in moves:
        if move['Name'] == moveName:
            moves.remove(move)
            break

    await saveDataVariableToFile(dpsFileLocations.get('Moves'), moves)
    await saveDataVariableToFile(sharedFileLocations.get('PoGoPokemon'), pogoPokemon)

    return 'Move deleted successfully!'

async def dpsAddMoveset(monName, newMoves):
    monName = checkForNickname(monName)

    if not checkDuplicatePoGoMon(monName):
        return 'That pokemon is not registered!'
    
    mon = [obj for obj in pogoPokemon if obj['Name'] == formatTextForBackend(monName)][0]

    output = ''

    for move in newMoves:
        moveName = formatTextForBackend(move)
    
        if not checkDuplicateMove(move):
            output += f'The move \'{formatTextForDisplay(moveName)}\' has not been registered!\n'
            continue

        if len([obj for obj in mon['Moves'] if obj['Name'] == formatTextForBackend(move)]) > 0:
            output += f'\'{formatTextForDisplay(moveName)}\' has already been added to {formatTextForDisplay(monName)}!\n'
            continue

        moveType = [obj for obj in moves if obj['Name'] == moveName][0]['Type']

        mon['Moves'].append({
            'Name': moveName,
            'Type': moveType
        })

        output += f'\'{formatTextForDisplay(moveName)}\' has been added to {formatTextForDisplay(monName)}!\n'

    await saveDataVariableToFile(sharedFileLocations.get('PoGoPokemon'), pogoPokemon)

    return output

async def dpsRemoveMoveset(monName, delMoves):
    monName = checkForNickname(monName)

    if not checkDuplicatePoGoMon(monName):
        return 'That pokemon is not registered!'
    
    mon = [obj for obj in pogoPokemon if obj['Name'] == monName][0]

    output = ''

    for move in delMoves:
        moveName = formatTextForBackend(move)

        if not checkDuplicateMove(move):
            output += f'The move \'{formatTextForDisplay(moveName)}\' has not been registered!\n'
            continue

        if len([obj for obj in mon['Moves'] if obj['Name'] == formatTextForBackend(move)]) == 0:
            output += f'\'{formatTextForDisplay(moveName)}\' has not been added to {formatTextForDisplay(monName)} yet!\n'
            continue

        mon['Moves'].remove(next(move for move in mon['Moves'] if move['Name'] == moveName))

        output += f'\'{formatTextForDisplay(moveName)}\' has been removed from {formatTextForDisplay(monName)}!\n'

    await saveDataVariableToFile(sharedFileLocations.get('PoGoPokemon'), pogoPokemon)

    return output

def formatFastMoveDuration(fastMove):
    return f'{fastMove["Duration"]}\n'
def formatChargedMoveDuration(chargedMove):
    return f'{chargedMove["Duration"]} | {chargedMove["DamageWindow"]}\n'

async def dpsListMoves():
    embeds = []

    embed = discord.Embed(title=f'Registered Moves',
                            description='',
                            color=sharedEmbedColours.get('Default'))

    fieldTitles = ['Move', 'Dmg & Energy', 'Duration']
    allMoves = (
        [(move, formatFastMoveDuration) for move in moves if move['Type'] == 'Fast'] +
        [(move, formatChargedMoveDuration) for move in moves if move['Type'] == 'Charged']
    )
    fieldContent = ['', '', '']

    pageCount = 15
    for i, (move, durationFormat) in enumerate(allMoves, start=1):
        
        fieldContent[0] += f'{formatTextForDisplay(move["Name"])}\n'
        fieldContent[1] += f'{move["Damage"]} | {move["Energy"]}\n'
        fieldContent[2] += durationFormat(move)
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['', '', '']

    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds
#endregion

#region dps calculations
async def batchDpsCheck(monNames, battleSystem, author):
    embeds = []
    errorText = ''

    for mon in monNames:
        embed, file = await dpsCheck(mon, battleSystem, author)

        if (isinstance(embed, str)):
            errorText += f'{embed}\n'
        else:
            embeds.append(embed)
    
    if errorText != '':
        return f'An error occured while dps checking!\n{errorText}'
    
    return embeds

async def dpsCheck(monName, battleSystem, author, extraInputs=None):
    modifiers = getDefaultModifiers(battleSystem, author)

    if extraInputs != None:
        modifiers, errorText = await determineModifierValues([str(i).strip().lower() for i in extraInputs], battleSystem, author)
        if errorText != '':
            return errorText, None
    
    monName = checkForNickname(monName)

    if not checkDuplicatePoGoMon(monName):
        return 'That pokemon is not registered!', None
    
    mon = [obj for obj in pogoPokemon if obj['Name'] == monName][0]

    monTypes = await getTypesFromPokeAPI(mon['ImageDexNum'])
    bossTypes = await getTypesFromPokeAPI(modifiers['Boss']['DexNum'])

    monAttack, monDefence, monStamina, monCP = getCalculatedStats(mon, modifiers)

    fastMoves = []
    chargedMoves = []
    fastMovesText = ''
    chargedMovesText = ''

    for move in mon['Moves']:
        if move['Type'] == 'Fast':
            fastMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            fastMovesText += f'{formatTextForDisplay(move["Name"])}, '
        else:
            chargedMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            chargedMovesText += f'{formatTextForDisplay(move["Name"])}, '

    if modifiers['UsingFunnyMove50']:
        chargedMoves.append(activeModifiers.get('ModeratelyFunnyMove'))
    if modifiers['UsingFunnyMove100']:
        chargedMoves.append(activeModifiers.get('VeryFunnyMove'))

    if len(fastMoves) == 0:
        return 'This pokemon doesn\'t have any fast moves registered to it!', None
    if len(chargedMoves) == 0:
        return 'This pokemon doesn\'t have any charged moves registered to it!', None
    
    moveNameOutput = ''
    moveDpsOutput = ''
    moveEpsOutput = ''
    moveTtdOutput = ''
    dpsResults = []

    embed = discord.Embed(title=getEmbedTitle(mon, modifiers, battleSystem),
                          description=f'{monCP} CP\nAttack: {mon["Attack"]}\nDefence: {mon["Defence"]}\nStamina: {mon["Stamina"]}\nIVs: {modifiers["Ivs"]["Attack"]}/{modifiers["Ivs"]["Defence"]}/{modifiers["Ivs"]["Stamina"]}',
                          color=getTypeColour(monTypes[0]))
    
    if battleSystem == 'dmax':
        maxMoveDamage = await calcMaxMoveDamage(modifiers['MaxMovePower'], monAttack, modifiers)

    for fastMove in fastMoves:
        modifiers['FastSTABMultiplier'] = determineSTAB(modifiers['ForceNoFastSTAB'], modifiers['ForceFastSTAB'], fastMove, monTypes)

        if modifiers['CalculateFastEffectiveness']:
            modifiers['FastEffectiveness'] = calculateMoveEffectiveness(fastMove['MoveType'], bossTypes)
        
        modifiers['FastWeatherMultiplier'] = determineWeatherMultiplier(modifiers['WeatherTypes'], fastMove)

        if modifiers['ApplyMegaBoost']:
            modifiers['FastMegaMultiplier'] = determineMegaMultiplier(modifiers['MegaTypes'], fastMove)

        if modifiers['ApplyMegaBoost']:
            if fastMove['MoveType'] in modifiers['MegaTypes']:
                modifiers['FastMegaMultiplier'] = activeModifiers.get('MegaMultiplier').get('SameType')
            else:
                modifiers['FastMegaMultiplier'] = activeModifiers.get('MegaMultiplier').get('DiffType')

        if battleSystem == 'dmax' and modifiers['SimFastAlone']:
            fastDps, fastEps = await calcMaxFastAlone(monAttack, fastMove, modifiers)

            if modifiers['ShowCycleDps']:
                maxMoveDamage, cycleDps, timeToDmax = await calcFullCycleDps(fastDps, fastEps, maxMoveDamage, modifiers)

                dpsResults.append({
                    'FastName': fastMove['Name'],
                    'ChargedName': '',
                    'DPS': cycleDps,
                    'TTD': timeToDmax
                })
            else:
                dpsResults.append({
                    'FastName': fastMove['Name'],
                    'ChargedName': '',
                    'DPS': fastDps,
                    'MaxEPS': fastEps
                })

        for chargedMove in chargedMoves:
            modifiers['ChargedSTABMultiplier'] = determineSTAB(modifiers['ForceNoChargedSTAB'], modifiers['ForceChargedSTAB'], chargedMove, monTypes)

            if modifiers['CalculateChargedEffectiveness']:
                modifiers['ChargedEffectiveness'] = calculateMoveEffectiveness(chargedMove['MoveType'], bossTypes)

            modifiers['ChargedWeatherMultiplier'] = determineWeatherMultiplier(modifiers['WeatherTypes'], chargedMove)

            if modifiers['ApplyMegaBoost']:
                modifiers['ChargedMegaMultiplier'] = determineMegaMultiplier(modifiers['MegaTypes'], chargedMove)
            
            dps = await calcOverallDPS(monAttack, monDefence, monStamina, fastMove, chargedMove, modifiers)

            if battleSystem == 'raids':
                dpsResults.append({
                    'FastName': fastMove['Name'],
                    'FastDuration': fastMove['Duration'],
                    'NewFastDuration': fastMove['Duration'],
                    'ChargedName': chargedMove['Name'],
                    'ChargedDuration': chargedMove['Duration'],
                    'NewChargedDuration': chargedMove['Duration'],
                    'DPS': dps
                })

            elif battleSystem == 'dmax':
                maxEPS = await calcMaxEPS(monAttack, monDefence, monStamina, fastMove, chargedMove, modifiers)
                
                if modifiers['ShowCycleDps']:
                    dps = dps * modifiers['CyclePlayers']
                    maxMoveDamage, cycleDps, timeToDmax = await calcFullCycleDps(dps, maxEPS, maxMoveDamage, modifiers)

                    dpsResults.append({
                        'FastName': fastMove['Name'],
                        'ChargedName': chargedMove['Name'],
                        'DPS': cycleDps,
                        'TTD': timeToDmax
                    })

                else:
                    dpsResults.append({
                        'FastName': fastMove['Name'],
                        'ChargedName': chargedMove['Name'],
                        'DPS': dps,
                        'MaxEPS': maxEPS
                    })

    #raids results sorting
    if modifiers['ResultSortOrder'] == 'ByDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['DPS'], reverse=True)

    #dmax results sorting
    elif modifiers['ResultSortOrder'] == 'ByMaxEps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['MaxEPS'], reverse=True)

    #cycle dmax results sorting
    elif modifiers['ResultSortOrder'] == 'ByCycleTime':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['TTD'])

    #both systems results sorting
    elif modifiers['ResultSortOrder'] == 'ByFast':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['FastName'])
    elif modifiers['ResultSortOrder'] == 'ByCharged':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['ChargedName'])

    for result in sortedDpsResults:
        if battleSystem == 'raids':
            moveNameOutput += f'{formatTextForDisplay(result["FastName"])} | {formatTextForDisplay(result["ChargedName"])}\n'
            moveDpsOutput += f'{pogoRound(result["DPS"], 2)}\n'
        elif battleSystem == 'dmax':
            moveNameOutput += f'{formatTextForDisplay(result["FastName"])} | {formatTextForDisplay(result["ChargedName"])}\n'
            moveDpsOutput += f'{pogoRound(result["DPS"], 2)}\n'
            if modifiers['ShowCycleDps']:
                moveTtdOutput += f'{pogoRound(result["TTD"], 2)}s\n'
            else:
                moveEpsOutput += f'{pogoRound(result["MaxEPS"], 2)}\n'

    if len(moveNameOutput) > 1024:
        return f'You exceeded the character limit by {len(moveNameOutput) - 1024} characters! Get rid of some moves!', None

    embed.add_field(name='Moveset',
                    value=moveNameOutput,
                    inline=True)

    embed.add_field(name='DPS',
                    value=moveDpsOutput,
                    inline=True)

    if battleSystem == 'dmax':

        if modifiers['ShowCycleDps']:
            if modifiers['CycleWillSwap']:
                swapMonCpMultiplier = getPoGoCPMultiplier(modifiers['CycleSwapMon']['Level'])

                swapMonAttack = calcPoGoStat(modifiers['CycleSwapMon']['Stats']['Attack'], modifiers['CycleSwapMon']['Ivs']['Attack'], swapMonCpMultiplier)
                swapMonDefence = calcPoGoStat(modifiers['CycleSwapMon']['Stats']['Defence'], modifiers['CycleSwapMon']['Ivs']['Defence'], swapMonCpMultiplier)
                swapMonStamina = calcPoGoStat(modifiers['CycleSwapMon']['Stats']['Stamina'], modifiers['CycleSwapMon']['Ivs']['Stamina'], swapMonCpMultiplier)
                embed.description = (f'{monCP} CP | {calcPoGoCP(swapMonAttack, swapMonDefence, swapMonStamina)} CP\n'
                                    f'Attack: {mon["Attack"]} | Attack: {modifiers["CycleSwapMon"]["Stats"]["Attack"]}\n'
                                    f'Defence: {mon["Defence"]} | Defence: {modifiers["CycleSwapMon"]["Stats"]["Defence"]}\n'
                                    f'Stamina: {mon["Stamina"]} | Stamina: {modifiers["CycleSwapMon"]["Stats"]["Stamina"]}\n'
                                    f'IVs: {modifiers["Ivs"]["Attack"]}/{modifiers["Ivs"]["Defence"]}/{modifiers["Ivs"]["Stamina"]} | '
                                    f'IVs: {modifiers["CycleSwapMon"]["Ivs"]["Attack"]}/{modifiers["CycleSwapMon"]["Ivs"]["Defence"]}/{modifiers["CycleSwapMon"]["Ivs"]["Stamina"]}')
            
            embed.add_field(name='Time to Max',
                            value=moveTtdOutput,
                            inline=True)
        else:
            embed.add_field(name='Max EPS',
                            value=moveEpsOutput,
                            inline=True)
        
        embed.description += f'\n\n{modifiers["MaxMoveText"]}Move Damage: {pogoRound(maxMoveDamage, 2)} dmg'

    embed.description += f'\n\nFast Moves: {fastMovesText[:-2]}\nCharged Moves: {chargedMovesText[:-2]}'

    embedImg, embedImgFile = await getEmbedImage(mon, modifiers, getTypeColour(monTypes[0]))

    embed.set_thumbnail(url=embedImg)

    return embed, embedImgFile

def getEmbedTitle(mon, modifiers, battleSystem):
    titleStart = ''
    chargerTxt = ''
    cycleSwapText = ''
    playerText = ''

    if mon['Name'] == 'eternatus':
        gmaxText = ''
    else:
        gmaxText = modifiers['GMaxText']

    if battleSystem == 'dmax':
        titleStart = 'Max '
        if modifiers['ShowCycleDps']:
            titleStart += 'Cycle '

    lvlText = str(modifiers["Level"]).rstrip("0").rstrip(".")

    if modifiers['CycleWillSwap']:
        chargerTxt = '(Charging)'
        gmaxText = ''
        cycleSwapText = f' and{modifiers["ShadowText"]}{modifiers["GMaxText"]} {formatTextForDisplay(modifiers["CycleSwapMon"]["Name"])}(Max Move) at Lv {str(modifiers["CycleSwapMon"]["Level"]).rstrip("0").rstrip(".")}'

    if modifiers['CyclePlayers'] > 1:
        playerText = f', with {int(modifiers["CyclePlayers"])} trainers'

    return f'{titleStart}DPS Calculations for{modifiers["ShadowText"]}{gmaxText} {formatTextForDisplay(mon["Name"])}{chargerTxt} at Lv {lvlText}{cycleSwapText}{playerText}'

def getCalculatedStats(mon, modifiers):
    cpMultiplier = getPoGoCPMultiplier(modifiers['Level'])

    monAttack = calcPoGoStat(mon['Attack'], modifiers['Ivs']['Attack'], cpMultiplier)
    monDefence = calcPoGoStat(mon['Defence'], modifiers['Ivs']['Defence'], cpMultiplier)
    monStamina = calcPoGoStat(mon['Stamina'], modifiers['Ivs']['Stamina'], cpMultiplier)

    monCP = calcPoGoCP(monAttack, monDefence, monStamina)

    return monAttack, monDefence, monStamina, monCP

async def calcFullCycleDps(dps, maxEPS, maxMoveDamage, modifiers):
    if modifiers['CycleWillSwap']:
        swapMonAttack = (modifiers['CycleSwapMon']['Stats']['Attack'] + 15)*getPoGoCPMultiplier(modifiers['CycleSwapMon']['Level'])
        maxMoveDamage = await calcMaxMoveDamage(modifiers['MaxMovePower'], swapMonAttack, modifiers)

    timeToDmax = calcTimeToMax(maxEPS)
    totalCycleDps = calcEntireCycleDps(dps, timeToDmax, maxMoveDamage, modifiers)

    return maxMoveDamage, totalCycleDps, timeToDmax

async def getEmbedImage(mon, modifiers, embedColour):
    imageMon = [obj for obj in pokemon if obj['Name'] == formatTextForBackend(f'{mon["Name"]}{modifiers["GMaxText"]}')]
    if len(imageMon) > 0:
        imageDexNum = imageMon[0]['DexNum']
    else:
        imageDexNum = mon['ImageDexNum']

    if modifiers['CycleWillSwap']:
        imageCycleMon = [obj for obj in pokemon if obj['Name'] == formatTextForBackend(f'{modifiers["CycleSwapMon"]["Name"]}{modifiers["GMaxText"]}')]
        if len(imageCycleMon) > 0:
            imageCycleDexNum = imageCycleMon[0]['DexNum']
        else:
            imageCycleDexNum = modifiers['CycleSwapMon']['ImageDexNum']

        combinedMonImage = await createCombinedMonsImage(mon['ImageDexNum'], imageCycleDexNum, embedColour)

        return f'attachment://maxCycle.png', combinedMonImage
    
    return getPokeAPISpriteUrl(imageDexNum), None

async def createCombinedMonsImage(chargingMonDex, maxMonDex, embedColour):
    chargingMonImg = await openHttpImage(getPokeAPISpriteUrl(chargingMonDex))
    maxMonImg = await openHttpImage(getPokeAPISpriteUrl(maxMonDex))

    width, height = chargingMonImg.size

    combinedMons = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    shiftAmountPx = 5
    shiftedChargingMon = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shiftedMaxMon = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    shiftedChargingMon.paste(chargingMonImg, (-shiftAmountPx, shiftAmountPx))
    shiftedMaxMon.paste(maxMonImg, (shiftAmountPx, -shiftAmountPx))

    chargingMask = Image.new('L', (width, height), 0)
    chargingDraw = ImageDraw.Draw(chargingMask)
    chargingDraw.polygon([(0, height), (0, 0), (width, height)], fill=255)
    maxMask = Image.new('L', (width, height), 0)
    maxDraw = ImageDraw.Draw(maxMask)
    maxDraw.polygon([(width, 0), (0, 0), (width, height)], fill=255)

    combinedMons.paste(shiftedChargingMon, (0, 0), chargingMask)
    combinedMons.paste(shiftedMaxMon, (0, 0), maxMask)

    draw = ImageDraw.Draw(combinedMons)
    draw.line([(0, 0), (width, height)], fill=((embedColour >> 16) & 0xFF, (embedColour >> 8) & 0xFF, embedColour & 0xFF, 255), width=2)

    image_in_memory = BytesIO()
    combinedMons.save(image_in_memory, format='PNG')

    image_in_memory.seek(0)
    return discord.File(image_in_memory, filename=f'maxCycle.png')

#endregion

#region modifiers
def getModifierTitle(battleSystem, author):
    if battleSystem == 'raids':
        return f'Default Raid Modifiers for {author.mention}'
    elif battleSystem == 'dmax':
        return f'Default Max Modifiers for {author.mention}'

async def getUserModifiers(battleSystem, author):
    try:
        modifiers = copy.deepcopy([obj for obj in userModifiers if obj['User'] == author][0][battleSystem])

        if modifiers == []:
            raise Exception
    except:
        return 'You haven\'t specified any default modifiers yet!'
    
    embed = discord.Embed(title=getModifierTitle(battleSystem, author),
                          description='',
                          color=sharedEmbedColours.get('Default'))
    
    

    return embed

async def setUserModifiers(extraInputs, battleSystem, author):
    if len([obj for obj in userModifiers if obj['User'] == author]) == 0:
        userModifiers.append({
            'User': author,
            'raids': {},
            'dmax': {}
        })

    modifiers, errorText = await determineModifierValues([str(i).strip().lower() for i in extraInputs], battleSystem, author)
    if errorText != '':
        return errorText
    
    [obj for obj in userModifiers if obj['User'] == author][0][battleSystem] = modifiers

    await saveDataVariableToFile(dpsFileLocations.get('UserModifiers'), userModifiers)

    return 'Default Modifiers set!'

async def resetUserModifiers(battleSystem, author):
    try:
        modifiers = copy.deepcopy([obj for obj in userModifiers if obj['User'] == author][0][battleSystem])

        if modifiers == []:
            raise Exception
    except:
        return 'You haven\'t even specified any default modifiers yet! So in a sense, they\'ve been reset already!'
    
    [obj for obj in userModifiers if obj['User'] == author][0][battleSystem] = {}

    await saveDataVariableToFile(dpsFileLocations.get('UserModifiers'), userModifiers)

    return 'Default Modifiers reset!'


def getDefaultModifiers(battleSystem, author):
    try:
        modifiers = copy.deepcopy([obj for obj in userModifiers if obj['User'] == author][0][battleSystem])

        if modifiers == {}:
            raise Exception
        
    except:
        modifiers = copy.deepcopy(defaultModifiers)
        modifiers['Level'] = defaultModifiers.get('Level').get(battleSystem)
        modifiers['ResultSortOrder'] = defaultModifiers.get('ResultSortOrder').get(battleSystem)

    return modifiers

#region shared basic modifiers
#Level, IVs, Shadow, FastEffective, ChargedEffective, NoEnergyPenalty,
#NoFastSTAB, NoChargedSTAB, ForceFastSTAB, ForceChargedSTAB,
#FriendBoost, WeatherBoost, MegaBoost,
#BehemothBlade, BehemothBash,
#BossAtk, BossDef, Boss{name}, NoCPM,
#FunnyMove, VeryFunnyMove,
#SortByFastMoves, SortByChargedMoves
async def determineModifierValues(extraInputs, battleSystem, author):
    modifiers = getDefaultModifiers(battleSystem, author)

    errorText = ''
    systemSpecificInputs = []

    for input in extraInputs:
        if re.fullmatch(r'\d+(\.5|\.0)?', input):
            try:
                val = float(input)
                if 1.0 > val or val > 55.0:
                    raise Exception
                modifiers['Level'] = float(input)
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid level! Keep it between 1 and 51!\n'
        elif '/' in input and not input.startswith('cycle'):
            ivs = re.split(r'[/]+', input)
            try:
                for iv in ivs:
                    if 0 > int(iv) or int(iv) > 15:
                        raise Exception
                modifiers['Ivs']['Attack'] = int(ivs[0])
                modifiers['Ivs']['Defence'] = int(ivs[1])
                modifiers['Ivs']['Stamina'] = int(ivs[2])
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!\n'
        elif input == 'shadow':
            modifiers['ShadowMultiplier'] = activeModifiers.get('ShadowMultiplier')
            modifiers['ShadowText'] = ' Shadow'
        elif input.startswith('fasteffective'):
            try:
                if input[-1:] != 'x':
                    raise Exception
                val = float(input[13:-1])
                if 0.1 > val or val > 10.0:
                    raise Exception
                modifiers['FastEffectiveness'] = val
                modifiers['CalculateFastEffectiveness'] = False
            except:
                errorText += f'\'{input[13:]}\' wasn\'t understood as a valid fast effectiveness value! Keep it between 0.1 and 10! And don\'t forget the x at the end!\n'
        elif input.startswith('chargedeffective'):
            try:
                if input[-1:] != 'x':
                    raise Exception
                val = float(input[16:-1])
                if 0.1 > val or val > 10.0:
                    raise Exception
                modifiers['ChargedEffectiveness'] = val
                modifiers['CalculateChargedEffectiveness'] = False
            except:
                errorText += f'\'{input[16:]}\' wasn\'t understood as a valid charged effectiveness value! Keep it between 0.1 and 10! And don\'t forget the x at the end!\n'
        elif input == 'nofaststab':
            modifiers['ForceNoFastSTAB'] = True
        elif input == 'nochargedstab':
            modifiers['ForceNoChargedSTAB'] = True
        elif input == 'forcefaststab':
            modifiers['ForceFastSTAB'] = True
        elif input == 'forcechargedstab':
            modifiers['ForceChargedSTAB'] = True
        elif input == 'noenergypenalty':
            modifiers['ApplyEnergyPenalty'] = False
        elif input == 'friendboost':
            modifiers['FriendMultiplier'] = activeModifiers.get('FriendMultiplier')
        elif 'weatherboost' in input:
            if input == 'weatherboost':
                modifiers['WeatherTypes'] = [obj['Name'] for obj in types]
            else:
                weatherTypes = weather.get(formatTextForBackend(input[:-12]), None)
                if weatherTypes is not None:
                    modifiers['WeatherTypes'] = weatherTypes
                else:
                    errorText += f'\'{input[:-12]}\' wasn\'t understood as a valid weather type!\n'
        elif 'megaboost' in input or 'primalboost' in input:
            if input == 'megaboost':
                modifiers['MegaTypes'] = [obj['Name'] for obj in types]
                modifiers['ApplyMegaBoost'] = True
            elif input == 'primalboost':
                modifiers['ApplyMegaBoost'] = True
            else:
                try:
                    megaMon = checkForNickname(input[:-5])
                    if not checkDuplicatePoGoMon(megaMon):
                        raise Exception
                    megaMon = [obj for obj in pogoPokemon if obj['Name'] == formatTextForBackend(megaMon)][0]
                    match megaMon['Name']:
                        case 'groudon-primal':
                            megaTypes = weather.get('sunny')
                        case 'kyogre-primal':
                            megaTypes = weather.get('rainy')
                        case 'rayquaza-mega':
                            megaTypes = weather.get('windy')
                        case _:
                            megaTypes = await getTypesFromPokeAPI(megaMon['ImageDexNum'])

                    modifiers['MegaTypes'] = megaTypes
                    modifiers['ApplyMegaBoost'] = True
                except:
                    errorText += f'\'{input}\' wasn\'t understood as a valid mega name! Make sure it\'s registered!\n'
        elif input == 'behemothblade':
            modifiers['ZacianMultiplier'] = activeModifiers.get('ZacianMultiplier').get(battleSystem)
            if not modifiers['UsingAdventureEffect']:
                modifiers['UsingAdventureEffect'] = True
            else:
                errorText += 'You can only use one adventure effect at a time!'
        elif input == 'behemothbash':
            modifiers['ZamazentaMultiplier'] = activeModifiers.get('ZamazentaMultiplier').get(battleSystem)
            if not modifiers['UsingAdventureEffect']:
                modifiers['UsingAdventureEffect'] = True
            else:
                errorText += 'You can only use one adventure effect at a time!'
        elif input.startswith('bossatk'):
            try:
                atkVal = int(input[7:])
                if 1 > atkVal or atkVal > 1000:
                    raise Exception
                modifiers['Boss']['Stats']['Attack'] = atkVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss attack value! Keep it between 1 and 1000!\n'
        elif input.startswith('bossdef'):
            try:
                defVal = int(input[7:])
                if 1 > defVal or defVal > 1000:
                    raise Exception
                modifiers['Boss']['Stats']['Defence'] = defVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss defence value! Keep it between 1 and 1000!\n'
        elif input.startswith('boss'):
            try:
                bossMon = checkForNickname(input[4:])
                if not checkDuplicatePoGoMon(bossMon):
                    raise Exception
                bossMon = [obj for obj in pogoPokemon if obj['Name'] == formatTextForBackend(bossMon)][0]
                modifiers['Boss']['DexNum'] = bossMon['ImageDexNum']
                modifiers['Boss']['Stats']['Attack'] = bossMon['Attack']
                modifiers['Boss']['Stats']['Defence'] = bossMon['Defence']
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss name! Make sure it\'s registered!\n'
        elif input.startswith('tier'):
            modifiers['Boss']['Tier'] = input[4:].lower()
            modifiers['Boss']['Stats']['Health'] = battleTierStats.get(input[4:], {}).get(battleSystem, {}).get('bossHealth', None)
            modifiers['Boss']['Cpm'] = battleTierStats.get(input[4:], {}).get(battleSystem, {}).get('cpmMultiplier', None)
            attackMultiplier = battleTierStats.get(input[4:], {}).get(battleSystem, {}).get('attackMultiplier', None)
            energyMultiplier = battleTierStats.get(input[4:], {}).get(battleSystem, {}).get('energyMultiplier', None)

            if attackMultiplier is not None:
                modifiers['Boss']['AttackMultiplier'] = attackMultiplier

            if energyMultiplier is not None:
                modifiers['Boss']['EnergyMultiplier'] = energyMultiplier

            if modifiers['Boss']['Stats']['Health'] is None or modifiers['Boss']['Cpm'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid raid battle tier!\n'
        elif input == 'nocpm':
            modifiers['Boss']['UseCpmMultiplier'] = False
        elif input == 'funnymove':
            modifiers['UsingFunnyMove50'] = True
        elif input == 'veryfunnymove':
            modifiers['UsingFunnyMove100'] = True
        elif input == 'sortbyfastmoves':
            modifiers['ResultSortOrder'] = 'ByFast'
        elif input == 'sortbychargedmoves':
            modifiers['ResultSortOrder'] = 'ByCharged'
        else:
            systemSpecificInputs.append(input)

    if battleSystem == 'raids':
        modifiers, errorText = await determineRaidModifierValues(modifiers, systemSpecificInputs, errorText)
    elif battleSystem == 'dmax':
        modifiers, errorText = await determineMaxModifierValues(modifiers, systemSpecificInputs, errorText)

    if modifiers['Boss']['DexNum'] != -1:
        bossName = [obj for obj in pokemon if obj['DexNum'] == modifiers['Boss']['DexNum']][0]['Name']
        hpOverride = battleStatOverrides.get(modifiers['Boss']['Tier'], {}).get(battleSystem, {}).get(bossName, {}).get('bossHealth', None)
        attackOverride = battleStatOverrides.get(modifiers['Boss']['Tier'], {}).get(battleSystem, {}).get(bossName, {}).get('attackMultiplier', None)
        energyOverride = battleStatOverrides.get(modifiers['Boss']['Tier'], {}).get(battleSystem, {}).get(bossName, {}).get('energyMultiplier', None)
        cpmOverride = battleStatOverrides.get(modifiers['Boss']['Tier'], {}).get(battleSystem, {}).get(bossName, {}).get('cpmMultiplier', None)

        if hpOverride is not None:
            modifiers['Boss']['Stats']['Health'] = hpOverride

        if attackOverride is not None:
            modifiers['Boss']['AttackMultiplier'] = attackOverride

        if energyOverride is not None:
            modifiers['Boss']['EnergyMultiplier'] = energyOverride

        if cpmOverride is not None:
            modifiers['Boss']['Cpm'] = cpmOverride

    if modifiers['Boss']['UseCpmMultiplier'] and modifiers['Boss']['Cpm'] is not None:
        modifiers['Boss']['Stats']['Attack'] = modifiers['Boss']['Stats']['Attack'] * modifiers['Boss']['AttackMultiplier'] * modifiers['Boss']['Cpm']
        modifiers['Boss']['Stats']['Defence'] = modifiers['Boss']['Stats']['Defence'] * modifiers['Boss']['Cpm']

    return modifiers, errorText
#endregion

#region raid exclusive modifiers
#Party Power, Tier
async def determineRaidModifierValues(modifiers, raidInputs, errorText):

    for input in raidInputs:
        if input.startswith('partysize'):
            modifiers['PartyPowerGain'] = activeModifiers.get('PartyPowerGain').get(input[9:], None)

            if modifiers['PartyPowerGain'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid amount of trainers in a party! Keep it between 2 and 4!\n'
        
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if errorText != '':
        errorText += '\nCheck `$dps modifiers` to see all valid modifiers!' 

    return modifiers, errorText
#endregion

#region dynamax exclusive modifiers
#MaxEffective, NoMaxSTAB, PowerSpotBoost{level}, MushroomBoost
#Dmax{level}, GMax{level}, Tier{level}
#ShowCycleDps, CycleSwapTo{mon}, CycleSwapLevel{level}
#NoFastMoveCalc, NoMaxOrb, SortByDps, SortByCycleTime
async def determineMaxModifierValues(modifiers, dynamaxInputs, errorText):

    for input in dynamaxInputs:
        if input.startswith('maxeffective'):
            try:
                if input[-1:] != 'x':
                    raise Exception
                val = float(input[12:-1])
                if 0.1 > val or val > 10.0:
                    raise Exception
                modifiers['MaxEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid max move effectiveness value! Keep it between 0.1 and 10! And don\'t forget the x at the end!\n'
        elif input == 'nomaxstab':
            modifiers['MaxSTABMultiplier'] = 1.0
        elif input.startswith('powerspotboost'):
            modifiers['PowerSpotMultiplier'] = activeModifiers.get('PowerSpotMultiplier', {}).get(input[14:], None)

            if modifiers['PowerSpotMultiplier'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid power spot level! The boost level should be the amount of icons you see!\n'
        elif input == 'mushroomboost':
            modifiers['MushroomMultiplier'] = activeModifiers.get('MushroomMultiplier')
        elif input.startswith('dmax') or input.startswith('gmax'):
            maxMoveLevel = input[4:]
            modifiers['MaxMovePower'] = activeModifiers.get('MaxMovePower', {}).get(input[:4], {}).get(maxMoveLevel, None)
            modifiers['MaxMoveText'] = f'Lv {maxMoveLevel} {input[0].upper()}Max '
            
            if input.startswith('gmax'):
                modifiers['GMaxText'] = ' Gmax'

            if modifiers['MaxMovePower'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid dynamax move level!\n'
            if maxMoveLevel == '4':
                if not modifiers['UsingAdventureEffect']:
                    modifiers['UsingAdventureEffect'] = True
                else:
                    errorText += 'You can only use one adventure effect at a time!'
        elif input == 'showcycledps':
            modifiers['ShowCycleDps'] = True
            modifiers['ResultSortOrder'] = defaultModifiers.get('ResultSortOrder').get('dmax-cycle')
        elif input.startswith('cycleswapto'):
            try:
                swapMon = checkForNickname(input[11:])
                if not checkDuplicatePoGoMon(swapMon):
                    raise Exception
                swapMon = [obj for obj in pogoPokemon if obj['Name'] == formatTextForBackend(swapMon)][0]
                modifiers['ShowCycleDps'] = True
                modifiers['ResultSortOrder'] = defaultModifiers.get('ResultSortOrder').get('dmax-cycle')
                modifiers['CycleWillSwap'] = True
                modifiers['CycleSwapMon']['Name'] = swapMon['Name']
                modifiers['CycleSwapMon']['ImageDexNum'] = swapMon['ImageDexNum']
                modifiers['CycleSwapMon']['Stats']['Attack'] = swapMon['Attack']
                modifiers['CycleSwapMon']['Stats']['Defence'] = swapMon['Defence']
                modifiers['CycleSwapMon']['Stats']['Stamina'] = swapMon['Stamina']
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid mon name! Make sure it\'s registered!\n'
        elif input.startswith('cycleswaplevel'): 
            try:
                if re.fullmatch(r'\d+(\.5|\.0)?', input[14:]):
                    val = float(input[14:])
                    if 1.0 > val or val > 55.0:
                        raise Exception
                    modifiers['CycleSwapMon']['Level'] = float(input[14:])
                else:
                    raise Exception
            except:
                errorText += f'\'{input[14:]}\' wasn\'t understood as a valid level for the swapped mon! Keep it between 1 and 51!\n'
        elif input.startswith('cycleswapivs'):
            try:
                if '/' in input[12:]:
                    ivs = re.split(r'[/]+', input[12:])
                    for iv in ivs:
                        if 0 > int(iv) or int(iv) > 15:
                            raise Exception
                    modifiers['CycleSwapMon']['Ivs']['Attack'] = int(ivs[0])
                    modifiers['CycleSwapMon']['Ivs']['Defence'] = int(ivs[1])
                    modifiers['CycleSwapMon']['Ivs']['Stamina'] = int(ivs[2])
                else:
                    raise Exception
            except:
                errorText += f'\'{input[12:]}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!\n'
        elif input.startswith('players'):
            try:
                playerCount = input[7:]
                if 1 > int(playerCount) or int(playerCount) > 4:
                    raise Exception
                modifiers['CyclePlayers'] = float(int(playerCount))
            except:
                errorText += f'\'{input[12:]}\' wasn\'t understood as a valid player amount! Keep it between 1 and 4!\n'
        elif input == 'oldenergycalc':
            modifiers['UseNewMaxFormula'] = False
        elif input == 'nofastmovecalc':
            modifiers['SimFastAlone'] = False
        elif input == 'nomaxorb':
            modifiers['ApplyMaxOrb'] = False
        elif input == 'sortbycycletime':
            modifiers['ResultSortOrder'] = 'ByCycleTime'
        elif input == 'sortbydps':
            modifiers['ResultSortOrder'] = 'ByDps'
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if not modifiers['ShowCycleDps'] and modifiers['ResultSortOrder'] == 'ByCycleTime':
        errorText += f'You need to ShowCycleDps in order to be able to sort by cycle time!\n'

    if not modifiers['ShowCycleDps'] and modifiers['CyclePlayers'] > 1:
        errorText += f'You need to ShowCycleDps in order to sim with multiple players!\n'

    if errorText != '':
        errorText += '\n\nCheck `$max modifiers` to see all valid modifiers!'

    return modifiers, errorText
#endregion
#endregion

#region math calculations
async def calcOverallDPS(attack, defence, stamina, fastMove, chargedMove, modifiers):
    dpsBoss = await calcBossDPS(modifiers['EnemyDpsScaling'], modifiers['Boss']['Stats']['Attack'], defence, modifiers['ShadowMultiplier'], modifiers['ZamazentaMultiplier'])

    fastDps = await calcFastDPS(fastMove['Damage'], fastMove['Duration'], modifiers)
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMoveEnergy = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss, modifiers['ApplyEnergyPenalty'])

    fastMovesPerCharged = calcFastMovesPerCharged(fastMove['Duration'], fastEps, chargedMoveEnergy, dpsBoss)

    chargedDps = await calcChargedDPS(chargedMove['Damage'], chargedMove['Duration'], fastMovesPerCharged, modifiers)
    chargedEps = await calcChargedEPS(chargedMoveEnergy, chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastDps, fastEps, chargedDps, chargedEps)

    weaveDps = await calcWeaveDPS(fastDps, fastEps, energyEfficiency, dpsBoss)

    movesetDps = await calcFinalMovesetDPS(fastDps, chargedDps, chargedMove['Duration'], weaveDps, dpsBoss, stamina)

    finalDps = await calcFinalDPS(movesetDps, attack, modifiers['Boss']['Stats']['Defence'])

    return finalDps

async def calcMaxEPS(attack, defence, stamina, fastMove, chargedMove, modifiers):
    dpsBoss = await calcBossDPS(modifiers['EnemyDpsScaling'], modifiers['Boss']['Stats']['Attack'], defence, modifiers['ShadowMultiplier'], modifiers['ZamazentaMultiplier'])

    fastMaxEps = await calcFastMaxEPS(fastMove['Damage'], fastMove['Duration'], attack, modifiers)
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMoveEnergy = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss, modifiers['ApplyEnergyPenalty'])

    chargedMaxEps = await calcChargedMaxEPS(chargedMove['Damage'], chargedMove['Duration'], attack, modifiers)
    chargedEps = await calcChargedEPS(chargedMoveEnergy, chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastMaxEps, fastEps, chargedMaxEps, chargedEps)

    weaveMaxEps = await calcWeaveDPS(fastMaxEps, fastEps, energyEfficiency, dpsBoss)

    movesetMaxEps = await calcFinalMovesetDPS(fastMaxEps, chargedMaxEps, chargedMove['Duration'], weaveMaxEps, dpsBoss, stamina)

    movesetMaxEps = movesetMaxEps * modifiers['CyclePlayers']

    if modifiers['ApplyMaxOrb']:
        movesetMaxEps += getMaxOrbEps()

    return movesetMaxEps

async def calcMaxFastAlone(attack, fastMove, modifiers):
    fastMaxDps = await calcFastMaxDps(fastMove['Damage'], fastMove['Duration'], attack, modifiers)
    fastMaxEps = await calcFastMaxEPS(fastMove['Damage'], fastMove['Duration'], attack, modifiers)
    
    fastMaxDps = fastMaxDps * modifiers['CyclePlayers']
    fastMaxEps = fastMaxEps * modifiers['CyclePlayers']

    if modifiers['ApplyMaxOrb']:
        fastMaxEps += getMaxOrbEps()

    return fastMaxDps, fastMaxEps
    
async def checkChargedEnergy(fastEnergy, chargedEnergyDelta, chargedWindow, dpsBoss, applyEnergyPenalty):
    if chargedEnergyDelta == 100 and applyEnergyPenalty:
        chargedEnergy = chargedEnergyDelta + 0.5*(fastEnergy - 1) + chargedWindow*0.5*dpsBoss
    else:
        chargedEnergy = chargedEnergyDelta
    return int(chargedEnergy)
    
async def calcBossDPS(enemyScaling, bossAttack, defence, SHADOW_MULTIPLIER, ZAMA_BOOST):
    dpsBoss = enemyScaling*bossAttack/(defence * ZAMA_BOOST * (2.0 - SHADOW_MULTIPLIER))
    return dpsBoss

async def calcModifierValue(modifiers, moveType, fastMovesPerCharged=0.0):
    weatherMultiplier = 1.0
    megaMultiplier = 1.0
    partyPower = 1.0
    if moveType == 'Fast':
        weatherMultiplier = modifiers['FastWeatherMultiplier']
        megaMultiplier = modifiers['FastMegaMultiplier']
    elif moveType == 'Charged':
        weatherMultiplier = modifiers['ChargedWeatherMultiplier']
        megaMultiplier = modifiers['ChargedMegaMultiplier']
        partyPower = calculatePartyPowerMultiplier(fastMovesPerCharged, modifiers)
    elif moveType == 'Max':
        if len(modifiers['WeatherTypes']) > 0:
            weatherMultiplier = activeModifiers.get('WeatherMultiplier').get('active')
        if modifiers['ApplyMegaBoost']:
            megaMultiplier = activeModifiers.get('MegaMultiplier').get('SameType')
    
    modifierVal = modifiers[f'{moveType}Effectiveness'] * modifiers[f'{moveType}STABMultiplier'] * modifiers['ShadowMultiplier'] * modifiers['FriendMultiplier'] * weatherMultiplier * megaMultiplier * modifiers['PowerSpotMultiplier'] * modifiers['MushroomMultiplier'] * modifiers['ZacianMultiplier'] * partyPower

    return modifierVal

async def calcFastDPS(fastDamage, fastDuration, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Fast')
    dmgFast = (fastDamage * modifierVal) + modifiers['ExtraDpsValue']
    dpsFast = dmgFast/fastDuration
    return dpsFast

async def calcFastEPS(fastEnergy, fastDuration):
    epsFast = fastEnergy/fastDuration
    return epsFast

async def calcChargedDPS(chargedDamage, chargedDuration, fastMovesPerCharged, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Charged', fastMovesPerCharged)
    dmgCharged = (chargedDamage * modifierVal) + modifiers['ExtraDpsValue']
    dpsCharged = dmgCharged/chargedDuration
    return dpsCharged

async def calcChargedEPS(chargedEnergy, chargedDuration):
    epsCharged = chargedEnergy/chargedDuration
    return epsCharged

async def calcEnergyEfficiency(dpsFast, epsFast, dpsCharged, epsCharged):
    energyEff = (dpsCharged - dpsFast)/(epsFast + epsCharged)
    return energyEff

async def calcWeaveDPS(dpsFast, epsFast, energyEff, dpsBoss):
    dpsWeave = dpsFast + energyEff * (epsFast + (0.5 * dpsBoss))
    return dpsWeave

async def calcFinalMovesetDPS(dpsFast, dpsCharged, chargedDuration, dpsWeave, dpsBoss, stamina):
    dpsMoveset = dpsWeave - (dpsBoss/(2*stamina)) * chargedDuration * (dpsCharged - dpsFast)
    return dpsMoveset

async def calcFinalDPS(dpsMoveset, attack, defBoss):
    dpsFinal = dpsMoveset * (0.5*attack/defBoss)
    return dpsFinal

async def calcFastMaxDps(fastDamage, fastDuration, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Fast')
    dmgFast = (0.5 * fastDamage * (attack/modifiers['Boss']['Stats']['Defence']) * modifierVal) + modifiers['ExtraDpsValue']
    dpsFast = dmgFast/fastDuration
    return dpsFast
    
async def calcFastMaxEPS(fastDamage, fastDuration, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Fast')
    dmgFast = (0.5 * fastDamage * (attack/modifiers['Boss']['Stats']['Defence']) * modifierVal) + modifiers['ExtraDpsValue']
    if modifiers['UseNewMaxFormula']:
        attackEnergy = dmgFast/(modifiers['Boss']['Stats']['Health'] * (0.005 / modifiers['Boss']['EnergyMultiplier']))
    else:
        attackEnergy = math.floor(dmgFast/(modifiers['Boss']['Stats']['Health'] * 0.005))
    epsFast = max(attackEnergy, 1)/fastDuration
    return epsFast

async def calcChargedMaxEPS(chargedDamage, chargedDuration, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Charged')
    dmgCharged = (0.5 * chargedDamage * (attack/modifiers['Boss']['Stats']['Defence']) * modifierVal) + modifiers['ExtraDpsValue']
    if modifiers['UseNewMaxFormula']:
        attackEnergy = dmgCharged/(modifiers['Boss']['Stats']['Health'] * (0.005 / modifiers['Boss']['EnergyMultiplier']))
    else:
        attackEnergy = math.floor(dmgCharged/(modifiers['Boss']['Stats']['Health'] * 0.005))
    epsCharged = max(attackEnergy, 1)/chargedDuration
    return epsCharged

async def calcMaxMoveDamage(movePower, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Max')
    dmgMax = math.floor((0.5 * movePower * (attack/modifiers['Boss']['Stats']['Defence']) * modifierVal) + modifiers['ExtraDpsValue'])
    return dmgMax

def getMaxOrbEps():
    return activeModifiers.get('MaxOrbEnergy')/15.0

def calcTimeToMax(maxEPS):
    return 100.0/maxEPS

def calcEntireCycleDps(dps, timeToDmax, maxMoveDamage, modifiers):
    return ((dps * timeToDmax) + ((maxMoveDamage * 3)* modifiers['CyclePlayers']))/timeToDmax

def calculateMoveEffectiveness(atkType, bossTypes):
    moveEffectiveness = 1.0

    superMult = activeModifiers.get('TypeEffectiveness').get('Super')
    notVeryMult = activeModifiers.get('TypeEffectiveness').get('NotVery')

    for bossType in bossTypes:
        defType = [obj for obj in types if obj['Name'] == bossType][0]['TypeChart'].get('Defending')
        if atkType in defType.get('Super'):
            moveEffectiveness *= superMult
        elif atkType in defType.get('NotVery'):
            moveEffectiveness *= notVeryMult
        elif atkType in defType.get('Immune'):
            moveEffectiveness *= (notVeryMult * notVeryMult)
    
    return moveEffectiveness

def calculatePartyPowerMultiplier(fastMovesPerCharged, modifiers):
    avgBoost = calcAveragePartyBoost(fastMovesPerCharged, modifiers)

    return 1.0 + avgBoost

def calcFastMovesPerCharged(fastDuration, epsFast, chargedEnergy, dpsBoss):
    return chargedEnergy/((epsFast + (0.5*dpsBoss))* fastDuration)

def calcAveragePartyBoost(fastMovesPerCharged, modifiers):
    if modifiers['PartyPowerGain'] == 0.0:
        return 0.0

    #charged moves count towards party power, so the +1 accounts for that
    partyEnergyPerCharged = modifiers['PartyPowerGain'] * (fastMovesPerCharged + 1)

    return min(1.0, partyEnergyPerCharged/activeModifiers.get('PartyPowerReadyAt'))
#endregion
#endregion

#region chatgpt notes
async def addDPSNote(note):
    global dpsNotes

    dpsNotes += f'{note}\n'

    await saveDataVariableToFile(dpsFileLocations.get('Notes'), dpsNotes)

    return 'Note added successfully!'

async def clearDPSNotes():
    global dpsNotes

    noteDeletionMessage = f'All notes were deleted! Here\'s what was in there, for posterity:\n{dpsNotes}'

    dpsNotes = ''

    await saveDataVariableToFile(dpsFileLocations.get('Notes'), dpsNotes)

    return noteDeletionMessage[:2000]

async def readDPSNotes(user, userInput):
    rand_num = random.randint(1, 100)
    if rand_num > 95:
        systemContent = loadShucklePersonality('drunk')

    elif rand_num > 90:
        systemContent = loadShucklePersonality('distracted')

    elif rand_num > 85:
        systemContent = loadShucklePersonality('hollow')

    elif rand_num > 75:
        systemContent = loadShucklePersonality('haunted')

    else:
        systemContent = loadShucklePersonality('smart')

    messages = [
        {'role':'system', 'content':systemContent},
        {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
        {'role':'user', 'content':userInput}
    ]  

    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages = messages, temperature=0.8, max_tokens=500)

        return response.choices[0].message.content[:2000]
    except Exception as ex:
        return 'Anderson ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
#endregion

#if i need more later '鬼' '獣'
async def getDPSSymbol(dps):
    try:
        dps = float(dps)
    except:
        return f'\'{dps}\' isn\'t a valid number, try again!'
    
    if dps > 69:
        return '神'
    elif dps > 64:
        return '帝'
    elif dps > 59:
        return '王'
    elif dps > 54:
        return '死'
    elif dps > 49:
        return 'ゴ'
    elif dps > 44:
        return '龍'
    elif dps > 39:
        return '滅'
    elif dps > 34:
        return '攻'
    elif dps > 30:
        return 'ド'
    return '∅'

#endregion