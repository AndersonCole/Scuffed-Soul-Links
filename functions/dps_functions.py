""" 
Contains the functions relating to PoGO dps. 
Usually returns data in a discord embed

Cole Anderson, Sept 2024
"""

import discord
import openai
import json
import random
import requests
import regex as re
import math
import copy
from PIL import Image, ImageDraw
from io import BytesIO
from text_files.soul_links.soul_link_dictionaries import types
from text_files.dps.dps_dictionaries import defaultModifiers, activeModifiers, battleTierStats, cpMultipliers

with open("tokens/openai_key.txt") as file:
    openai.api_key = file.read()

with open('text_files/dps/moves.txt', 'r') as file:
    moves = json.loads(file.read())

with open('text_files/dps/move_changes.txt', 'r') as file:
    changedMoves = json.loads(file.read())

with open('text_files/dps/pokemon.txt', 'r') as file:
    loadedMons = json.loads(file.read())

with open('text_files/soul_links/pokemon.txt', 'r') as file:
    pokemon = json.loads(file.read())

with open('text_files/dps/notes.txt', 'r') as file:
    dpsNotes = file.read()

#dev command $dps symbol {num}
async def dpsHelp():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

    embed = discord.Embed(title='Shuckles PoGo DPS Commands',
                            description='```$dps check Kartana``` Calcs the dps for the moveset for the mon at level 50\n' +
                                        '```$dps modifiers``` Lists out all the available modifers\n' +
                                        '```$dps add-move Razor Leaf, 13, 7, 1000, Grass``` For fast moves, list their damage, energy, and duration in milliseconds.\n' +
                                        '```$dps add-move Leaf Blade, 70, 33, 2400, 1250, Grass``` For charged moves, list their damage, energy cost, duration, and damage window start, with the times in milliseconds.\n' +
                                        '```$dps add-mon Kartana, 323, 182, 139``` Registers a mons base stats in Atk/Def/HP order.\n' +
                                        '```$dps add-moveset Kartana, Razor Leaf, Leaf Blade, etc...``` Adds every move listed to a registered mon\n' +
                                        '```$dps remove-moveset Kartana, Razor Leaf, Leaf Blade, etc...``` Removes every move listed from a registered mon, as long as they\'re registered to it.\n' +
                                        '```$dps list-mons``` Lists all the registered mons.\n' +
                                        '```$dps list-moves``` Lists all the registered moves.\n' +
                                        '```$dps list-move-changes``` Lists all the changes made in October to some moves.\n' +
                                        '```$dps delete-mon Kartana``` Deletes a mon from the registered list.\n' +
                                        '```$dps delete-move Razor Leaf``` Deletes a move from the registered list.\n' +
                                        '```$dps add-note Necrozma Dusk Mane does way too much damage``` Adds a note to be processed by Shuckle.\n' +
                                        '```$dps delete-notes``` Deletes all saved notes.\n' +
                                        '```$dps check-notes How good is Necrozma Dusk``` Asks shuckle to understand what you\'ve written in the notes.\n\n' +
                                        'Everything should be case insensitive.\nAlways assume stats are listed in Attack/Defence/HP order.\nA \'★\' beside a move name indicates its been changed in an update.\nhttps://db.pokemongohub.net is good for checking move data.', 
                            color=3553598)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://shiny_swole_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://swole_shuckle.png')
        return embed, file

async def dynamaxHelp():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

    embed = discord.Embed(title=f'Shuckles PoGo Dynamax Commands',
                            description='```$max check Charizard``` Calcs the dps and max eps for the moveset for the mon\n' +
                                        '```$max modifiers``` Lists out all the available modifers\n\n' +
                                        'The max commands use all the data added in the Raid DPS side of Shuckle.',
                            color=3553598)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://shiny_swole_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://swole_shuckle.png')
        return embed, file
    
async def getSharedModifiers(commandText):
    embed = discord.Embed(title='Shuckles PoGo Shared Modifiers',
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
                                        f'```{commandText}, MegaBoost``` MegaBoost: Adds a 1.3x boost to all attacks\n' +
                                        f'```{commandText}, BehemothBlade``` BehemothBlade: Adds a 1.2x boost to all attacks\n' +
                                        f'```{commandText}, BehemothBash``` BehemothBash: Adds a 1.2x boost to your defence\n\n' +
                                        f'```{commandText}, BossAtk200``` BossAtk: Sets the enemy boss attack to the specified value. The default is 200\n' +
                                        f'```{commandText}, BossDef70``` BossDef: Sets the enemy boss defence to the specified value. The default is 70\n' +
                                        f'```{commandText}, BossKyogre``` Boss: Sets the enemy boss attack and defence to that of the specified mon\n' +
                                        f'```{commandText}, Tier3``` Tier: Sets the tier of the battle. Also sets the CPM value\n' +
                                        f'```{commandText}, NoCPM``` NoCPM: If the tier is set, ignores the CPM values\n\n' +
                                        f'```{commandText}, SortByFastMoves``` SortByFast: Orders the output by fast moves\n' +
                                        f'```{commandText}, SortByChargedMoves``` SortByCharged: Orders the output by charged moves\n\n' +
                                        'Everything should be case insensitive\nThese modifiers will work for both raid and dynamax dps calculations',
                            color=3553598)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='https://i.imgur.com/vwke1vY.png')
    else: 
        embed.set_thumbnail(url='https://i.imgur.com/N4RHrVQ.png')

    return embed, rand_num

async def dpsModifiers():
    sharedEmbed, rand_num = await getSharedModifiers('$dps check Kartana')

    embeds = []

    embeds.append(sharedEmbed)

    embed = discord.Embed(title='Shuckles PoGo Raid Specific Modifiers',
                            description='```$dps check Kartana, PartyPower1``` PartyPower: Applies the party power boost at the specified rate\n1 = Every charged move, 2 = Every other, 3 = Every third, etc\n' +
                                        '```$dps check Kartana, ShowMoveTimings``` ShowMoveTimings: Shows the timing difference when the moves got rounded to the nearest 0.5s\n' +
                                        '```$dps check Kartana, ShowMoveChanges``` ShowMoveChanges: Adds a star beside the moves that were changed in the Oct 2024 re-balance\n' +
                                        '```$dps check Kartana, NoMoveChanges``` NoMoveChanges: Ignores the changes made to move base stats in October 2024\n' +
                                        '```$dps check Kartana, ShowOldDps``` ShowOldDps: Additionally shows the dps as it was June 2024 and prior\n' +
                                        '```$dps check Kartana, SortByOldDps``` SortByOldDps: Orders the output by the old dps\n\n' +
                                        'Everything should be case insensitive\nThese modifiers will only work for raid calculations\nDefault check assumes Lv50, Hundo, Not Shadow, calculates STAB, Neutral effectiveness, No Special Boosts, Sorted by Dps',
                            color=3553598)

    if rand_num == 69:
        embed.set_thumbnail(url='https://i.imgur.com/vwke1vY.png')
    else:
        embed.set_thumbnail(url='https://i.imgur.com/N4RHrVQ.png')

    embeds.append(embed)

    return embeds

