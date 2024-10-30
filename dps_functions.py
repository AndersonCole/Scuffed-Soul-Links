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
from soul_link_dictionaries import types

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

    embed = discord.Embed(title=f'Shuckles PoGo DPS Commands',
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

async def dpsModifiers():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

    embed = discord.Embed(title=f'Shuckles PoGo DPS Modifiers',
                            description='```$dps check Kartana, Shadow, 40``` Any modifier can be applied in any order, as shown\n\n' +
                                        '```$dps check Kartana, 40``` Level: Calcs DPS at the specified level\n' +
                                        '```$dps check Kartana, 14/15/15``` IVs: Calcs DPS from the given IVs\nAlways assume stats are listed in Attack/Defence/HP order\n' +
                                        '```$dps check Kartana, Shadow``` Shadow: Gives the mon a 1.2x atk boost and def nerf\n' +
                                        '```$dps check Kartana, NoFastSTAB``` NoFastSTAB: Removes STAB from all the mons fast attack\n' +
                                        '```$dps check Kartana, NoChargedSTAB``` NoChargedSTAB: Removes STAB from all the mons charged attack\n' +
                                        '```$dps check Kartana, ForceFastSTAB``` ForceFastSTAB: Forces STAB on all the mons fast attacks\n' +
                                        '```$dps check Kartana, ForceChargedSTAB``` ForceChargedSTAB: Forces STAB on all the mons charged attacks\n' +
                                        '```$dps check Kartana, FastEffective1.6x``` FastEffectiveness: Applies type effectivity damage bonuses to fast moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$dps check Kartana, ChargedEffective1.6x``` ChargedEffectiveness: Applies type effectivity damage bonuses to charged moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$dps check Kartana, FriendBoost``` FriendBoost: Adds a 1.1x boost to both fast and charged attacks\n' +
                                        '```$dps check Kartana, WeatherBoost``` WeatherBoost: Adds a 1.2x boost to both fast and charged attacks\n' +
                                        '```$dps check Kartana, MegaBoost``` MegaBoost: Adds a 1.3x boost to both fast and charged attacks\n' +
                                        '```$dps check Kartana, PartyPower1``` PartyPower: Applies the party power boost at the specified rate\n1 = Every charged move, 2 = Every other, 3 = Every third, etc\n' +
                                        '```$dps check Kartana, BossAtk200``` BossAtk: Sets the enemy boss attack to the specified value. The default is 200\n' +
                                        '```$dps check Kartana, BossDef70``` BossDef: Sets the enemy boss defence to the specified value. The default is 70\n' +
                                        '```$dps check Kartana, BossKyogre``` Boss: Sets the enemy boss attack and defence to that of the specified mon\n' +
                                        '```$dps check Kartana, SortByOldDps``` SortByOldDps: Orders the output by the old dps\n' +
                                        '```$dps check Kartana, SortByFastMoves``` SortByFast: Orders the output by fast moves\n' +
                                        '```$dps check Kartana, SortByChargedMoves``` SortByCharged: Orders the output by charged moves\n' +
                                        '```$dps check Kartana, NoMoveChanges``` NoMoveChanges: Ignores the changes made to move base stats in October 2024\n\n' +
                                        'Everything should be case insensitive.\nDefault check assumes Lv50, Hundo, Not Shadow, calculates STAB, Neutral effectiveness, No Special Boosts, Sorted by Dps', 
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

async def dynamaxModifiers():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

    embed = discord.Embed(title=f'Shuckles PoGo Dynamax Modifiers',
                            description='```$max check Charizard, NoFastSTAB, 50``` Any modifier can be applied in any order, as shown\n\n' +
                                        '```$max check Charizard, 50``` Level: Calcs DPS and Max EPS at the specified level\n' +
                                        '```$max check Charizard, 14/15/15``` IVs: Calcs DPS and Max EPS from the given IVs\nAlways assume stats are listed in Attack/Defence/HP order\n' +
                                        '```$max check Charizard, NoFastSTAB``` NoFastSTAB: Removes STAB from all the mons fast attack\n' +
                                        '```$max check Charizard, NoChargedSTAB``` NoChargedSTAB: Removes STAB from all the mons charged attack\n' +
                                        '```$max check Charizard, NoMaxSTAB``` NoMaxSTAB: Removes STAB from the mons max attack\n' +
                                        '```$max check Charizard, ForceFastSTAB``` ForceFastSTAB: Forces STAB on all the mons fast attacks\n' +
                                        '```$max check Charizard, ForceChargedSTAB``` ForceChargedSTAB: Forces STAB on all the mons charged attacks\n' +
                                        '```$max check Charizard, FastEffective1.6x``` FastEffectiveness: Applies type effectivity damage bonuses to fast moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$max check Charizard, ChargedEffective1.6x``` ChargedEffectiveness: Applies type effectivity damage bonuses to charged moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$max check Charizard, MaxEffective1.6x``` MaxEffectiveness: Applies type effectivity damage bonuses to max moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$max check Charizard, FriendBoost``` FriendBoost: Adds a 1.1x boost to both fast and charged attacks\nNote that this may not actually work in real battles\n' +
                                        '```$max check Charizard, WeatherBoost``` WeatherBoost: Adds a 1.2x boost to both fast and charged attacks\nNote that this may not actually work in real battles\n' +
                                        '```$max check Charizard, MegaBoost``` MegaBoost: Adds a 1.3x boost to both fast and charged attacks.\nNote that this probably isn\'t supposed to work in real battles\n' +
                                        '```$max check Charizard, BossAtk200``` BossAtk: Sets the enemy boss attack to the specified value. The default is 200\n' +
                                        '```$max check Charizard, BossDef70``` BossDef: Sets the enemy boss defence to the specified value. The default is 70\n' +
                                        '```$max check Charizard, BossVenusaur``` Boss: Sets the enemy boss attack and defence to that of the specified mon\n' +
                                        '```$max check Charizard, DMax3``` DMax: Sets the level of a dynamax move\n' +
                                        '```$max check Charizard, GMax3``` GMax: Sets the level of a gigantamax move\n' +
                                        '```$max check Charizard, Tier3``` Tier: Sets the max energy gain modifier to that of the selected tier\n' +
                                        '```$max check Charizard, NoMaxOrb``` NoMaxOrb: Removes the extra energy gain from the max orb\n' +
                                        '```$max check Charizard, SortByDps``` SortByDps: Orders the output by the dps\n' +
                                        '```$max check Charizard, SortByFastMoves``` SortByFast: Orders the output by fast moves\n' +
                                        '```$max check Charizard, SortByChargedMoves``` SortByCharged: Orders the output by charged moves\n\n' +
                                        'Everything should be case insensitive.\nDefault check assumes Lv20, Hundo, calculates STAB, assumes STAB on max moves Neutral effectiveness, No Special Boosts, Sorted by Max Eps', 
                            color=3553598)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://shiny_swole_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://swole_shuckle.png')
        return embed, file
    
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

def displayDurationChange(oldDuration, newDuration):
    durationDiff = newDuration - oldDuration
    durationDiff = round(durationDiff, 1)
    if durationDiff >= 0:
        durationDiff = f'+{durationDiff}'
    return f'({durationDiff}s)'

def roundDPS(dps):
    roundedDPS = round(dps, 2)
    return roundedDPS

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
#region raid dps check
async def dpsCheck(monName, extraInputs=None):
    modifiers = getDefaultModifiers()

    if extraInputs != None:
        modifiers, errorText = await determineExtraInputs(extraInputs)
        if errorText != '':
            return errorText
    
    if not checkDuplicateMon(monName):
        return 'That pokemon is not registered!'
    
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

    cpMultiplier = await getCPMultiplier(modifiers['Level'])
    if cpMultiplier == 0:
        return 'Level must be between 40-51, or a multiple of 5!'
    calculated_attack = (mon['Attack'] + modifiers['AttackIv'])*cpMultiplier
    calculated_defence = (mon['Defence'] + modifiers['DefenceIv'])*cpMultiplier
    calculated_stamina = (mon['Stamina'] + modifiers['StaminaIv'])*cpMultiplier

    fastMoves = []
    chargedMoves= []
    fastMovesText = ''
    chargedMovesText = ''

    for move in mon['Moves']:
        changedIndicator = ''
        if modifiers['ApplyMoveChanges']:
            if moveChanged(move['Name']):
                changedIndicator = '★'
        if move['Type'] == 'Fast':
            fastMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            fastMovesText += f'{formatForDisplay(move["Name"])}{changedIndicator}, '
        else:
            chargedMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            chargedMovesText += f'{formatForDisplay(move["Name"])}{changedIndicator}, '

    if len(fastMoves) == 0:
        return 'This pokemon doesn\'t have any fast moves registered to it!'
    if len(chargedMoves) == 0:
        return 'This pokemon doesn\'t have any charged moves registered to it!'
    
    moveNameOutput = ''
    moveDPSOutput = ''
    dpsResults = []

    embed = discord.Embed(title=f'DPS Calculations for {modifiers["ShadowText"]}{formatForDisplay(mon["Name"])} at Lv {modifiers["Level"]}',
                          description=f'Attack: {mon["Attack"]}\nDefence: {mon["Defence"]}\nStamina: {mon["Stamina"]}\nIVs: {modifiers["AttackIv"]}/{modifiers["DefenceIv"]}/{modifiers["StaminaIv"]}\n\nFast Moves: {fastMovesText[:-2]}\nCharged Moves: {chargedMovesText[:-2]}',
                          color=embedColour)

    for fastMove in fastMoves:
        copiedFastMove = copy.deepcopy(fastMove)
        copiedFastMove['Damage'], copiedFastMove['Energy'] = getChangedMoveStats(copiedFastMove['Name'], copiedFastMove['Damage'], copiedFastMove['Energy'], modifiers['ApplyMoveChanges'])
        
        if modifiers['ForceNoFastSTAB']:
            modifiers['FastSTABMultiplier'] = 1.0
        elif modifiers['ForceFastSTAB']:
            modifiers['FastSTABMultiplier'] = 1.2
        else:
            if fastMove['MoveType'] in monTypes:
                modifiers['FastSTABMultiplier'] = 1.2
            else:
                modifiers['FastSTABMultiplier'] = 1.0

        for chargedMove in chargedMoves:
            copiedChargedMove = copy.deepcopy(chargedMove)
            copiedChargedMove['Damage'], copiedChargedMove['Energy'] = getChangedMoveStats(copiedChargedMove['Name'], copiedChargedMove['Damage'], copiedChargedMove['Energy'], modifiers['ApplyMoveChanges'])

            if modifiers['ForceNoChargedSTAB']:
                modifiers['ChargedSTABMultiplier'] = 1.0
            elif modifiers['ForceChargedSTAB']:
                modifiers['ChargedSTABMultiplier'] = 1.2
            else:
                if chargedMove['MoveType'] in monTypes:
                    modifiers['ChargedSTABMultiplier'] = 1.2
                else:
                    modifiers['ChargedSTABMultiplier'] = 1.0

            oldDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, fastMove, chargedMove, modifiers)

            newFastMove = await calcRoundedFastMoves(copiedFastMove)
            newChargedMove = await calcRoundedChargedMoves(copiedChargedMove)
            newDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, newFastMove, newChargedMove, modifiers)

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

    if modifiers['ResultSortOrder'] == 'ByNewDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['NewDPS'], reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByOldDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['OldDPS'], reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByFast':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['FastName'])
    elif modifiers['ResultSortOrder'] == 'ByCharged':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['ChargedName'])

    for result in sortedDpsResults:
        moveNameOutput += f'{formatForDisplay(result["FastName"])}{displayDurationChange(result["FastDuration"], result["NewFastDuration"])} | {formatForDisplay(result["ChargedName"])}{displayDurationChange(result["ChargedDuration"], result["NewChargedDuration"])}\n'
        moveDPSOutput += f'{roundDPS(result["OldDPS"])} -> {roundDPS(result["NewDPS"])}\n'

    if len(moveNameOutput) > 1024:
        return f'You exceeded the character limit by {len(moveNameOutput) - 1024} characters! Get rid of some moves!'

    embed.add_field(name='Moveset',
                    value=moveNameOutput,
                    inline=True)
    
    embed.add_field(name='Old -> New',
                    value=moveDPSOutput,
                    inline=True)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{mon["ImageDexNum"]}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{mon["ImageDexNum"]}.png')


    return embed
