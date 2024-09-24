""" 
Contains the functions relating to PoGO dps. 
Usually returns data in a discord embed

Cole Anderson, Sept 2024
"""

import discord
import json
import random
import requests
import regex as re
import math
import copy
from soul_link_dictionaries import types

with open('text_files/dps/moves.txt', 'r') as file:
    moves = json.loads(file.read())

with open('text_files/dps/pokemon.txt', 'r') as file:
    loadedMons = json.loads(file.read())

with open('text_files/soul_link_pokemon.txt', 'r') as file:
    pokemon = json.loads(file.read())

async def dpsHelp():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

    embed = discord.Embed(title=f'Shuckles PoGo DPS Commands',
                            description='```$dps check Kartana``` Calcs the dps for the moveset for the mon at level 50\n' +
                                        '```$dps check Kartana, 50, Shadow, NoFastSTAB, NoChargeSTAB``` Calcs the dps for the moveset based on the provided modifiers. Any order is allowed.\n' +
                                        '```$dps add-move Razor Leaf, 13, 7, 1000``` For fast moves, list their damage, energy, and duration in milliseconds.\n' +
                                        '```$dps add-move Leaf Blade, 70, 33, 2400, 1250``` For charged moves, list their damage, energy cost, duration, and damage window start, with the times in milliseconds.\n' +
                                        '```$dps add-mon Kartana, 323, 182, 139``` Registers a mons base stats in Atk/Def/HP order.\n' +
                                        '```$dps add-moveset Kartana, Razor Leaf, Leaf Blade, etc...``` Adds every move listed to a registered mon\n' +
                                        '```$dps remove-moveset Kartana, Razor Leaf, Leaf Blade, etc...``` Removes every move listed from a registered mon, as long as they\'re registered to it.\n' +
                                        '```$dps list-mons``` Lists all the registered mons.\n' +
                                        '```$dps list-moves``` Lists all the registered moves.\n' +
                                        '```$dps delete-mon Kartana``` Deletes a mon from the registered list.\n' +
                                        '```$dps delete-move Razor Leaf``` Deletes a move from the registered list.\n\n' +
                                        'Everything should be case insensitive.\nAlways assume stats are listed in Attack/Defence/HP order, and that all calcs are done based on hundo ivs.\nhttps://db.pokemongohub.net is good for checking move data.', 
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
#endregion

#region dps commands
async def saveDpsData():
    global moves
    global loadedMons

    with open('text_files/dps/moves.txt', 'w') as file:
        file.write(json.dumps(moves))

    with open('text_files/dps/moves.txt', 'r') as file:
        moves = json.loads(file.read())

    with open('text_files/dps/pokemon.txt', 'w') as file:
        file.write(json.dumps(loadedMons))

    with open('text_files/dps/pokemon.txt', 'r') as file:
        loadedMons = json.loads(file.read())

async def dpsAddMon(monName, attack, defence, stamina):
    if checkDuplicateMon(monName):
        return 'That pokemon is already registered!'
    
    if (1000 < attack <= 0) or (1000 < defence <= 0) or (1000 < stamina <= 0):
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
    
    if (1000 < damage <= 0) or (100 < energy <= 0) or (10000 < duration <= 0):
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
    
    if (1000 < damage <= 0) or (100 < energyDelta <= 0) or (10000 < duration <= 0):
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
    BOSS_ATTACK = 200
    BOSS_DEFENCE = 70
    EXTRA_DPS_VALUE = 0.5

    level = 50
    fastSTABMultiplier = 1.2
    chargedSTABMultipler = 1.2

    shadowMultiplier = 1.0
    shadowText = ''

    if extraInputs != None:
        level, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, shadowText, errorText = await determineExtraInputs(extraInputs)
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
    calculated_attack = (mon['Attack'] + 15)*cpMultiplier
    calculated_defence = (mon['Defence'] + 15)*cpMultiplier
    calculated_stamina = (mon['Stamina'] + 15)*cpMultiplier

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
    moveDPSOutput = ''
    #movePwrIncrease = ''

    embed = discord.Embed(title=f'DPS Calculations for {shadowText}{formatForDisplay(mon["Name"])} at Lv {level}',
                          description=f'Attack: {mon["Attack"]}\nDefence: {mon["Defence"]}\nStamina: {mon["Stamina"]}\n\nFast Moves: {fastMovesText[:-2]}\nCharged Moves: {chargedMovesText[:-2]}',
                          color=embedColour)

    for fastMove in fastMoves:
        for chargedMove in chargedMoves:
            oldDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, fastMove, chargedMove, ENEMY_DPS_SCALING, BOSS_ATTACK, BOSS_DEFENCE, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, EXTRA_DPS_VALUE)

            newFastMove = await calcRoundedFastMoves(fastMove)
            newChargedMove = await calcRoundedChargedMoves(chargedMove)
            newDPS = await calcOverallDPS(calculated_attack, calculated_defence, calculated_stamina, newFastMove, newChargedMove, ENEMY_DPS_SCALING, BOSS_ATTACK, BOSS_DEFENCE, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, EXTRA_DPS_VALUE)

            moveNameOutput += f'{formatForDisplay(fastMove["Name"])}{displayDurationChange(fastMove["Duration"], newFastMove["Duration"])} | {formatForDisplay(chargedMove["Name"])}{displayDurationChange(chargedMove["Duration"], newChargedMove["Duration"])}\n'
            moveDPSOutput += f'{roundDPS(oldDPS)} -> {roundDPS(newDPS)}\n'
            #movePwrIncrease += f'{calcDPSDifference(oldDPS, newDPS)}%\n'

    embed.add_field(name='Moveset',
                    value=moveNameOutput,
                    inline=True)
    
    embed.add_field(name='Old -> New',
                    value=moveDPSOutput,
                    inline=True)
    
    '''
    embed.add_field(name='% Diff',
                    value=movePwrIncrease,
                    inline=True)
    '''

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{mon["ImageDexNum"]}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{mon["ImageDexNum"]}.png')


    return embed