async def dynamaxModifiers():
    sharedEmbed, rand_num = await getSharedModifiers('$max check Charizard')

    embeds = []

    embeds.append(sharedEmbed)

    embed = discord.Embed(title='Shuckles PoGo Dynamax Specific Modifiers',
                            description='```$max check Charizard, NoMaxSTAB``` NoMaxSTAB: Removes STAB from the mons max attack\n' +
                                        '```$max check Charizard, MaxEffective1.6x``` MaxEffectiveness: Applies type effectivity damage bonuses to max moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$max check Charizard, DMax3``` DMax: Sets the level of a dynamax move\n' +
                                        '```$max check Charizard, GMax3``` GMax: Sets the level of a gigantamax move\n' +
                                        '```$max check Charizard, ShowCycleDps``` ShowCycleDps: Averages your dps between the charging and max phases\n' +
                                        '```$max check Charizard, CycleSwapToBlastoise``` CycleSwapTo: Averages the dps between a charging mon and max move mon\n' +
                                        '```$max check Charizard, CycleSwapLevel50``` CycleSwapLevel: Sets the level of the max move swap mon\n' +
                                        '```$max check Charizard, CycleSwapIvs15/15/15``` CycleSwapIvs: Sets the ivs of the max move swap mon\n' +
                                        '```$max check Charizard, Players2``` Players: Only for max cycles, increases the calculated stats as if there were multiple players using the same setups\n' +
                                        '```$max check Charizard, PowerSpotBoost4``` PowerSpotBoost: Sets the power spot boost percentage\nLv 1 (1 helper) = +10%, Lv 2 (2-3 helpers) = +15%\nLv 3 (4-14 helpers) = +18.8%, Lv 4 (15+ helpers) = +20%\n' +
                                        '```$max check Charizard, MushroomBoost``` MushroomBoost: Adds the 2x max mushroom damage multiplier\n' +
                                        '```$max check Charizard, NoFastMoveCalc``` NoFastMoveCalc: Turns off the fast move only calcs\n' +
                                        '```$max check Charizard, NoMaxOrb``` NoMaxOrb: Removes the extra energy gain from the max orb\n' +
                                        '```$max check Charizard, SortByDps``` SortByDps: Orders the output by the dps\n' +
                                        '```$max check Charizard, SortByCycleTime``` SortByCycleTime: Orders the output by the cycle time\n\n' +
                                        'Everything should be case insensitive\nThese modifiers will only work for dynamax calculations\nDefault check assumes Lv40, Hundo, calculates STAB, Assumes STAB on max moves, Neutral effectiveness, No Special Boosts, Sorted by Max Eps',
                            color=3553598)

    if rand_num == 69:
        embed.set_thumbnail(url='https://i.imgur.com/vwke1vY.png')
    else:
        embed.set_thumbnail(url='https://i.imgur.com/N4RHrVQ.png')

    embeds.append(embed)

    return embeds

#region parsing funcs
def formatName(mon_name):
    mon = re.sub(r'\s', '-', str(mon_name).strip().lower())
    return mon

def checkDuplicateMon(mon_name):
    mon_name = formatName(mon_name)
    temp = [obj for obj in loadedMons if obj['Name'] == mon_name]
    if len(temp) >= 1:
        return True
    return False

def checkDuplicateMove(move_name):
    move_name = formatName(move_name)
    temp = [obj for obj in moves if obj['Name'] == move_name]
    if len(temp) >= 1:
        return True
    return False

def getDexNum(mon):
    mon = formatName(mon)
    try:
        return [obj for obj in pokemon if obj['Name'] == mon][0]['DexNum']
    except:
        return -1

def formatMoveType(moveType):
    moveType = moveType.lower()
    moveType = moveType.capitalize()
    return moveType

def verifyMoveType(moveType):
    moveType = formatMoveType(moveType)
    temp = [obj for obj in types if obj['Name'] == moveType]
    if len(temp) == 1:
        return True
    return False

def formatForDisplay(name):
    words = re.split(r'[\s-.]+', name)
    name = ' '.join(word.capitalize() for word in words)
    return name

def displayDurationChange(oldDuration, newDuration, showChanges):
    if showChanges:
        durationDiff = newDuration - oldDuration
        durationDiff = round(durationDiff, 1)
        if durationDiff >= 0:
            durationDiff = f'+{durationDiff}'
        return f'({durationDiff}s)'
    return ''

def roundDPS(dps):
    roundedDPS = round(dps, 2)
    return roundedDPS

def displayOldDps(oldDps, showDps):
    if showDps:
        return f'{oldDps} -> '
    return ''

def moveChanged(moveName):
    for move in changedMoves:
        if move['Name'] == moveName:
            return True
    return False

def getChangedMoveStats(moveName, oldPower, oldEnergy, applyChanges):
    power = oldPower
    energy = oldEnergy
    if applyChanges:
        for move in changedMoves:
            if move['Name'] == moveName:
                if move['PowerChanged']:
                    power = move['NewPower']
                if move['EnergyChanged']:
                    energy = move['NewEnergy']
                break
    return power, energy

def getOriginalFromNickname(mon):
    with open('text_files/soul_links/pokemon.txt', 'r') as file:
        pokemon = json.loads(file.read())
        
    mon = formatName(mon)
    try:
        dexNum = [obj for obj in pokemon if obj['Name'] == mon and obj['Nickname']][0]['DexNum']
        return [obj for obj in pokemon if obj['DexNum'] == dexNum][0]['Name']
    except:
        return None

#endregion

#region dps commands
async def saveDpsData():
    global moves
    global loadedMons
    global dpsNotes

    with open('text_files/dps/moves.txt', 'w') as file:
        file.write(json.dumps(moves))

    with open('text_files/dps/moves.txt', 'r') as file:
        moves = json.loads(file.read())

    with open('text_files/dps/pokemon.txt', 'w') as file:
        file.write(json.dumps(loadedMons))

    with open('text_files/dps/pokemon.txt', 'r') as file:
        loadedMons = json.loads(file.read())

    with open('text_files/dps/notes.txt', 'w') as file:
        file.write(dpsNotes)

    with open('text_files/dps/notes.txt', 'r') as file:
        dpsNotes = file.read()

