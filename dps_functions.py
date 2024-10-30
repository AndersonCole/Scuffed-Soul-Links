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
                                        '```$dps add-move Razor Leaf, 13, 7, 1000``` For fast moves, list their damage, energy, and duration in milliseconds.\n' +
                                        '```$dps add-move Leaf Blade, 70, 33, 2400, 1250``` For charged moves, list their damage, energy cost, duration, and damage window start, with the times in milliseconds.\n' +
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
                                        '```$dps check Kartana, 14/15/15``` IVs: Calcs DPS from the given IVs. Always assume stats are listed in Attack/Defence/HP order.\n' +
                                        '```$dps check Kartana, Shadow``` Shadow: Gives the mon a 1.2x atk boost and def nerf\n' +
                                        '```$dps check Kartana, NoFastSTAB``` NoFastSTAB: Removes STAB from the mons fast attack\n' +
                                        '```$dps check Kartana, NoChargedSTAB``` NoChargedSTAB: Removes STAB from the mons charged attack\n' +
                                        '```$dps check Kartana, FastEffective1.6x``` FastEffectiveness: Applies type effectivity damage bonuses to fast moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$dps check Kartana, ChargedEffective1.6x``` ChargedEffectiveness: Applies type effectivity damage bonuses to charged moves\n4x Weakness = 2.56x dmg | 2x Weakness = 1.6x dmg.\n 0.5x Resistance = 0.625x dmg | 0x Immunity = 0.39x dmg\n' +
                                        '```$dps check Kartana, FriendBoost``` FriendBoost: Adds a 1.1x boost to both fast and charged attacks\n' +
                                        '```$dps check Kartana, WeatherBoost``` WeatherBoost: Adds a 1.2x boost to both fast and charged attacks\n' +
                                        '```$dps check Kartana, MegaBoost``` MegaBoost: Adds a 1.3x boost to both fast and charged attacks\n' +
                                        '```$dps check Kartana, PartyPower1``` PartyPower: Applies the party power boost at the specified rate\n1 = Every charged move, 2 = Every other, 3 = Every third, etc' +
                                        '```$dps check Kartana, BossAtk200``` BossAtk: Sets the enemy boss attack to the specified value. The default is 200\n' +
                                        '```$dps check Kartana, BossDef70``` BossDef: Sets the enemy boss defence to the specified value. The default is 70\n' +
                                        '```$dps check Kartana, SortByOldDps``` SortByOldDps: Orders the output by the old dps\n' +
                                        '```$dps check Kartana, SortByFastMoves``` SortByFast: Orders the output by fast moves\n' +
                                        '```$dps check Kartana, SortByChargedMoves``` SortByCharged: Orders the output by charged moves\n' +
                                        '```$dps check Kartana, NoMoveChanges``` NoMoveChanges: Ignores the changes made to move base stats in October 2024\n\n' +
                                        'Everything should be case insensitive.\nDefault check assumes Lv50, Hundo, Not Shadow, STAB for everything, Neutral effectiveness, No Special Boosts, Sorted by Dps', 
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

async def dpsAddFastMove(moveName, damage, energy, duration):
    if checkDuplicateMove(moveName):
        return 'That move is already registered!'
    
    if (1000 < damage or damage <= 0) or (100 < energy or energy <= 0) or (10000 < duration or duration <= 0):
        return 'Make sure the damage is between 1 and 1000, the energy between 1 and 100, and the duration between 1 and 10,000 ms!'

    moveName = formatName(moveName)

    duration = duration/1000

    moves.append({
        'Name': moveName,
        'Type': 'Fast',
        'Damage': damage,
        'Energy': energy,
        'Duration': duration
    })

    await saveDpsData()

    return 'Fast move added successfully!'