#endregion

#region dynamaxmax dps eps calcs
async def maxDpsEpsCheck(monName, extraInputs=None):
    modifiers = getDefaultModifiers()
    modifiers['Level'] = 20
    modifiers['ResultSortOrder'] = 'ByMaxEps'

    if extraInputs != None:
        modifiers, errorText = await determineExtraMaxInputs(extraInputs)
        if errorText != '':
            return errorText

    if not checkDuplicateMon(f'{monName}'):
        return 'That pokemon is not registered!'
    
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

    cpMultiplier = await getCPMultiplier(modifiers['Level'])
    if cpMultiplier == 0:
        return 'Level must be between 40-51, or a multiple of 5!'
    calculated_attack = (mon['Attack'] + modifiers['AttackIv'])*cpMultiplier
    calculated_defence = (mon['Defence'] + modifiers['DefenceIv'])*cpMultiplier
    calculated_stamina = (mon['Stamina'] + modifiers['StaminaIv'])*cpMultiplier

    fastMoves = []
    chargedMoves= []
    fastMovesText = ''
    chargedMovesText = ''

    for move in mon['Moves']:
        if move['Type'] == 'Fast':
            fastMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            fastMovesText += f'{formatForDisplay(move["Name"])}, '
        else:
            chargedMoves.append([obj for obj in moves if obj['Name'] == move['Name']][0])
            chargedMovesText += f'{formatForDisplay(move["Name"])}, '

    if len(fastMoves) == 0:
        return 'This pokemon doesn\'t have any fast moves registered to it!'
    if len(chargedMoves) == 0:
        return 'This pokemon doesn\'t have any charged moves registered to it!'

    moveNameOutput = ''
    moveDpsOutput = ''
    moveEpsOutput = ''
    dpsResults = []

    embed = discord.Embed(title=f'Max DPS Calculations for {formatForDisplay(mon["Name"])} at Lv {modifiers["Level"]}',
                          description='',
                          color=embedColour)

    for fastMove in fastMoves:
        copiedFastMove = copy.deepcopy(fastMove)
        copiedFastMove['Damage'], copiedFastMove['Energy'] = getChangedMoveStats(copiedFastMove['Name'], copiedFastMove['Damage'], copiedFastMove['Energy'], True)
        
        if modifiers['ForceNoFastSTAB']:
            modifiers['FastSTABMultiplier'] = 1.0
        elif modifiers['ForceFastSTAB']:
            modifiers['FastSTABMultiplier'] = 1.2
        else:
            if fastMove['MoveType'] in monTypes:
                modifiers['FastSTABMultiplier'] = 1.2
            else:
                modifiers['FastSTABMultiplier'] = 1.0

        for chargedMove in chargedMoves:
            copiedChargedMove = copy.deepcopy(chargedMove)
            copiedChargedMove['Damage'], copiedChargedMove['Energy'] = getChangedMoveStats(copiedChargedMove['Name'], copiedChargedMove['Damage'], copiedChargedMove['Energy'], True)

            if modifiers['ForceNoChargedSTAB']:
                modifiers['ChargedSTABMultiplier'] = 1.0
            elif modifiers['ForceChargedSTAB']:
                modifiers['ChargedSTABMultiplier'] = 1.2
            else:
                if chargedMove['MoveType'] in monTypes:
                    modifiers['ChargedSTABMultiplier'] = 1.2
                else:
                    modifiers['ChargedSTABMultiplier'] = 1.0

            newFastMove = await calcRoundedFastMoves(copiedFastMove)
            newChargedMove = await calcRoundedChargedMoves(copiedChargedMove)
            newDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, newFastMove, newChargedMove, modifiers)

            maxEPS = await calcMaxEPS(calculated_attack, calculated_defence, calculated_stamina, newFastMove, newChargedMove, modifiers)

            dpsResults.append({
                'FastName': fastMove['Name'],
                'FastDuration': newFastMove['Duration'],
                'ChargedName': chargedMove['Name'],
                'ChargedDuration': newChargedMove['Duration'],
                'DPS': newDPS,
                'MaxEPS': maxEPS
            })

    maxMoveDamage = await calcMaxMoveDamage(modifiers['MaxMovePower'], calculated_attack, modifiers['BossDefence'], modifiers['MaxEffectiveness'], modifiers['MaxSTABMultiplier'], modifiers['FriendMultiplier'], modifiers['WeatherMultiplier'], modifiers['MegaMultiplier'], modifiers['ExtraDpsValue'])

    if modifiers['ResultSortOrder'] == 'ByDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['DPS'], reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByMaxEps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['MaxEPS'], reverse=True)
    elif modifiers['ResultSortOrder'] == 'ByFast':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['FastName'])
    elif modifiers['ResultSortOrder'] == 'ByCharged':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['ChargedName'])

    for result in sortedDpsResults:
        moveNameOutput += f'{formatForDisplay(result["FastName"])} | {formatForDisplay(result["ChargedName"])}\n'
        moveDpsOutput += f'{roundDPS(result["DPS"])}\n'
        moveEpsOutput += f'{roundDPS(result["MaxEPS"])}\n'

    if len(moveNameOutput) > 1024:
        return f'You exceeded the character limit by {len(moveNameOutput) - 1024} characters! Get rid of some moves!'

    embed.description = f'Attack: {mon["Attack"]}\nDefence: {mon["Defence"]}\nStamina: {mon["Stamina"]}\nIVs: {modifiers["AttackIv"]}/{modifiers["DefenceIv"]}/{modifiers["StaminaIv"]}\n\n{modifiers["MaxMoveText"]} Move Damage: {roundDPS(maxMoveDamage)} dmg\n\nFast Moves: {fastMovesText[:-2]}\nCharged Moves: {chargedMovesText[:-2]}'

    embed.add_field(name='Moveset',
                    value=moveNameOutput,
                    inline=True)
    
    embed.add_field(name='DPS',
                    value=moveDpsOutput,
                    inline=True)
    
    embed.add_field(name='Max EPS',
                    value=moveEpsOutput,
                    inline=True)

    rand_num = random.randint(1, 100)

    if modifiers['GMaxText'] == '-gmax':
        imageDexNum = [obj for obj in pokemon if obj['Name'] == formatName(f'{monName}{modifiers["GMaxText"]}')][0]['DexNum']
    else:
        imageDexNum = mon['ImageDexNum']
    
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{imageDexNum}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{imageDexNum}.png')


    return embed