async def dpsAddMon(monName, attack, defence, stamina):
    if checkDuplicateMon(monName):
        return 'That pokemon is already registered!'
    
    if (1000 < attack or attack <= 0) or (1000 < defence or defence <= 0) or (1000 < stamina or stamina <= 0):
        return 'Make sure the stats are greater than 0 or less than 1000!'
    
    dexNum = getDexNum(monName)

    if dexNum == -1:
        return f'The pokemon \'{monName}\' was not recognized!'

    monName = formatName(monName)

    loadedMons.append({
        'Name': monName,
        'ImageDexNum': dexNum,
        'Attack': attack,
        'Defence': defence,
        'Stamina': stamina,
        'Moves': []
    })

    await saveDpsData()

    return 'Mon added successfully!'

async def dpsAddFastMove(moveName, damage, energy, duration, moveType):
    if checkDuplicateMove(moveName):
        return 'That move is already registered!'
    
    if (1000 < damage or damage <= 0) or (100 < energy or energy <= 0) or (10000 < duration or duration <= 0):
        return 'Make sure the damage is between 1 and 1000, the energy between 1 and 100, and the duration between 1 and 10,000 ms!'

    if not verifyMoveType(moveType):
        return f'The entered type {moveType} was not recognized!'

    moveName = formatName(moveName)

    moveType = formatMoveType(moveType)

    duration = duration/1000

    moves.append({
        'Name': moveName,
        'Type': 'Fast',
        'Damage': damage,
        'Energy': energy,
        'Duration': duration,
        'MoveType': moveType
    })

    await saveDpsData()

    return 'Fast move added successfully!'

async def dpsAddChargedMove(moveName, damage, energyDelta, duration, damageWindow, moveType):
    if checkDuplicateMove(moveName):
        return 'That move is already registered!'
    
    if (1000 < damage or damage <= 0) or (100 < energyDelta or energyDelta <= 0) or (10000 < duration or duration <= 0):
        return 'Make sure the damage is between 1 and 1000, the energy cost between 1 and 100, and the duration between 1 and 10,000 ms!'

    if  0 >= damageWindow > duration:
        return 'Make sure the damage window starts before the move ends, or is at least 1!'
    
    if not verifyMoveType(moveType):
        return f'The entered type {moveType} was not recognized!'
    
    moveName = formatName(moveName)
    
    moveType = formatMoveType(moveType)

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

    await saveDpsData()

    return 'Charged move added successfully!'

async def dpsAddMoveset(monName, newMoves):
    if not checkDuplicateMon(monName):
        return 'That pokemon is not registered!'
    
    mon = [obj for obj in loadedMons if obj['Name'] == formatName(monName)][0]

    output = ''

    for move in newMoves:
        moveName = formatName(move)

        if not checkDuplicateMove(move):
            output += f'The move \'{formatForDisplay(moveName)}\' has not been registered!\n'
            continue

        if len([obj for obj in mon['Moves'] if obj['Name'] == formatName(move)]) > 0:
            output += f'\'{formatForDisplay(moveName)}\' has already been added to {monName}!\n'
            continue

        moveType = [obj for obj in moves if obj['Name'] == moveName][0]['Type']

        mon['Moves'].append({
            'Name': moveName,
            'Type': moveType
        })

        output += f'\'{formatForDisplay(moveName)}\' has been added to {monName}!\n'

    await saveDpsData()

    return output

async def dpsRemoveMoveset(monName, delMoves):
    if not checkDuplicateMon(monName):
        return 'That pokemon is not registered!'
    
    mon = [obj for obj in loadedMons if obj['Name'] == formatName(monName)][0]

    output = ''

    for move in delMoves:
        moveName = formatName(move)

        if not checkDuplicateMove(move):
            output += f'The move \'{formatForDisplay(moveName)}\' has not been registered!\n'
            continue

        if len([obj for obj in mon['Moves'] if obj['Name'] == formatName(move)]) == 0:
            output += f'\'{formatForDisplay(moveName)}\' has not been added to {monName} yet!\n'
            continue

        mon['Moves'].remove(next(move for move in mon['Moves'] if move['Name'] == moveName))

        output += f'\'{formatForDisplay(moveName)}\' has been removed from {monName}!\n'

    await saveDpsData()

    return output

#region read and delete commands
async def listDPSMoves():
    embeds = []

    fastMoves = []
    chargedMoves = []
    for move in moves:
        if move['Type'] == 'Fast':
            fastMoves.append(move)
        else:
            chargedMoves.append(move)

    embed = discord.Embed(title=f'Registered Moves',
                            description='',
                            color=3553598)
    
    moveText = ''
    dmgEnergyText = ''
    durationText = ''

    pageCount = 15
    for fastMove in fastMoves:
        if pageCount > 0:
            moveText += f'{formatForDisplay(fastMove["Name"])}\n'
            dmgEnergyText += f'{fastMove["Damage"]} | {fastMove["Energy"]}\n'
            durationText += f'{fastMove["Duration"]}\n'
            pageCount -= 1
        else:
            embed.add_field(name='Move',
                            value=moveText,
                            inline=True)
            
            embed.add_field(name='Dmg & Energy',
                            value=dmgEnergyText,
                            inline=True)
            
            embed.add_field(name='Duration',
                            value=durationText,
                            inline=True)
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            moveText = ''
            dmgEnergyText = ''
            durationText = ''
            pageCount = 15

    for chargedMove in chargedMoves:
        if pageCount > 0:
            moveText += f'{formatForDisplay(chargedMove["Name"])}\n'
            dmgEnergyText += f'{chargedMove["Damage"]} | {chargedMove["Energy"]}\n'
            durationText += f'{chargedMove["Duration"]} | {chargedMove["DamageWindow"]}\n'
            pageCount -= 1
        else:
            embed.add_field(name='Move',
                            value=moveText,
                            inline=True)
            
            embed.add_field(name='Dmg & Energy',
                            value=dmgEnergyText,
                            inline=True)
            
            embed.add_field(name='Duration',
                            value=durationText,
                            inline=True)
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            moveText = ''
            dmgEnergyText = ''
            durationText = ''
            pageCount = 15

    embed.add_field(name='Move',
                            value=moveText,
                            inline=True)
            
    embed.add_field(name='Dmg & Energy',
                    value=dmgEnergyText,
                    inline=True)
    
    embed.add_field(name='Duration',
                    value=durationText,
                    inline=True)
    
    embeds.append(embed)
    
    return embeds