async def determineExtraInputs(extraInputs):
    level = 50
    fastSTABMultiplier = 1.2
    chargedSTABMultipler = 1.2

    shadowMultiplier = 1.0
    shadowText = ''

    errorText = ''

    for input in extraInputs:
        if input.strip().isdigit():
            level = int(input)
        elif str(input).strip().lower() == 'shadow':
            shadowMultiplier = 1.2
            shadowText = 'Shadow '
        elif str(input).strip().lower() == 'nofaststab':
            fastSTABMultiplier = 1.0
        elif str(input).strip().lower() == 'nochargestab':
            chargedSTABMultipler = 1.0
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if errorText != '':
        errorText += '\nCheck `$dps help` to see all valid modifiers!'
    
    return level, fastSTABMultiplier, chargedSTABMultipler, shadowMultiplier, shadowText, errorText

async def calcOverallDPS(attack, defence, stamina, fastMove, chargedMove, ENEMY_DPS_SCALING, BOSS_ATTACK, BOSS_DEFENCE, FAST_STAB_MULTIPLIER, CHARGED_STAB_MULTIPLIER, SHADOW_MULTIPLIER, EXTRA_DPS_VALUE):
    dpsBoss = await calcBossDPS(ENEMY_DPS_SCALING, BOSS_ATTACK, defence, SHADOW_MULTIPLIER)

    fastDps = await calcFastDPS(fastMove['Damage'], fastMove['Duration'], FAST_STAB_MULTIPLIER, SHADOW_MULTIPLIER, EXTRA_DPS_VALUE)
    fastEps = await calcFastEPS(fastMove['Energy'], fastMove['Duration'])

    chargedMove['Energy'] = await checkChargedEnergy(fastMove['Energy'], chargedMove['Energy'], chargedMove['DamageWindow'], dpsBoss)
    chargedDps = await calcChargedDPS(chargedMove['Damage'], chargedMove['Duration'], CHARGED_STAB_MULTIPLIER, SHADOW_MULTIPLIER, EXTRA_DPS_VALUE)
    chargedEps = await calcChargedEPS(chargedMove['Energy'], chargedMove['Duration'])

    energyEfficiency = await calcEnergyEfficiency(fastDps, fastEps, chargedDps, chargedEps)

    weaveDps = await calcWeaveDPS(fastDps, fastEps, energyEfficiency, dpsBoss)

    movesetDps = await calcFinalMovesetDPS(fastDps, chargedDps, chargedMove['Duration'], weaveDps, dpsBoss, stamina)

    finalDps = await calcFinalDPS(movesetDps, attack, BOSS_DEFENCE)

    return finalDps
    
async def checkChargedEnergy(fastEnergy, chargedEnergyDelta, chargedWindow, dpsBoss):
    chargedEnergyDeltaCopy = copy.deepcopy(chargedEnergyDelta)
    if chargedEnergyDeltaCopy == 100:
        chargedEnergy = chargedEnergyDeltaCopy + 0.5*(fastEnergy - 1) + chargedWindow*0.5*dpsBoss
    else:
        chargedEnergy = chargedEnergyDeltaCopy
    return int(chargedEnergy)
    
async def calcBossDPS(dpsScaling, bossAttack, defence, SHADOW_MULTIPLIER):
    dpsBoss = dpsScaling*bossAttack/(defence * (2.0 - SHADOW_MULTIPLIER))
    return dpsBoss

'''
async def calcSurvivalTime(dpsBoss, stamina):
    survivalTime = stamina/dpsBoss
    return survivalTime
'''

async def calcFastDPS(fastDamage, fastDuration, STAB_MULTIPLIER, SHADOW_MULTIPLIER, EXTRA_DPS_VALUE):
    dmgFast = (fastDamage * STAB_MULTIPLIER * SHADOW_MULTIPLIER) + EXTRA_DPS_VALUE
    dpsFast = dmgFast/fastDuration
    return dpsFast

async def calcFastEPS(fastEnergy, fastDuration):
    epsFast = fastEnergy/fastDuration
    return epsFast

async def calcChargedDPS(chargedDamage, chargedDuration, STAB_MULTIPLIER, SHADOW_MULTIPLIER, EXTRA_DPS_VALUE):
    dmgCharged = (chargedDamage * STAB_MULTIPLIER * SHADOW_MULTIPLIER) + EXTRA_DPS_VALUE
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