async def dpsAddChargedMove(moveName, damage, energyDelta, duration, damageWindow):
    if checkDuplicateMove(moveName):
        return 'That move is already registered!'
    
    if (1000 < damage or damage <= 0) or (100 < energyDelta or energyDelta <= 0) or (10000 < duration or duration <= 0):
        return 'Make sure the damage is between 1 and 1000, the energy cost between 1 and 100, and the duration between 1 and 10,000 ms!'

    if  0 >= damageWindow > duration:
        return 'Make sure the damage window starts before the move ends, or is at least 1!'
    
    moveName = formatName(moveName)

    duration = duration/1000
    damageWindow = damageWindow/1000

    moves.append({
        'Name': moveName,
        'Type': 'Charged',
        'Damage': damage,
        'Energy': energyDelta,
        'Duration': duration,
        'DamageWindow': damageWindow
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
async def dpsCheck(monName, extraInputs=None):
    ENEMY_DPS_SCALING = 4.0
    EXTRA_DPS_VALUE = 0.5

    bossAttack = 200
    bossDefence = 70

    level = 50
    attack_iv = 15
    defence_iv = 15
    stamina_iv = 15

    fastEffectiveness = 1.0
    chargedEffectiveness = 1.0

    fastSTABMultiplier = 1.2
    chargedSTABMultipler = 1.2

    shadowMultiplier = 1.0
    shadowText = ''
    
    weatherMultiplier = 1.0
    megaMultiplier = 1.0
    friendMultiplier = 1.0
    partyPowerMultiplier = 1.0

    applyMoveChanges = True

    resultSortOrder = 'ByNewDps'

    if extraInputs != None:
        level, attack_iv, defence_iv, stamina_iv, fastEffectiveness, chargedEffectiveness, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, shadowText, friendMultiplier, weatherMultiplier, megaMultiplier, partyPowerMultiplier, bossAttack, bossDefence, resultSortOrder, applyMoveChanges, errorText = await determineExtraInputs(extraInputs)
        if errorText != '':
            return errorText
    
    if not checkDuplicateMon(monName):
        return 'That pokemon is not registered!'
    
    mon = [obj for obj in loadedMons if obj['Name'] == formatName(monName)][0]
    if mon['ImageDexNum'] >= 0:
        mon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{mon["ImageDexNum"]}')
        mon_data = mon_data.json()
        mon_primary_type = str(mon_data['types'][0]['type']['name']).capitalize()
        embedColour = [obj for obj in types if obj['Name'] == mon_primary_type][0]['Colour']
    else:
        embedColour = 3553598

    cpMultiplier = await getCPMultiplier(level)
    if cpMultiplier == 0:
        return 'Level must be between 40-51, or a multiple of 5!'
    calculated_attack = (mon['Attack'] + attack_iv)*cpMultiplier
    calculated_defence = (mon['Defence'] + defence_iv)*cpMultiplier
    calculated_stamina = (mon['Stamina'] + stamina_iv)*cpMultiplier

    fastMoves = []
    chargedMoves= []
    fastMovesText = ''
    chargedMovesText = ''

    for move in mon['Moves']:
        changedIndicator = ''
        if applyMoveChanges:
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

    embed = discord.Embed(title=f'DPS Calculations for {shadowText}{formatForDisplay(mon["Name"])} at Lv {level}',
                          description=f'Attack: {mon["Attack"]}\nDefence: {mon["Defence"]}\nStamina: {mon["Stamina"]}\nIVs: {attack_iv}/{defence_iv}/{stamina_iv}\n\nFast Moves: {fastMovesText[:-2]}\nCharged Moves: {chargedMovesText[:-2]}',
                          color=embedColour)

    for fastMove in fastMoves:
        copiedFastMove = copy.deepcopy(fastMove)
        copiedFastMove['Damage'], copiedFastMove['Energy'] = getChangedMoveStats(copiedFastMove['Name'], copiedFastMove['Damage'], copiedFastMove['Energy'], applyMoveChanges)
        for chargedMove in chargedMoves:
            copiedChargedMove = copy.deepcopy(chargedMove)
            copiedChargedMove['Damage'], copiedChargedMove['Energy'] = getChangedMoveStats(copiedChargedMove['Name'], copiedChargedMove['Damage'], copiedChargedMove['Energy'], applyMoveChanges)

            oldDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, fastMove, chargedMove, ENEMY_DPS_SCALING, bossAttack, bossDefence, fastEffectiveness, chargedEffectiveness, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, friendMultiplier, weatherMultiplier, megaMultiplier, partyPowerMultiplier, EXTRA_DPS_VALUE)

            newFastMove = await calcRoundedFastMoves(copiedFastMove)
            newChargedMove = await calcRoundedChargedMoves(copiedChargedMove)
            newDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, newFastMove, newChargedMove, ENEMY_DPS_SCALING, bossAttack, bossDefence, fastEffectiveness, chargedEffectiveness, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, friendMultiplier, weatherMultiplier, megaMultiplier, partyPowerMultiplier, EXTRA_DPS_VALUE)

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

    if resultSortOrder == 'ByNewDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['NewDPS'], reverse=True)
    elif resultSortOrder == 'ByOldDps':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['OldDPS'], reverse=True)
    elif resultSortOrder == 'ByFast':
        sortedDpsResults = sorted(dpsResults, key=lambda x: x['FastName'])
    elif resultSortOrder == 'ByCharged':
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

