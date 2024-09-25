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

with open('text_files/dps/pokemon.txt', 'r') as file:
    loadedMons = json.loads(file.read())

with open('text_files/soul_link_pokemon.txt', 'r') as file:
    pokemon = json.loads(file.read())

with open('text_files/dps/notes.txt', 'r') as file:
    dpsNotes = file.read()

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

#region chatgpt notes
async def addDPSNote(note):
    global dpsNotes

    dpsNotes += f'{note}\n'

    await saveDpsData()

    return 'Note added successfully!'

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
        print(ex)
        return '<@341722760852013066> ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
#endregion
#endregion