async def listDPSMoveChanges():
    embeds = []

    embed = discord.Embed(title=f'Changed Moves',
                            description='These move changes happened in October 2024\n\'-\' means it was unchanged\nOld -> New',
                            color=3553598)

    moveText = ''
    dmgText = ''
    energyText = ''

    pageCount = 15
    for move in changedMoves:
        if pageCount > 0:
            moveText += f'{formatForDisplay(move["Name"])}\n'
            if move['PowerChanged']:
                dmgText += f'{move["OldPower"]} -> {move["NewPower"]}\n'
            else:
                dmgText += f'-\n'
            if move['EnergyChanged']:
                energyText += f'{move["OldEnergy"]} -> {move["NewEnergy"]}\n'
            else:
                energyText += f'-\n'
            pageCount -= 1
        else:
            embed.add_field(name='Move',
                            value=moveText,
                            inline=True)
            
            embed.add_field(name='Damage',
                            value=dmgText,
                            inline=True)
            
            embed.add_field(name='Energy',
                            value=energyText,
                            inline=True)
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            moveText = ''
            dmgText = ''
            energyText = ''
            pageCount = 15

    embed.add_field(name='Move',
                            value=moveText,
                            inline=True)
            
    embed.add_field(name='Damage',
                    value=dmgText,
                    inline=True)
    
    embed.add_field(name='Energy',
                    value=energyText,
                    inline=True)
    
    embeds.append(embed)
    
    return embeds

async def listDPSMons():
    embeds = []

    embed = discord.Embed(title=f'Registered Pokemon',
                            description='',
                            color=3553598)
    
    monText = ''
    statsText = ''

    pageCount = 15
    for mon in loadedMons:
        if pageCount > 0:
            monText += f'{formatForDisplay(mon["Name"])}\n'
            statsText += f'{mon["Attack"]} | {mon["Defence"]} | {mon["Stamina"]}\n'
            pageCount -= 1
        else:
            embed.add_field(name='Mon',
                            value=monText,
                            inline=True)
            
            embed.add_field(name='Stats',
                            value=statsText,
                            inline=True)
            
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            monText = ''
            statsText = ''
            pageCount = 15

    embed.add_field(name='Mon',
                            value=monText,
                            inline=True)
            
    embed.add_field(name='Stats',
                    value=statsText,
                    inline=True)
    
    embeds.append(embed)
    
    return embeds

async def deleteDPSMove(moveName):
    if not checkDuplicateMove(moveName):
        return 'That move is not even registered yet!'
    
    moveName = formatName(moveName)

    for mon in loadedMons:
        for move in mon['Moves']:
            if move['Name'] == moveName:
                mon['Moves'].remove(move)
                break

    for move in moves:
        if move['Name'] == moveName:
            moves.remove(move)
            break

    await saveDpsData()

    return 'Move deleted successfully!'

async def deleteDPSMon(monName):
    if not checkDuplicateMon(monName):
        return 'That pokemon is not even registered yet!'
    
    monName = formatName(monName)

    for mon in loadedMons:
        if mon['Name'] == monName:
            loadedMons.remove(mon)
            break

    await saveDpsData()

    return 'Mon deleted successfully!'
#endregion