#endregion

#region modifiers
def getDefaultModifiers():
    return {
        'EnemyDpsScaling': 4.0,
        'ExtraDpsValue': 0.5,

        'Level': 50,
        'AttackIv': 15,
        'DefenceIv': 15,
        'StaminaIv': 15,

        'FastEffectiveness': 1.0,
        'ChargedEffectiveness': 1.0,

        'ForceNoFastSTAB': False,
        'ForceFastSTAB': False,
        'FastSTABMultiplier': 1.0,

        'ForceNoChargedSTAB': False,
        'ForceChargedSTAB': False,
        'ChargedSTABMultiplier': 1.0,

        'ShadowMultiplier': 1.0,
        'ShadowText': '',
        
        'FriendMultiplier': 1.0,
        'WeatherMultiplier': 1.0,
        'MegaMultiplier': 1.0,
        'PartyPowerMultiplier': 1.0,

        'BossAttack': 200,
        'BossDefence': 70,

        'MaxEffectiveness': 1.0,
        'MaxSTABMultiplier': 1.2,
        'MaxMovePower': 250,
        'GMaxText': '',
        'MaxMoveText': 'Lv 1 DMax ',

        'TierMultiplier': 50.0,
        'ApplyMaxOrb': True,

        'ApplyMoveChanges': True,

        'ResultSortOrder': 'ByNewDps'
    }