#region modifiers
async def determineExtraInputs(extraInputs):
    bossAttack = 200
    bossDefence = 70

    level = 50
    attack_iv = 15
    defence_iv = 15
    stamina_iv = 15

    fastEffectiveness = 1.0
    chargedEffectiveness = 1.0

    fastSTABMultiplier = 1.2
    chargedSTABMultipler = 1.2

    shadowMultiplier = 1.0
    shadowText = ''
    
    weatherMultiplier = 1.0
    megaMultiplier = 1.0
    friendMultiplier = 1.0
    partyPowerMultiplier = 1.0

    applyMoveChanges = True

    resultSortOrder = 'ByNewDps'

    errorText = ''

    for input in extraInputs:
        if input.strip().isdigit():
            level = int(input)
        elif '/' in str(input).strip():
            ivs = re.split(r'[/]+', input.strip())
            try:
                for iv in ivs:
                    if 0 > int(iv) or int(iv) > 15:
                        raise Exception
                attack_iv = int(ivs[0])
                defence_iv = int(ivs[1])
                stamina_iv = int(ivs[2])
            except Exception as ex:
                errorText += f'\'{input}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!'
        elif str(input).strip().lower() == 'shadow':
            shadowMultiplier = 1.2
            shadowText = 'Shadow '
        elif str(input).strip().lower()[:13] == 'fasteffective':
            try :
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[13:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                fastEffectiveness = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid fast effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!'
        elif str(input).strip().lower()[:16] == 'chargedeffective':
            try :
                if input.strip()[-1:] != 'x':
                    raise Exception
                val = float(input.strip()[16:-1])
                if 0.1 > val or val > 4.0:
                    raise Exception
                chargedEffectiveness = val
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid charged effectiveness value! Keep it between 0.1 and 4! And don\'t forget the x at the end!'
        elif str(input).strip().lower() == 'nofaststab':
            fastSTABMultiplier = 1.0
        elif str(input).strip().lower() == 'nofaststab':
            fastSTABMultiplier = 1.0
        elif str(input).strip().lower() == 'nochargedstab':
            chargedSTABMultipler = 1.0
        elif str(input).strip().lower() == 'friendboost':
            friendMultiplier = 1.1
        elif str(input).strip().lower() == 'weatherboost':
            weatherMultiplier = 1.2
        elif str(input).strip().lower() == 'megaboost':
            megaMultiplier = 1.3
        elif str(input).strip().lower()[:10] == 'partypower':
            try:
                multiplier = int(input.strip()[10:])
                if multiplier < 1 or multiplier > 5:
                    raise Exception
                partyPowerMultiplier = 1.0 + (1.0/float(multiplier))
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid party power value! Keep it between 1 and 5!'
        elif str(input).strip().lower()[:7] == 'bossatk':
            try :
                atkVal = int(input.strip()[7:])
                if 1 > atkVal or atkVal > 1000:
                    raise Exception
                bossAttack = atkVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss attack value! Keep it between 1 and 1000!'
        elif str(input).strip().lower()[:7] == 'bossdef':
            try :
                defVal = int(input.strip()[7:])
                if 1 > defVal or defVal > 1000:
                    raise Exception
                bossDefence = defVal
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid boss defence value! Keep it between 1 and 1000!'
        elif str(input).strip().lower()[:12] == 'sortbyolddps':
            resultSortOrder = 'ByOldDps'
        elif str(input).strip().lower()[:15] == 'sortbyfastmoves':
            resultSortOrder = 'ByFast'
        elif str(input).strip().lower()[:18] == 'sortbychargedmoves':
            resultSortOrder = 'ByCharged'
        elif str(input).strip().lower()[:13] == 'nomovechanges':
            applyMoveChanges = False
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if errorText != '':
        errorText += '\n\nCheck `$dps modifiers` to see all valid modifiers!'
    
    return level, attack_iv, defence_iv, stamina_iv, fastEffectiveness, chargedEffectiveness, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, shadowText, friendMultiplier, weatherMultiplier, megaMultiplier, partyPowerMultiplier, bossAttack, bossDefence, resultSortOrder, applyMoveChanges, errorText
#endregion

#region math calculations
async def calcOverallDPS(attack, defence, stamina, fastMove, chargedMove, ENEMY_DPS_SCALING, BOSS_ATTACK, BOSS_DEFENCE, FAST_EFFECTIVENESS, CHARGED_EFFECTIVENESS, FAST_STAB_MULTIPLIER, CHARGED_STAB_MULTIPLIER, SHADOW_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, PARTY_POWER_MULTIPLIER, EXTRA_DPS_VALUE):
    dpsBoss = await calcBossDPS(ENEMY_DPS_SCALING, BOSS_ATTACK, defence, SHADOW_MULTIPLIER)

    fastDps = await calcFastDPS(fastMove['Damage'], fastMove['Duration'], FAST_EFFECTIVENESS, FAST_STAB_MULTIPLIER, SHADOW_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, EXTRA_DPS_VALUE)
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMoveEnergy = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss)
    chargedDps = await calcChargedDPS(chargedMove['Damage'], chargedMove['Duration'], CHARGED_EFFECTIVENESS, CHARGED_STAB_MULTIPLIER, SHADOW_MULTIPLIER, FRIEND_MULTIPLIER, WEATHER_MULTIPLIER, MEGA_MULTIPLIER, PARTY_POWER_MULTIPLIER, EXTRA_DPS_VALUE)
    chargedEps = await calcChargedEPS(chargedMoveEnergy, chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastDps, fastEps, chargedDps, chargedEps)

    weaveDps = await calcWeaveDPS(fastDps, fastEps, energyEfficiency, dpsBoss)

    movesetDps = await calcFinalMovesetDPS(fastDps, chargedDps, chargedMove['Duration'], weaveDps, dpsBoss, stamina)

    finalDps = await calcFinalDPS(movesetDps, attack, BOSS_DEFENCE)

    return finalDps
    
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

'''
def calcDPSDifference(oldDPS, newDPS):
    dpsDiff = ((newDPS/oldDPS)*100)-100
    return round(dpsDiff, 2)
'''

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