#region dps calculations
async def dpsCheck(monName, battleSystem, extraInputs=None):
    modifiers = getDefaultModifiers(battleSystem)

    if extraInputs != None:
        modifiers, errorText = await determineModifierValues([str(i).strip().lower() for i in extraInputs], battleSystem)
        if errorText != '':
            return errorText, None
    
    if not checkDuplicateMon(monName):
        baseMonName = getOriginalFromNickname(monName)
        if baseMonName is not None:
            monName = baseMonName
            if not checkDuplicateMon(monName):
                return 'That pokemon is not registered!', None
        else:
            return 'That pokemon is not registered!', None
    
    monTypes = []

    mon = [obj for obj in loadedMons if obj['Name'] == formatName(monName)][0]
    if mon['ImageDexNum'] >= 0:
        monData = requests.get(f'https://pokeapi.co/api/v2/pokemon/{mon["ImageDexNum"]}')
        monData = monData.json()
        monTypes.append(str(monData['types'][0]['type']['name']).capitalize())
        if len(monData['types']) > 1:
            monTypes.append(str(monData['types'][1]['type']['name']).capitalize())
        embedColour = [obj for obj in types if obj['Name'] == monTypes[0]][0]['Colour']
    else:
        monTypes.append('???')
        embedColour = [obj for obj in types if obj['Name'] == monTypes[0]][0]['Colour']

    calculated_stats = getCalculatedStats(mon, modifiers)

    fastMoves = []
    chargedMoves = []
    fastMovesText = ''
    chargedMovesText = ''

    for move in mon['Moves']:
        changedIndicator = ''
        if modifiers['ShowMoveChanges']:
            if moveChanged(move['Name']):
                changedIndicator = '★'
        if move['Type'] == 'Fast':
            fastMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            fastMovesText += f'{formatForDisplay(move["Name"])}{changedIndicator}, '
        else:
            chargedMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            chargedMovesText += f'{formatForDisplay(move["Name"])}{changedIndicator}, '

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
                          description=f'Attack: {mon["Attack"]}\nDefence: {mon["Defence"]}\nStamina: {mon["Stamina"]}\nIVs: {modifiers["Ivs"]["Attack"]}/{modifiers["Ivs"]["Defence"]}/{modifiers["Ivs"]["Stamina"]}',
                          color=embedColour)
    
    if battleSystem == 'dmax':
        maxMoveDamage = await calcMaxMoveDamage(modifiers['MaxMovePower'], calculated_stats[0], modifiers)

    for fastMove in fastMoves:
        copiedFastMove = copy.deepcopy(fastMove)
        copiedFastMove['Damage'], copiedFastMove['Energy'] = getChangedMoveStats(copiedFastMove['Name'], copiedFastMove['Damage'], copiedFastMove['Energy'], modifiers['ApplyMoveChanges'])
        
        if modifiers['ForceNoFastSTAB']:
            modifiers['FastSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('inactive')
        elif modifiers['ForceFastSTAB']:
            modifiers['FastSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('active')
        else:
            if fastMove['MoveType'] in monTypes:
                modifiers['FastSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('active')
            else:
                modifiers['FastSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('inactive')

        newFastMove = await calcRoundedFastMoves(copiedFastMove)

        if battleSystem == 'dmax' and modifiers['SimFastAlone']:
            fastDps, fastEps = await calcMaxFastAlone(calculated_stats[0], newFastMove, modifiers)

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
            copiedChargedMove = copy.deepcopy(chargedMove)
            copiedChargedMove['Damage'], copiedChargedMove['Energy'] = getChangedMoveStats(copiedChargedMove['Name'], copiedChargedMove['Damage'], copiedChargedMove['Energy'], modifiers['ApplyMoveChanges'])

            if modifiers['ForceNoChargedSTAB']:
                modifiers['ChargedSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('inactive')
            elif modifiers['ForceChargedSTAB']:
                modifiers['ChargedSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('active')
            else:
                if chargedMove['MoveType'] in monTypes:
                    modifiers['ChargedSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('active')
                else:
                    modifiers['ChargedSTABMultiplier'] = activeModifiers.get('STABMultiplier').get('inactive')

            newChargedMove = await calcRoundedChargedMoves(copiedChargedMove)
            
            newDPS = await calcOverallDPS(calculated_stats[0], calculated_stats[1], calculated_stats[2], newFastMove, newChargedMove, modifiers)

            if battleSystem == 'raids':
                oldDPS = await calcOverallDPS(calculated_stats[0], calculated_stats[1], calculated_stats[2], fastMove, chargedMove, modifiers)

                dpsResults.append({
                    'FastName': fastMove['Name'],
                    'FastDuration': fastMove['Duration'],
                    'NewFastDuration': newFastMove['Duration'],
                    'ChargedName': chargedMove['Name'],
                    'ChargedDuration': chargedMove['Duration'],
                    'NewChargedDuration': newChargedMove['Duration'],
                    'OldDPS': oldDPS,
                    'NewDPS': newDPS
                })

            elif battleSystem == 'dmax':
                maxEPS = await calcMaxEPS(calculated_stats[0], calculated_stats[1], calculated_stats[2], newFastMove, newChargedMove, modifiers)
                
                if modifiers['ShowCycleDps']:
                    newDPS = newDPS * modifiers['CyclePlayers']
                    maxMoveDamage, cycleDps, timeToDmax = await calcFullCycleDps(newDPS, maxEPS, maxMoveDamage, modifiers)

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
                        'DPS': newDPS,
                        'MaxEPS': maxEPS
                    })

    #raids results sorting
    if modifiers['ResultSortOrder'] == 'ByNewDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['NewDPS'], reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByOldDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['OldDPS'], reverse=True)

    #dmax results sorting
    elif modifiers['ResultSortOrder'] == 'ByMaxEps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['MaxEPS'], reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['DPS'], reverse=True)
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
            moveNameOutput += f'{formatForDisplay(result["FastName"])}{displayDurationChange(result["FastDuration"], result["NewFastDuration"], modifiers["ShowMoveTimings"])} | {formatForDisplay(result["ChargedName"])}{displayDurationChange(result["ChargedDuration"], result["NewChargedDuration"], modifiers["ShowMoveTimings"])}\n'
            moveDpsOutput += f'{displayOldDps(roundDPS(result["OldDPS"]), modifiers["ShowOldDps"])}{roundDPS(result["NewDPS"])}\n'
        elif battleSystem == 'dmax':
            moveNameOutput += f'{formatForDisplay(result["FastName"])} | {formatForDisplay(result["ChargedName"])}\n'
            moveDpsOutput += f'{roundDPS(result["DPS"])}\n'
            if modifiers['ShowCycleDps']:
                moveTtdOutput += f'{roundDPS(result["TTD"])}s\n'
            else:
                moveEpsOutput += f'{roundDPS(result["MaxEPS"])}\n'

    if len(moveNameOutput) > 1024:
        return f'You exceeded the character limit by {len(moveNameOutput) - 1024} characters! Get rid of some moves!', None

    embed.add_field(name='Moveset',
                    value=moveNameOutput,
                    inline=True)
    
    if modifiers['ShowOldDps']:
        dpsFieldName = 'Old -> New'
    else:
        dpsFieldName = 'DPS'

    embed.add_field(name=dpsFieldName,
                    value=moveDpsOutput,
                    inline=True)

    if battleSystem == 'dmax':

        if modifiers['ShowCycleDps']:
            if modifiers['CycleWillSwap']:
                embed.description = (f'Attack: {mon["Attack"]} | Attack: {modifiers["CycleSwapMon"]["Attack"]}\n'
                                    f'Defence: {mon["Defence"]} | Defence: {modifiers["CycleSwapMon"]["Defence"]}\n'
                                    f'Stamina: {mon["Stamina"]} | Stamina: {modifiers["CycleSwapMon"]["Stamina"]}\n'
                                    f'IVs: {modifiers["Ivs"]["Attack"]}/{modifiers["Ivs"]["Defence"]}/{modifiers["Ivs"]["Stamina"]} | '
                                    f'IVs: {modifiers["CycleSwapMonIvs"]["Attack"]}/{modifiers["CycleSwapMonIvs"]["Defence"]}/{modifiers["CycleSwapMonIvs"]["Stamina"]}')
            
            embed.add_field(name='Time to Max',
                            value=moveTtdOutput,
                            inline=True)
        else:
            embed.add_field(name='Max EPS',
                            value=moveEpsOutput,
                            inline=True)
        
        embed.description += f'\n\n{modifiers["MaxMoveText"]} Move Damage: {roundDPS(maxMoveDamage)} dmg'

    embed.description += f'\n\nFast Moves: {fastMovesText[:-2]}\nCharged Moves: {chargedMovesText[:-2]}'

    embedImg, embedImgFile = await getEmbedImage(mon, modifiers, embedColour)

    embed.set_thumbnail(url=embedImg)

    return embed, embedImgFile

def getEmbedTitle(mon, modifiers, battleSystem):
    titleStart = ''
    gmaxText = modifiers['GMaxText']
    chargerTxt = ''
    cycleSwapText = ''
    playerText = ''

    if battleSystem == 'dmax':
        titleStart = 'Max '
        if modifiers['ShowCycleDps']:
            titleStart += 'Cycle '

    lvlText = str(modifiers["Level"]).rstrip("0").rstrip(".")

    if modifiers['CycleWillSwap']:
        chargerTxt = '(Charging)'
        gmaxText = ''
        cycleSwapText = f' and{modifiers["ShadowText"]}{modifiers["GMaxText"]} {formatForDisplay(modifiers["CycleSwapMon"]["Name"])}(Max Move) at Lv {str(modifiers["CycleSwapMonLevel"]).rstrip("0").rstrip(".")}'

    if modifiers['CyclePlayers'] > 1:
        playerText = f', with {int(modifiers["CyclePlayers"])} trainers'

    return f'{titleStart}DPS Calculations for{modifiers["ShadowText"]}{gmaxText} {formatForDisplay(mon["Name"])}{chargerTxt} at Lv {lvlText}{cycleSwapText}'

def getCalculatedStats(mon, modifiers):
    calculated_stats = []
    cpMultiplier = getCPMultiplier(modifiers['Level'])

    calculated_stats.append((mon['Attack'] + modifiers['Ivs']['Attack'])*cpMultiplier)
    calculated_stats.append((mon['Defence'] + modifiers['Ivs']['Defence'])*cpMultiplier)
    calculated_stats.append((mon['Stamina'] + modifiers['Ivs']['Stamina'])*cpMultiplier)

    return calculated_stats

async def calcFullCycleDps(dps, maxEPS, maxMoveDamage, modifiers):
    if modifiers['CycleWillSwap']:
        swapMonAttack = (modifiers['CycleSwapMon']['Attack'] + 15)*getCPMultiplier(modifiers['CycleSwapMonLevel'])
        maxMoveDamage = await calcMaxMoveDamage(modifiers['MaxMovePower'], swapMonAttack, modifiers)

    timeToDmax = calcTimeToMax(maxEPS)
    totalCycleDps = calcEntireCycleDps(dps, timeToDmax, maxMoveDamage, modifiers)

    return maxMoveDamage, totalCycleDps, timeToDmax

async def getEmbedImage(mon, modifiers, embedColour):
    imageMon = [obj for obj in pokemon if obj['Name'] == formatName(f'{mon["Name"]}{modifiers["GMaxText"]}')]
    if len(imageMon) > 0:
        imageDexNum = imageMon[0]['DexNum']
    else:
        imageDexNum = mon['ImageDexNum']

    if modifiers['CycleWillSwap']:
        imageCycleMon = [obj for obj in pokemon if obj['Name'] == formatName(f'{modifiers["CycleSwapMon"]["Name"]}{modifiers["GMaxText"]}')]
        if len(imageCycleMon) > 0:
            imageCycleDexNum = imageCycleMon[0]['DexNum']
        else:
            imageCycleDexNum = modifiers['CycleSwapMon']['ImageDexNum']

        combinedMonImage = await createCombinedMonsImage(mon['ImageDexNum'], imageCycleDexNum, embedColour)

        return f'attachment://maxCycle.png', combinedMonImage

    rand_num = random.randint(1, 100)

    if rand_num == 69:
        return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{imageDexNum}.png', None
    
    return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{imageDexNum}.png', None

async def openHttpImage(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        return Image.open(image_data).convert('RGBA')
    return Image.open(f'images/evo_helpers/missing_no.png').convert('RGBA')

async def createCombinedMonsImage(chargingMonDex, maxMonDex, embedColour):
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        chargingMonImg = await openHttpImage(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{chargingMonDex}.png')
        maxMonImg = await openHttpImage(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{maxMonDex}.png')
    else:
        chargingMonImg = await openHttpImage(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{chargingMonDex}.png')
        maxMonImg = await openHttpImage(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{maxMonDex}.png')

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
def getDefaultModifiers(battleSystem):
    modifiers = copy.deepcopy(defaultModifiers)
    modifiers['Level'] = defaultModifiers.get('Level').get(battleSystem)
    modifiers['ResultSortOrder'] = defaultModifiers.get('ResultSortOrder').get(battleSystem)
    return modifiers

#region shared basic modifiers
#Level, IVs, Shadow, FastEffective, ChargedEffective, NoEnergyPenalty
#NoFastSTAB, NoChargedSTAB, ForceFastSTAB, ForceChargedSTAB,
#FriendBoost, WeatherBoost, MegaBoost,
#BehemothBlade, BehemothBash
#BossAtk, BossDef, Boss{name}, NoCPM
#SortByFastMoves, SortByChargedMoves
async def determineModifierValues(extraInputs, battleSystem):
    modifiers = getDefaultModifiers(battleSystem)

    errorText = ''
    systemSpecificInputs = []

    for input in extraInputs:
        if re.fullmatch(r'\d+(\.5|\.0)?', input):
            try:
                val = float(input)
                if 1.0 > val or val > 51.0:
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
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid fast effectiveness value! Keep it between 0.1 and 10! And don\'t forget the x at the end!\n'
        elif input.startswith('chargedeffective'):
            try:
                if input[-1:] != 'x':
                    raise Exception
                val = float(input[16:-1])
                if 0.1 > val or val > 10.0:
                    raise Exception
                modifiers['ChargedEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid charged effectiveness value! Keep it between 0.1 and 10! And don\'t forget the x at the end!\n'
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
        elif input == 'weatherboost':
            modifiers['WeatherMultiplier'] = activeModifiers.get('WeatherMultiplier')
        elif input == 'megaboost':
            modifiers['MegaMultiplier'] = activeModifiers.get('MegaMultiplier')
        elif input == 'behemothblade':
            modifiers['ZacianMultiplier'] = activeModifiers.get('ZacianMultiplier')
        elif input == 'behemothbash':
            modifiers['ZamazentaMultiplier'] = activeModifiers.get('ZamazentaMultiplier')
        elif input.startswith('bossatk'):
            try:
                atkVal = int(input[7:])
                if 1 > atkVal or atkVal > 1000:
                    raise Exception
                modifiers['BossAttack'] = atkVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss attack value! Keep it between 1 and 1000!\n'
        elif input.startswith('bossdef'):
            try:
                defVal = int(input[7:])
                if 1 > defVal or defVal > 1000:
                    raise Exception
                modifiers['BossDefence'] = defVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss defence value! Keep it between 1 and 1000!\n'
        elif input.startswith('boss'):
            try:
                bossMon = input[4:]
                if not checkDuplicateMon(bossMon):
                    raise Exception
                bossMon = [obj for obj in loadedMons if obj['Name'] == formatName(bossMon)][0]
                modifiers['BossAttack'] = bossMon['Attack']
                modifiers['BossDefence'] = bossMon['Defence']
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss name! Make sure it\'s registered!\n'
        elif input == 'nocpm':
            modifiers['UseCpmMultiplier'] = False
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

    return modifiers, errorText
#endregion

#region raid exclusive modifiers
#Party Power, Tier
#SortByOldDps, ShowMoveChanges, NoMoveChanges
async def determineRaidModifierValues(modifiers, raidInputs, errorText):

    for input in raidInputs:
        if input.startswith('partypower'):
            try:
                multiplier = int(input[10:])
                if multiplier < 1 or multiplier > 5:
                    raise Exception
                modifiers['PartyPowerMultiplier'] = 1.0 + (1.0/float(multiplier))
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid party power value! Keep it between 1 and 5!\n'
        elif input.startswith('tier'):
            modifiers['BossHealth'] = battleTierStats.get(input[4:], {}).get('raids', {}).get('bossHealth', None)
            modifiers['CpmMultiplier'] = battleTierStats.get(input[4:], {}).get('raids', {}).get('cpmMultiplier', None)

            if modifiers['BossHealth'] is None or modifiers['CpmMultiplier'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid raid battle tier!\n'
        elif input == 'showmovetimings':
            modifiers['ShowMoveTimings'] = True
        elif input == 'showmovechanges':
            modifiers['ShowMoveChanges'] = True
        elif input == 'nomovechanges':
            modifiers['ApplyMoveChanges'] = False
        elif input == 'showolddps':
            modifiers['ShowOldDps'] = True
        elif input == 'sortbyolddps':
            modifiers['ResultSortOrder'] = 'ByOldDps'
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if not modifiers['ApplyMoveChanges'] and modifiers['ShowMoveChanges']:
        errorText += 'You have to apply the move changes to be able to see the changes!\n'

    if not modifiers['ShowOldDps'] and modifiers['ResultSortOrder'] == 'ByOldDps':
        errorText += 'You have to add ShowOldDps to be able to sort by it!\n'

    if errorText != '':
        errorText += '\nCheck `$dps modifiers` to see all valid modifiers!'
    
    if modifiers['UseCpmMultiplier'] and modifiers['CpmMultiplier'] is not None:
        modifiers['BossAttack'] = modifiers['BossAttack'] * modifiers['CpmMultiplier']
        modifiers['BossDefence'] = modifiers['BossDefence'] * modifiers['CpmMultiplier']

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
            modifiers['MaxMovePower'] = activeModifiers.get('MaxMovePower', {}).get(input[:4], {}).get(input[4:], None)
            modifiers['MaxMoveText'] = f'Lv {input[4:]} {input[0].upper()}Max '
            
            if input.startswith('gmax'):
                modifiers['GMaxText'] = ' Gmax'

            if modifiers['MaxMovePower'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid dynamax move level!\n'
        elif input.startswith('tier'):
            modifiers['BossHealth'] = battleTierStats.get(input[4:], {}).get('dmax', {}).get('bossHealth', None)
            modifiers['CpmMultiplier'] = battleTierStats.get(input[4:], {}).get('dmax', {}).get('cpmMultiplier', None)

            if modifiers['BossHealth'] is None or modifiers['CpmMultiplier'] is None:
                errorText += f'\'{input}\' wasn\'t understood as a valid dynamax battle tier!\n'
        elif input == 'showcycledps':
            modifiers['ShowCycleDps'] = True
            modifiers['ResultSortOrder'] = defaultModifiers.get('ResultSortOrder').get('dmax-cycle')
        elif input.startswith('cycleswapto'):
            try:
                swapMon = input[11:]
                if not checkDuplicateMon(swapMon):
                    raise Exception
                swapMon = [obj for obj in loadedMons if obj['Name'] == formatName(swapMon)][0]
                modifiers['ShowCycleDps'] = True
                modifiers['ResultSortOrder'] = defaultModifiers.get('ResultSortOrder').get('dmax-cycle')
                modifiers['CycleWillSwap'] = True
                modifiers['CycleSwapMon'] = swapMon
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid mon name! Make sure it\'s registered!\n'
        elif input.startswith('cycleswaplevel'): 
            try:
                if re.fullmatch(r'\d+(\.5|\.0)?', input[14:]):
                    val = float(input[14:])
                    if 1.0 > val or val > 51.0:
                        raise Exception
                    modifiers['CycleSwapMonLevel'] = float(input[14:])
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
                    modifiers['CycleSwapMonIvs']['Attack'] = int(ivs[0])
                    modifiers['CycleSwapMonIvs']['Defence'] = int(ivs[1])
                    modifiers['CycleSwapMonIvs']['Stamina'] = int(ivs[2])
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
    
    if modifiers['UseCpmMultiplier'] and modifiers['CpmMultiplier'] is not None:
        modifiers['BossAttack'] = modifiers['BossAttack'] * modifiers['CpmMultiplier']
        modifiers['BossDefence'] = modifiers['BossDefence'] * modifiers['CpmMultiplier']

    return modifiers, errorText
#endregion
#endregion

#region math calculations
async def calcOverallDPS(attack, defence, stamina, fastMove, chargedMove, modifiers):
    dpsBoss = await calcBossDPS(modifiers['EnemyDpsScaling'], modifiers['BossAttack'], defence, modifiers['ShadowMultiplier'], modifiers['ZamazentaMultiplier'])

    fastDps = await calcFastDPS(fastMove['Damage'], fastMove['Duration'], modifiers)
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMoveEnergy = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss, modifiers['ApplyEnergyPenalty'])
    chargedDps = await calcChargedDPS(chargedMove['Damage'], chargedMove['Duration'], modifiers)
    chargedEps = await calcChargedEPS(chargedMoveEnergy, chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastDps, fastEps, chargedDps, chargedEps)

    weaveDps = await calcWeaveDPS(fastDps, fastEps, energyEfficiency, dpsBoss)

    movesetDps = await calcFinalMovesetDPS(fastDps, chargedDps, chargedMove['Duration'], weaveDps, dpsBoss, stamina)

    finalDps = await calcFinalDPS(movesetDps, attack, modifiers['BossDefence'])

    return finalDps

async def calcMaxEPS(attack, defence, stamina, fastMove, chargedMove, modifiers):
    dpsBoss = await calcBossDPS(modifiers['EnemyDpsScaling'], modifiers['BossAttack'], defence, modifiers['ShadowMultiplier'], modifiers['ZamazentaMultiplier'])

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
    
async def calcBossDPS(dpsScaling, bossAttack, defence, SHADOW_MULTIPLIER, ZAMA_BOOST):
    dpsBoss = dpsScaling*bossAttack/(defence * ZAMA_BOOST * (2.0 - SHADOW_MULTIPLIER))
    return dpsBoss

'''
async def calcSurvivalTime(dpsBoss, stamina):
    survivalTime = stamina/dpsBoss
    return survivalTime
'''

async def calcModifierValue(modifiers, moveType):
    if moveType == 'Charged':
        partyPower = modifiers['PartyPowerMultiplier']
    else:
        partyPower = 1.0
    
    modifierVal = modifiers[f'{moveType}Effectiveness'] * modifiers[f'{moveType}STABMultiplier'] * modifiers['ShadowMultiplier'] * modifiers['FriendMultiplier'] * modifiers['WeatherMultiplier'] * modifiers['MegaMultiplier'] * modifiers['PowerSpotMultiplier'] * modifiers['MushroomMultiplier'] * modifiers['ZacianMultiplier'] * partyPower

    return modifierVal

async def calcFastDPS(fastDamage, fastDuration, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Fast')
    dmgFast = (fastDamage * modifierVal) + modifiers['ExtraDpsValue']
    dpsFast = dmgFast/fastDuration
    return dpsFast

async def calcFastEPS(fastEnergy, fastDuration):
    epsFast = fastEnergy/fastDuration
    return epsFast

async def calcChargedDPS(chargedDamage, chargedDuration, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Charged')
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
'''
async def calcRatio(epsFast, epsCharged, dpsBoss):
    ratio = (epsFast + (0.5*dpsBoss))/(epsFast+epsCharged)
    return ratio

async def calcCycleTime(chargedDuration, ratio):
    cycle = chargedDuration/ratio
    return cycle
'''
async def calcFinalMovesetDPS(dpsFast, dpsCharged, chargedDuration, dpsWeave, dpsBoss, stamina):
    dpsMoveset = dpsWeave - (dpsBoss/(2*stamina)) * chargedDuration * (dpsCharged - dpsFast)
    return dpsMoveset

async def calcFinalDPS(dpsMoveset, attack, defBoss):
    dpsFinal = dpsMoveset * (0.5*attack/defBoss)
    return dpsFinal

async def calcFastMaxDps(fastDamage, fastDuration, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Fast')
    dmgFast = (0.5 * fastDamage * (attack/modifiers['BossDefence']) * modifierVal) + modifiers['ExtraDpsValue']
    dpsFast = dmgFast/fastDuration
    return dpsFast
    
async def calcFastMaxEPS(fastDamage, fastDuration, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Fast')
    dmgFast = (0.5 * fastDamage * (attack/modifiers['BossDefence']) * modifierVal) + modifiers['ExtraDpsValue']
    epsFast = max(math.floor(dmgFast/(modifiers['BossHealth'] * 0.005)), 1)/fastDuration
    return epsFast

async def calcChargedMaxEPS(chargedDamage, chargedDuration, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Charged')
    dmgCharged = (0.5 * chargedDamage * (attack/modifiers['BossDefence']) * modifierVal) + modifiers['ExtraDpsValue']
    epsCharged = max(math.floor(dmgCharged/(modifiers['BossHealth'] * 0.005)), 1)/chargedDuration
    return epsCharged

async def calcMaxMoveDamage(movePower, attack, modifiers):
    modifierVal = await calcModifierValue(modifiers, 'Max')
    dmgMax = math.floor((0.5 * movePower * (attack/modifiers['BossDefence']) * modifierVal) + modifiers['ExtraDpsValue'])
    return dmgMax

def getMaxOrbEps():
    return activeModifiers.get('MaxOrbEnergy')/15.0

def calcTimeToMax(maxEPS):
    return 100.0/maxEPS

def calcEntireCycleDps(dps, timeToDmax, maxMoveDamage, modifiers):
    return ((dps * timeToDmax) + ((maxMoveDamage * 3)* modifiers['CyclePlayers']))/timeToDmax

async def calcRoundedFastMoves(move):
    newDuration = round(move['Duration']*2)/2
    newMove = {
        'Name': move['Name'],
        'Type': 'Fast',
        'Damage': move['Damage'],
        'Energy': move['Energy'],
        'Duration': newDuration
    }
    return newMove

async def calcRoundedChargedMoves(move):
    newDuration = round(move['Duration']*2)/2
    newDamageWindow = round(move['DamageWindow']*2)/2
    newMove = {
        'Name': move['Name'],
        'Type': 'Charged',
        'Damage': move['Damage'],
        'Energy': move['Energy'],
        'Duration': newDuration,
        'DamageWindow': newDamageWindow
    }
    return newMove

def getCPMultiplier(level):
    return cpMultipliers.get(level, 0)
#endregion
#endregion

#region chatgpt notes
async def addDPSNote(note):
    global dpsNotes

    dpsNotes += f'{note}\n'

    await saveDpsData()

    return 'Note added successfully!'

async def clearDPSNotes():
    global dpsNotes

    noteDeletionMessage = f'All notes were deleted! Here\'s what was in there, for posterity:\n{dpsNotes}'

    dpsNotes = ''

    await saveDpsData()

    return noteDeletionMessage[:2000]

async def readDPSNotes(user, userInput):
    rand_num = random.randint(1, 100)
    if rand_num > 95:
        with open('text_files/chat_gpt_instructions/drunkShuckle.txt', 'r') as file:
            systemContent = file.read()

        messages = [
            {'role':'system', 'content':systemContent},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    elif rand_num > 90:
        with open('text_files/chat_gpt_instructions/distractedShuckle.txt', 'r') as file:
            systemContent = file.read()

        messages = [
            {'role':'system', 'content':systemContent},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    elif rand_num > 85:
        with open('text_files/chat_gpt_instructions/hollowShuckle.txt', 'r') as file:
            systemContent = file.read()

        messages = [
            {'role':'system', 'content':systemContent},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    elif rand_num > 75:
        with open('text_files/chat_gpt_instructions/hauntedShuckle.txt', 'r') as file:
            systemContent = file.read()

        messages = [
            {'role':'system', 'content':systemContent},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    else:
        with open('text_files/chat_gpt_instructions/smartShuckle.txt', 'r') as file:
            systemContent = file.read()

        messages = [
            {'role':'system', 'content':systemContent},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]  

    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages = messages, temperature=0.8, max_tokens=500)

        return response.choices[0].message.content[:2000]
    except Exception as ex:
        return '<@341722760852013066> ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
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