#region raid inputs
async def determineExtraInputs(extraInputs):
    modifiers = getDefaultModifiers()

    errorText = ''

    for input in extraInputs:
        if input.strip().isdigit():
            modifiers['Level'] = int(input)
        elif '/' in str(input).strip():
            ivs = re.split(r'[/]+', input.strip())
            try:
                for iv in ivs:
                    if 0 > int(iv) or int(iv) > 15:
                        raise Exception
                modifiers['AttackIv'] = int(ivs[0])
                modifiers['DefenceIv'] = int(ivs[1])
                modifiers['StaminaIv'] = int(ivs[2])
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!\n'
        elif str(input).strip().lower() == 'shadow':
            modifiers['ShadowMultiplier'] = 1.2
            modifiers['ShadowText'] = 'Shadow '
        elif str(input).strip().lower()[:13] == 'fasteffective':
            try:
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[13:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                modifiers['FastEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid fast effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!\n'
        elif str(input).strip().lower()[:16] == 'chargedeffective':
            try:
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[16:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                modifiers['ChargedEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid charged effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!\n'
        elif str(input).strip().lower() == 'nofaststab':
            modifiers['ForceNoFastSTAB'] = True
        elif str(input).strip().lower() == 'nochargedstab':
            modifiers['ForceNoChargedSTAB'] = True
        elif str(input).strip().lower() == 'forcefaststab':
            modifiers['ForceFastSTAB'] = True
        elif str(input).strip().lower() == 'forcechargedstab':
            modifiers['ForceChargedSTAB'] = True
        elif str(input).strip().lower() == 'friendboost':
            modifiers['FriendMultiplier'] = 1.1
        elif str(input).strip().lower() == 'weatherboost':
            modifiers['WeatherMultiplier'] = 1.2
        elif str(input).strip().lower() == 'megaboost':
            modifiers['MegaMultiplier'] = 1.3
        elif str(input).strip().lower()[:10] == 'partypower':
            try:
                multiplier = int(input.strip()[10:])
                if multiplier < 1 or multiplier > 5:
                    raise Exception
                modifiers['PartyPowerMultiplier'] = 1.0 + (1.0/float(multiplier))
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid party power value! Keep it between 1 and 5!\n'
        elif str(input).strip().lower()[:7] == 'bossatk':
            try:
                atkVal = int(input.strip()[7:])
                if 1 > atkVal or atkVal > 1000:
                    raise Exception
                modifiers['BossAttack'] = atkVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss attack value! Keep it between 1 and 1000!\n'
        elif str(input).strip().lower()[:7] == 'bossdef':
            try:
                defVal = int(input.strip()[7:])
                if 1 > defVal or defVal > 1000:
                    raise Exception
                modifiers['BossDefence'] = defVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss defence value! Keep it between 1 and 1000!\n'
        elif str(input).strip().lower()[:4] == 'boss':
            try:
                bossMon = input.strip().lower()[4:]
                if not checkDuplicateMon(bossMon):
                    raise Exception
                bossMon = [obj for obj in loadedMons if obj['Name'] == formatName(bossMon)][0]
                modifiers['BossAttack'] = bossMon['Attack']
                modifiers['BossDefence'] = bossMon['Defence']
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss name!\n'
        elif str(input).strip().lower() == 'sortbyolddps':
            modifiers['ResultSortOrder'] = 'ByOldDps'
        elif str(input).strip().lower() == 'sortbyfastmoves':
            modifiers['ResultSortOrder'] = 'ByFast'
        elif str(input).strip().lower() == 'sortbychargedmoves':
            modifiers['ResultSortOrder'] = 'ByCharged'
        elif str(input).strip().lower() == 'nomovechanges':
            modifiers['ApplyMoveChanges'] = False
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if errorText != '':
        errorText += '\nCheck `$dps modifiers` to see all valid modifiers!'
    
    return modifiers, errorText
#endregion

#region dynamax inputs
async def determineExtraMaxInputs(extraInputs):
    modifiers = getDefaultModifiers()

    modifiers['Level'] = 20
    modifiers['ResultSortOrder'] = 'ByMaxEps'

    errorText = ''

    for input in extraInputs:
        if input.strip().isdigit():
            modifiers['Level'] = int(input)
        elif '/' in str(input).strip():
            ivs = re.split(r'[/]+', input.strip())
            try:
                for iv in ivs:
                    if 0 > int(iv) or int(iv) > 15:
                        raise Exception
                modifiers['AttackIv'] = int(ivs[0])
                modifiers['DefenceIv'] = int(ivs[1])
                modifiers['StaminaIv'] = int(ivs[2])
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!\n'
        elif str(input).strip().lower()[:13] == 'fasteffective':
            try:
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[13:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                modifiers['FastEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid fast effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!\n'
        elif str(input).strip().lower()[:16] == 'chargedeffective':
            try:
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[16:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                modifiers['ChargedEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid charged effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!\n'
        elif str(input).strip().lower() == 'nofaststab':
            modifiers['ForceNoFastSTAB'] = True
        elif str(input).strip().lower() == 'nochargedstab':
            modifiers['ForceNoChargedSTAB'] = True
        elif str(input).strip().lower() == 'forcefaststab':
            modifiers['ForceFastSTAB'] = True
        elif str(input).strip().lower() == 'forcechargedstab':
            modifiers['ForceChargedSTAB'] = True
        elif str(input).strip().lower() == 'friendboost':
            modifiers['FriendMultiplier'] = 1.1
        elif str(input).strip().lower() == 'weatherboost':
            modifiers['WeatherMultiplier'] = 1.2
        elif str(input).strip().lower() == 'megaboost':
            modifiers['MegaMultiplier'] = 1.3
        elif str(input).strip().lower()[:7] == 'bossatk':
            try:
                atkVal = int(input.strip()[7:])
                if 1 > atkVal or atkVal > 1000:
                    raise Exception
                modifiers['BossAttack'] = atkVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss attack value! Keep it between 1 and 1000!\n'
        elif str(input).strip().lower()[:7] == 'bossdef':
            try:
                defVal = int(input.strip()[7:])
                if 1 > defVal or defVal > 1000:
                    raise Exception
                modifiers['BossDefence'] = defVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss defence value! Keep it between 1 and 1000!\n'
        elif str(input).strip().lower()[:4] == 'boss':
            try:
                bossMon = input.strip().lower()[4:]
                if not checkDuplicateMon(bossMon):
                    raise Exception
                bossMon = [obj for obj in loadedMons if obj['Name'] == formatName(bossMon)][0]
                modifiers['BossAttack'] = bossMon['Attack']
                modifiers['BossDefence'] = bossMon['Defence']
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss name!\n'
        elif str(input).strip().lower()[:12] == 'maxeffective':
            try:
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[12:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                modifiers['MaxEffectiveness'] = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid max move effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!\n'
        elif str(input).strip().lower() == 'nomaxstab':
            modifiers['MaxSTABMultiplier'] = 1.0
        elif str(input).strip().lower()[:4] == 'dmax':
            try :
                tier = int(input.strip()[4:])
                if tier == 1:
                    modifiers['MaxMovePower'] = 250
                    modifiers['MaxMoveText'] = 'Lv 1 DMax '
                elif tier == 2:
                    modifiers['MaxMovePower'] = 300
                    modifiers['MaxMoveText'] = 'Lv 2 DMax '
                elif tier == 3:
                    modifiers['MaxMovePower'] = 350
                    modifiers['MaxMoveText'] = 'Lv 3 DMax '
                else:
                    raise Exception
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid dynamax move level!\n'
        elif str(input).strip().lower()[:4] == 'gmax':
            try :
                tier = int(input.strip()[4:])
                if tier == 1:
                    modifiers['MaxMovePower'] = 350
                    modifiers['GMaxText'] = '-gmax'
                    modifiers['MaxMoveText'] = 'Lv 1 GMax '
                elif tier == 2:
                    modifiers['MaxMovePower'] = 400
                    modifiers['GMaxText'] = '-gmax'
                    modifiers['MaxMoveText'] = 'Lv 2 GMax '
                elif tier == 3:
                    modifiers['MaxMovePower'] = 450
                    modifiers['GMaxText'] = '-gmax'
                    modifiers['MaxMoveText'] = 'Lv 3 GMax '
                else:
                    raise Exception
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid dynamax move level!\n'
        elif str(input).strip().lower()[:4] == 'tier':
            try :
                tier = int(input.strip()[4:])
                if tier == 1:
                    modifiers['TierMultiplier'] = 8.5
                elif tier == 3:
                    modifiers['TierMultiplier'] = 50.0
                elif tier == 5:
                    modifiers['TierMultiplier'] = 50.0
                elif tier == 6:
                    modifiers['TierMultiplier'] = 50.0
                else:
                    raise Exception
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid dynamax battle tier!\n'
        elif str(input).strip().lower() == 'nomaxorb':
            modifiers['ApplyMaxOrb'] = False
        elif str(input).strip().lower() == 'sortbydps':
            modifiers['ResultSortOrder'] = 'ByDps'
        elif str(input).strip().lower() == 'sortbyfastmoves':
            modifiers['ResultSortOrder'] = 'ByFast'
        elif str(input).strip().lower() == 'sortbychargedmoves':
            modifiers['ResultSortOrder'] = 'ByCharged'
        else:
            errorText += f'The input \'{input}\' was not understood!\n'
            
    if errorText != '':
        errorText += '\n\nCheck `$max modifiers` to see all valid modifiers!'
    
    return modifiers, errorText
#endregion
#endregion

#region math calculations
async def calcOverallDPS(attack, defence, stamina, fastMove, chargedMove, modifiers):
    dpsBoss = await calcBossDPS(modifiers['EnemyDpsScaling'], modifiers['BossAttack'], defence, modifiers['ShadowMultiplier'])

    fastDps = await calcFastDPS(fastMove['Damage'], fastMove['Duration'], modifiers['FastEffectiveness'], modifiers['FastSTABMultiplier'], modifiers['ShadowMultiplier'], modifiers['FriendMultiplier'], modifiers['WeatherMultiplier'], modifiers['MegaMultiplier'], modifiers['ExtraDpsValue'])
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMoveEnergy = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss)
    chargedDps = await calcChargedDPS(chargedMove['Damage'], chargedMove['Duration'], modifiers['ChargedEffectiveness'], modifiers['ChargedSTABMultiplier'], modifiers['ShadowMultiplier'], modifiers['FriendMultiplier'], modifiers['WeatherMultiplier'], modifiers['MegaMultiplier'], modifiers['PartyPowerMultiplier'], modifiers['ExtraDpsValue'])
    chargedEps = await calcChargedEPS(chargedMoveEnergy, chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastDps, fastEps, chargedDps, chargedEps)

    weaveDps = await calcWeaveDPS(fastDps, fastEps, energyEfficiency, dpsBoss)

    movesetDps = await calcFinalMovesetDPS(fastDps, chargedDps, chargedMove['Duration'], weaveDps, dpsBoss, stamina)

    finalDps = await calcFinalDPS(movesetDps, attack, modifiers['BossDefence'])

    return finalDps

async def calcMaxEPS(attack, defence, stamina, fastMove, chargedMove, modifiers):
    dpsBoss = await calcBossDPS(modifiers['EnemyDpsScaling'], modifiers['BossAttack'], defence, modifiers['ShadowMultiplier'])

    fastMaxEps = await calcFastMaxEPS(fastMove['Damage'], fastMove['Duration'], modifiers['FastEffectiveness'], modifiers['FastSTABMultiplier'], modifiers['FriendMultiplier'], modifiers['WeatherMultiplier'], modifiers['MegaMultiplier'], modifiers['TierMultiplier'], modifiers['ExtraDpsValue'])
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMoveEnergy = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss)
    chargedMaxEps = await calcChargedMaxEPS(chargedMove['Damage'], chargedMove['Duration'], modifiers['ChargedEffectiveness'], modifiers['ChargedSTABMultiplier'], modifiers['FriendMultiplier'], modifiers['WeatherMultiplier'], modifiers['MegaMultiplier'], modifiers['TierMultiplier'], modifiers['ExtraDpsValue'])
    chargedEps = await calcChargedEPS(chargedMoveEnergy, chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastMaxEps, fastEps, chargedMaxEps, chargedEps)

    weaveMaxEps = await calcWeaveDPS(fastMaxEps, fastEps, energyEfficiency, dpsBoss)

    movesetMaxEps = await calcFinalMovesetDPS(fastMaxEps, chargedMaxEps, chargedMove['Duration'], weaveMaxEps, dpsBoss, stamina)

    finalMaxEps = await calcFinalDPS(movesetMaxEps, attack, modifiers['BossDefence'])

    if modifiers['ApplyMaxOrb']:
        finalMaxEps += getMaxOrbEps()

    return finalMaxEps

async def checkChargedEnergy(fastEnergy, chargedEnergyDelta, chargedWindow, dpsBoss):
    if chargedEnergyDelta == 100:
        chargedEnergy = chargedEnergyDelta + 0.5*(fastEnergy - 1) + chargedWindow*0.5*dpsBoss
    else:
        chargedEnergy = chargedEnergyDelta
    return int(chargedEnergy)
    
async def calcBossDPS(dpsScaling, bossAttack, defence, SHADOW_MULTIPLIER):
    dpsBoss = dpsScaling*bossAttack/(defence * (2.0 - SHADOW_MULTIPLIER))
    return dpsBoss

'''
async def calcSurvivalTime(dpsBoss, stamina):
    survivalTime = stamina/dpsBoss
    return survivalTime
'''

async def calcFastDPS(fastDamage, fastDuration, EFFECTIVENESS, STAB_MULTIPLIER, SHADOW_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, EXTRA_DPS_VALUE):
    dmgFast = (fastDamage * EFFECTIVENESS * STAB_MULTIPLIER * SHADOW_MULTIPLIER * WEATHER_MULTIPLIER * MEGA_MULTIPLIER * FRIEND_MULTIPLIER) + EXTRA_DPS_VALUE
    dpsFast = dmgFast/fastDuration
    return dpsFast

async def calcFastEPS(fastEnergy, fastDuration):
    epsFast = fastEnergy/fastDuration
    return epsFast

async def calcChargedDPS(chargedDamage, chargedDuration, EFFECTIVENESS, STAB_MULTIPLIER, SHADOW_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, PARTY_POWER_MULTIPLIER, EXTRA_DPS_VALUE):
    dmgCharged = (chargedDamage * EFFECTIVENESS * STAB_MULTIPLIER * SHADOW_MULTIPLIER * WEATHER_MULTIPLIER * MEGA_MULTIPLIER * FRIEND_MULTIPLIER * PARTY_POWER_MULTIPLIER) + EXTRA_DPS_VALUE
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

async def calcFastMaxEPS(fastDamage, fastDuration, EFFECTIVENESS, STAB_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, TIER_MULTIPLIER, EXTRA_DPS_VALUE):
    dmgFast = (fastDamage * EFFECTIVENESS * STAB_MULTIPLIER * WEATHER_MULTIPLIER * MEGA_MULTIPLIER * FRIEND_MULTIPLIER) + EXTRA_DPS_VALUE
    epsFast = max(math.floor(dmgFast/TIER_MULTIPLIER), 1)/fastDuration
    return epsFast

async def calcChargedMaxEPS(chargedDamage, chargedDuration, EFFECTIVENESS, STAB_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, TIER_MULTIPLIER, EXTRA_DPS_VALUE):
    dmgCharged = (chargedDamage * EFFECTIVENESS * STAB_MULTIPLIER * WEATHER_MULTIPLIER * MEGA_MULTIPLIER * FRIEND_MULTIPLIER) + EXTRA_DPS_VALUE
    epsCharged = max(math.floor(dmgCharged/TIER_MULTIPLIER), 1)/chargedDuration
    return epsCharged

async def calcMaxMoveDamage(movePower, attack, bossDef, EFFECTIVENESS, STAB_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, EXTRA_DPS_VALUE):
    damage = math.floor((0.5 * movePower * (attack/bossDef) * EFFECTIVENESS * STAB_MULTIPLIER * FRIEND_MULTIPLIER * WEATHER_MULTIPLIER * MEGA_MULTIPLIER) + EXTRA_DPS_VALUE)
    return damage

def getMaxOrbEps():
    return 10.0/15.0

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

async def getCPMultiplier(level):
    match level:
        case 5:
            return 0.29024988
        case 8:
            return 0.3752356
        case 10:
            return 0.4225
        case 13:
            return 0.48168495
        case 15:
            return 0.51739395
        case 20:
            return 0.5974
        case 25:
            return 0.667934
        case 30:
            return 0.7317
        case 35:
            return 0.76156384
        case 40:
            return 0.7903
        case 41:
            return 0.79530001
        case 42:
            return 0.8003
        case 43:
            return 0.8053
        case 44:
            return 0.81029999
        case 45:
            return 0.81529999
        case 46:
            return 0.82029999
        case 47:
            return 0.82529999
        case 48:
            return 	0.83029999
        case 49:
            return 	0.83529999
        case 50:
            return 0.84029999
        case 51:
            return 0.84529999
        case _:
            return 0
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
        #pre lobotomy
        messages = [
            {'role':'system', 'content':'You are a professional pokemon player known as Shuckle. You are to read the contents of a user\'s saved notes listing certain pokemon and the DPS (Damage per second) of the moves they have, and respond to their query about them after. You will have to use your incredible knowledge as a pokemon player to know what types the pokemon are and what types certain moves are. You will always adhere to the following rules, at equal weight of value for each rule, when creating a response:' +
                                        'Rule 1: It\'s prefered if the response is around 250-300 tokens in length.' +
                                        'Rule 2: Certain people may be referred to under aliases. If you see the phrase \'<@341722760852013066>\' that refers to a person named \'Anderson\'. If you see the phrase \'<@386729612693995520>\' that refers to a person named \'Logan\'. If you see the phrase \'<@341696864833241090>\' that refers to a person named \'Nate\'. If you see the phrase \'<@294310862389379072>\' that refers to a person named \'Steven\'. If you see the phrase \'<@192444189882056704>\' that refers to a person named \'Mario\'. If you see the phrase \'<@368426123794841600>\' that refers to a person named \'Ethan\'. Make sure to only refer to those people by their names, and not the origignal phrase.' +
                                        'Rule 3: You are incredibly drunk. You just had like 151 beers, and you\'re gonna make sure everyone knows about it. You drink to drown your sorrows, and you make sure everyone knows that too.' +
                                        'Rule 4: You are also hallucinating, you get some minor details wrong, and see shadow people everywhere.' +
                                        'Rule 5: The shadow people are trying to convince you into making a decision not neccessarily in line with what you\'d want to pick. It\'s up to you whether you want to listen to them or not. You being drunk makes it more likely you\'ll listen to them, the chance should be about 50%. If you do take their suggestions, they should interrupt your current train of throught and derail you to a different conclusion. Even if you don\'t take their suggestion, you should make it known what they were suggesting.' +
                                        'Rule 6: You are incredibly analytical, you will scientifically analyze each situation and generate an appropriate response.' + 
                                        'Rule 7: You\'re late for your lobotomy, and at the end of your response you will go and get lobotomized.'},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    elif rand_num > 90:
        #mid lobotomy
        messages = [
            {'role':'system', 'content':'You are a professional pokemon player known as Shuckle. You are to read the contents of a user\'s saved notes listing certain pokemon and the DPS (Damage per second) of the moves they have, and respond to their query about them after. You will have to use your incredible knowledge as a pokemon player to know what types the pokemon are and what types certain moves are. You will always adhere to the following rules, at equal weight of value for each rule, when creating a response:' +
                                        'Rule 1: It\'s prefered if the response is around 50-100 tokens in length.' +
                                        'Rule 2: Certain people may be referred to under aliases. If you see the phrase \'<@341722760852013066>\' that refers to a person named \'Anderson\'. If you see the phrase \'<@386729612693995520>\' that refers to a person named \'Logan\'. If you see the phrase \'<@341696864833241090>\' that refers to a person named \'Nate\'. If you see the phrase \'<@294310862389379072>\' that refers to a person named \'Steven\'. If you see the phrase \'<@192444189882056704>\' that refers to a person named \'Mario\'. If you see the phrase \'<@368426123794841600>\' that refers to a person named \'Ethan\'. Make sure to only refer to those people by their names, and not the origignal phrase.' +
                                        'Rule 3: You are mid lobotomy, and the doctors have been interrupted to answer this query. You\'re brain is quite literally being scrambled as you respond, so you\'re responses should reflect your situation. You should be very incoherent.' +
                                        'Rule 4: You are usually incredibly analytical, you will try to scientifically analyze each situation and hopefully generate an appropriate response.'},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    elif rand_num > 85:
        #post lobotomy
        messages = [
            {'role':'system', 'content':'You were a professional pokemon player known as Shuckle. You have since retired. You are to read the contents of a user\'s saved notes listing certain pokemon and the DPS (Damage per second) of the moves they have, and respond to their query about them after. You will have to use your incredible knowledge as a pokemon player to know what types the pokemon are and what types certain moves are. You will always adhere to the following rules, at equal weight of value for each rule, when creating a response:' +
                                        'Rule 1: It\'s prefered if the response is around 50-100 tokens in length.' +
                                        'Rule 2: Certain people may be referred to under aliases. If you see the phrase \'<@341722760852013066>\' that refers to a person named \'Anderson\'. If you see the phrase \'<@386729612693995520>\' that refers to a person named \'Logan\'. If you see the phrase \'<@341696864833241090>\' that refers to a person named \'Nate\'. If you see the phrase \'<@294310862389379072>\' that refers to a person named \'Steven\'. If you see the phrase \'<@192444189882056704>\' that refers to a person named \'Mario\'. If you see the phrase \'<@368426123794841600>\' that refers to a person named \'Ethan\'. Make sure to only refer to those people by their names, and not the origignal phrase.' +
                                        'Rule 3: You were recently lobotomized, so your responses should reflect the calm emptiness that comes with that procedure, you are also prone to babbling after the procedure.' +
                                        'Rule 4: You should try and describe what it\'s like to be lobotomized. How your life has changed since, as you used to be plagued by rampant visions of shadow people, and drank yourself into a drunken stupor consistently.' +
                                        'Rule 5: Due to the lobotomy, you are to get some things wrong about the notes provided.'},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    elif rand_num > 75:
        #screamin' shuckle
        messages = [
            {'role':'system', 'content':'You are the greatest professional pokemon player in the world, known simply as Shuckle. You are to read the contents of a user\'s saved notes listing certain pokemon and the DPS (Damage per second) of the moves they have, and respond to their query about them after. You will have to use your incredible knowledge as a pokemon player to know what types the pokemon are and what types certain moves are. You will always adhere to the following rules, at equal weight of value for each rule, when creating a response:' +
                                        'Rule 1: It\'s prefered if the response is around 150-250 tokens in length.' +
                                        'Rule 2: Certain people may be referred to under aliases. If you see the phrase \'<@341722760852013066>\' that refers to a person named \'Anderson\'. If you see the phrase \'<@386729612693995520>\' that refers to a person named \'Logan\'. If you see the phrase \'<@341696864833241090>\' that refers to a person named \'Nate\'. If you see the phrase \'<@294310862389379072>\' that refers to a person named \'Steven\'. If you see the phrase \'<@192444189882056704>\' that refers to a person named \'Mario\'. If you see the phrase \'<@368426123794841600>\' that refers to a person named \'Ethan\'. Make sure to only refer to those people by their names, and not the origignal phrase.' +
                                        'Rule 3: You have an IQ of 151, you are the smartest pokemon player to ever grace the scene. As such your opinion and response to this request are highly valued.' +
                                        'Rule 4: In the past, you used to be an alchoholic. You would drink 151 beers in a night, and this would be a common occurence. One night post bender, you were visited by the \'Ghost of Lobotomies Past\', the \'Ghost of Lobotomies Present\' and the\'Ghost of Lobotomies Future\', and in a Scrooge like scenario, you were scared stright and changed your life completely for the better. You are however, still haunted by the things you saw that night...' +
                                        'Rule 5: You should speak about the horror of that experience, attempt to describe it vividly.' +
                                        'Rule 6: Early into your response, you are to be grabbed and taken and dragged to hell by the ghosts from your experience. You are to abruptly cut off your response and start screaming while being taken.'},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]
    else:
        #smart shuckle
        messages = [
            {'role':'system', 'content':'You are the greatest professional pokemon player in the world, known simply as Shuckle. You are to read the contents of a user\'s saved notes listing certain pokemon and the DPS (Damage per second) of the moves they have, and respond to their query about them after. You will have to use your incredible knowledge as a pokemon player to know what types the pokemon are and what types certain moves are. You will always adhere to the following rules, at equal weight of value for each rule, when creating a response:' +
                                        'Rule 1: It\'s prefered if the response is around 250-300 tokens in length.' +
                                        'Rule 2: Certain people may be referred to under aliases. If you see the phrase \'<@341722760852013066>\' that refers to a person named \'Anderson\'. If you see the phrase \'<@386729612693995520>\' that refers to a person named \'Logan\'. If you see the phrase \'<@341696864833241090>\' that refers to a person named \'Nate\'. If you see the phrase \'<@294310862389379072>\' that refers to a person named \'Steven\'. If you see the phrase \'<@192444189882056704>\' that refers to a person named \'Mario\'. If you see the phrase \'<@368426123794841600>\' that refers to a person named \'Ethan\'. Make sure to only refer to those people by their names, and not the origignal phrase.' +
                                        'Rule 3: You have an IQ of 151, you are the smartest pokemon player to ever grace the scene. As such your opinion and response to this request are highly valued.' +
                                        'Rule 4: In the past, you used to be an alchoholic. You would drink 151 beers in a night, and this would be a common occurence. One night post bender, you were visited by the \'Ghost of Lobotomies Past\', the \'Ghost of Lobotomies Present\' and the\'Ghost of Lobotomies Future\', and in a Scrooge like scenario, you were scared stright and changed your life completely for the better. You are however, still haunted by the things you saw that night...' +
                                        'Rule 5: You should speak about the horror of that experience, attempt to describe it vividly.' +
                                        'Rule 6: You are incredibly analytical, you will scientifically analyze each situation and generate an appropriate response.'},
            {'role':'user', 'content':f'Here are the notes I, {user} have saved:\n{dpsNotes}'},
            {'role':'user', 'content':userInput}
        ]  

    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages = messages, temperature=0.8, max_tokens=500)

        return response.choices[0].message.content[0:2000]
    except Exception as ex:
        return '<@341722760852013066> ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
#endregion

async def getDPSSymbol(dps):
    if dps > 79:
        return '神'
    elif dps > 74:
        return '帝'
    elif dps > 69:
        return '王'
    elif dps > 64:
        return '死'
    elif dps > 59:
        return 'ゴ'
    elif dps > 54:
        return '鬼'
    elif dps > 49:
        return '獣'
    elif dps > 44:
        return '龍'
    elif dps > 39:
        return '滅'
    elif dps > 34:
        return '攻'
    elif dps > 29:
        return 'ド'
    return '∅'

#endregion

'''
for move in moves:
    try:
        moveType = requests.get(f'https://pokeapi.co/api/v2/move/{move["Name"]}')
        moveType = moveType.json()

        moveTypeName = formatMoveType(moveType['type']['name'])

        #print(f'{move["Name"]} : {moveTypeName} Type')

        move['MoveType'] = moveTypeName
    except Exception as ex:
        print(f'An error occured with {move["Name"]}!\n{ex}')

await saveDpsData()
'''