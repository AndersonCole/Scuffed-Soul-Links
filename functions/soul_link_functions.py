import discord
import openai
import random
import regex as re
import math
import copy
import asyncio
import aiohttp
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from functions.shared_functions import (loadDataVariableFromFile, saveDataVariableToFile, 
                                        getPokeApiJsonData, getPokeAPISpriteUrl, openHttpImage,
                                        getDexNum, formatTextForDisplay, getMon, getMonName,
                                        getTypeEmoji, getTypeColour, addPaginatedEmbedFields,
                                        loadShucklePersonality, rollForShiny, pokemon)
from dictionaries.shared_dictionaries import sharedFileLocations, sharedImagePaths, sharedEmbedColours, types, categories
from dictionaries.soul_link_dictionaries import soulLinksFileLocations, defaultRun, gens, games

openai.api_key = loadDataVariableFromFile(sharedFileLocations.get('ChatGPT'), False)

runs = loadDataVariableFromFile(soulLinksFileLocations.get('Runs'))

currentRun = copy.deepcopy(defaultRun)

#region help command
#dev commands, undo-death {name}, reset, undo-status
async def help():
    embed = discord.Embed(title=f'Scuffed Soul Link Bot Commands',
                          description='```$sl new-sl HeartGold, HGAttempt1, @Player1, @Player2...``` Creates a new soul link run linked to the users specified\n' +
                                      '```$sl encounter Starter, Bulbasaur``` Adds data to an encounter, the other users in the sl can call the command again to set their encountered mon\n' +
                                      '```$sl encounter Starter, @Player1 Bulbasaur, @Player2 Charmander``` Another option for adding data to an encounter, you can specify encounters for as many players as needed\n' +
                                      '```$sl links``` Lists out the active links for the current run\n' +
                                      '```$sl link-data Bulbasaur``` Gives you information about the link for the specified mon you own\n' +
                                      '```$sl link-data Starter``` Gives you information about the link for the area it was encountered\n' +
                                      '```$sl evolve Bulbasaur``` Evolves a pokemon you own\n' +
                                      '```$sl death Starter, Metronome explosion :(``` Removes the link from the active links\n' +
                                      '```$sl deaths``` Lists out all the dead links, and cause of death\n' +
                                      '```$sl ask-shuckle It was Nate\'s fault the starters died``` Explain the situation, and an excuse for the cause of death will be generated\n' +
                                      '```$sl encounters``` Lists out all the areas where mons can be encountered\n' +
                                      '```$sl choose-team Bulbasaur, Groudon, Kyogre...``` Selects a team for the next important battle. Matches mons to links. Not required\n' +
                                      '```$sl random``` @\'s a random player participating in the run\n' +
                                      '```$sl next-battle``` Lists out the next important battle and its level cap\n' +
                                      '```$sl progress``` Moves the runs progress past the next important battle\n' +
                                      '```$sl add-note REM sleep is trendy!``` Adds a note to the run, highlighting funny events or whatnot\n' +
                                      '```$sl select-run HGAttempt1``` Selects a run to focus on\n' +
                                      '```$sl runs``` Lists out all runs\n' +
                                      '```$sl win-run``` Ends the run in victory\n' +
                                      '```$sl fail-run``` Ends the run in failure\n' +
                                      '```$sl run-info``` Prints out all relevant stats for the currently selected run\n\n' +
                                      '```$sl dex Bulbasaur``` Shows data on selected pokemon\n' +
                                      '```$sl dex Bulbasaur, HeartGold``` Shows data on selected pokemon in HearGold\n' +
                                      '```$sl moves Bulbasaur 24``` Shows the four moves the mon has at a specific level\n' +
                                      '```$sl catch Bulbasaur 5``` Caclulates the catch rate for the selected gen given the pokemon and level\n' +
                                      '```$sl rare-candies``` Shuckle explains how to aquire rare candies using PKHex\n\n' +
                                      'For Data on forms, type the pokemon\'s name like giratina origin, vulpix alola, charizard mega y, appletun gmax\n' +
                                      'Accessing data for a pokemon\'s default form will always work with their base name',
                          color=sharedEmbedColours.get('Default'))
    
    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    return embed
#endregion

#region text parsing functions
def getGroup(game):
    try:
        return [obj for obj in games if any(group.lower() == game.lower() for group in obj['Games'])][0]['Name']
    except:
        return None

def checkDuplicateName(name):
    temp = [obj for obj in runs if obj['Name'] == name]
    if len(temp) >= 1:
        return True
    return False

def formatVersionGroupName(versionGroup):
    if versionGroup == '':
        versionGroupName = 'Unknown'
    elif versionGroup == 'legends-za':
        versionGroupName = 'Legends Z-A'
    else:
        versionGroupName = re.split(r'[\s-.]+', versionGroup)
        versionGroupName = ' '.join(word.capitalize() for word in versionGroupName)

    return versionGroupName

def getSerebiiLink(gameGen, monData):
    serebiiLink = f'https://www.serebii.net/pokedex{gameGen["Serebii-Link"]}/'

    zeroFilledDexNum = str(monData["species"]["url"][42:].strip("/")).zfill(3)

    if gameGen['Name'] >= 8:
        serebiiLink += formatMonForSerebii(int(zeroFilledDexNum))
    else:
        serebiiLink += f'{zeroFilledDexNum}.shtml'

    return serebiiLink

def formatMonForSerebii(dexNum):
    hyphenDexNum = [250, 474, 782, 783, 784, 1001, 1002, 1003, 1004]
    apostropheDexNum = [83, 865]
    periodDexNum = [122, 866]
    trailingPeriodDexNum = [439]
    colonDexNum = [772]

    if dexNum in hyphenDexNum:
        joinChar = '-'
    elif dexNum in apostropheDexNum:
        joinChar = '\''
    elif dexNum in periodDexNum:
        joinChar = '.'
    elif dexNum in colonDexNum:
        joinChar = ':'
    else:
        joinChar = ''
    
    if dexNum in trailingPeriodDexNum:
        trailingChar = '.'
    else:
        trailingChar = ''

    mon = getMon(dexNum)
    if mon is None:
        return 'pikachu'
    
    words = re.split(r'[\s-.]+', mon['Name'])
    mon = joinChar.join(word.lower() for word in words)
    mon += trailingChar
    return mon

def getRun(runName):
    try:
        return [obj for obj in runs if obj['Name'].lower() == runName.strip().lower()][0]
    except:
        return None
    
def matchPlayer(player, run):
    try:
        return run['Players'].index(player)
    except:
        return None
    
def checkEncounter(name, run):
    return any(encounter['Name'].lower() == name.lower() for encounter in run['Encounters'])

def determineGenSpecificSprite(gameGen, versionGroup):
    baseUrlAddition = ''
    extension = '.png'
    rollShiny = True

    if gameGen['Name'] <= 5:
        if versionGroup == 'gold-silver':
            randNum = random.randint(0,1)
            if randNum == 0:
                versionName = 'gold'
            else:
                versionName = 'silver'
        elif versionGroup == 'black-2-white-2':
            versionName = 'black-white'
        else:
            versionName = versionGroup

        if gameGen['Name'] == 1:
            rollShiny = False

        baseUrlAddition += f'/versions/generation-{gameGen["Roman-Numeral"].lower()}/{versionName}/'
        
        if gameGen['Name'] == 5:
            baseUrlAddition += 'animated/'
            extension = '.gif'

    return baseUrlAddition, extension, rollShiny

def addMoveData(moveset, moveData):
    for move, data in zip(moveset, moveData):
        move['Type'] = str(data['type']['name']).capitalize()
        move['Category'] = str(data['damage_class']['name']).capitalize()
        move['Power'] = '᲼\-᲼' if data['power'] is None else str(data['power']).rjust(3, '᲼')
        move['Accuracy'] = '᲼\-' if data['accuracy'] is None else str(data['accuracy']).rjust(3, '᲼')

    return moveset

def getGameData(gameName):
    try:
        return [obj for obj in games if any(group == gameName for group in obj['Games'])][0]
    except:
        return None

def getGroupGen(versionGroup):
    try:
        return [obj for obj in gens if any(group["Name"] == versionGroup for group in obj["Version-Groups"])][0]
    except:
        return None

def getGameEmbedColour(gameName):
    try:
        gameData = getGameData(gameName)
        return gameData['Colour'][[game for game in gameData['Games']].index(gameName)]
    except:
        return sharedEmbedColours.get('Default')
    
def getGameMascot(gameName):
    try:
        gameData = getGameData(gameName)
        return gameData["Mascot"][[game for game in gameData["Games"]].index(gameName)]
    except:
        return 213
    
def getGameLinkEmoji(gameName):
    try:
        gameData = getGameData(gameName)
        return gameData['Link-Emoji'][[game for game in gameData['Games']].index(gameName)]
    except:
        return ''
#endregion

#region $sl new-sl command and createRole func
async def createNewRun(game, name, players, guild):
    versionGroup = getGroup(game)

    if versionGroup is None:
        return 'The name of the game wasn\'t recognized!'
    
    if len(name) > 50:
        return 'Limit the name of the run to less than 50 characters!'
    
    if checkDuplicateName(name):
        return 'The run name has been used before! Use unique names!'

    encounters = []
    encounterList = [obj for obj in games if obj['Name'] == versionGroup][0]['Progression'][0]['Encounters']

    for encounter in encounterList:
        encounters.append({
            'Name': encounter,
            'Pokemon': [-1 for i in players],
            'Completed': False,
            'Alive': True,
            'Death-Reason': ''
        })

    runs.append({
        'Name': name,
        'Game': game,
        'Version-Group': versionGroup,
        'Current-Progress': 0,
        'Players': players,
        'Encounters': encounters,
        'Run-Status': 'In Progress',
        'Teams': [[]],
        'Run-Notes': ''
    })

    currentRun['VersionGroup'] = versionGroup
    currentRun['RunName'] = name

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    await createRole(players, guild)

    return 'Run Created! Focus set to the newly created run!'

async def createRole(players, guild):
    try:
        run = getRun(currentRun['RunName'])
        
        if run is None:
            raise Exception('Somehow the run name is invalid. Get Anderson to look into it lol')

        rand_num = random.randint(1, 5)
        match rand_num:
            case 1:
                role_name = f'{currentRun["RunName"]} Gamers'
            case 2:
                role_name = f'{currentRun["RunName"]} Runners'
            case 3:
                role_name = f'Lobotomy Patients Attempt {currentRun["RunName"]}'
            case 4:
                role_name = f'Haha Funny {currentRun["RunName"]} Ping Role' 
            case 5:
                role_name = f'Gaslighting Central at {currentRun["RunName"]}'
            case _:
                role_name = currentRun['RunName']
                
        role = await guild.create_role(name=role_name)

        await role.edit(color=getGameEmbedColour(run['Game']))

        for player in players:
            userId = int(player[2:-1])
            user = guild.get_member(userId)

            await user.add_roles(role)
        
    except Exception as ex:
        print(f'An error occured while making a role!\n{ex}')
#endregion

#region $sl encounter command
async def encounterMon(encounterName, encounter, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    playerIndex = matchPlayer(player, run)
    dexNum = getDexNum(encounter)

    if playerIndex is None:
        return f'\'{player}\' was not recogized as a player in the currently selected run!'
    
    if dexNum == -1:
        return f'\'{encounter}\' was not recognized as a pokemon!'
    
    if not checkEncounter(encounterName, run):
        return f'\'{encounterName}\' was not recognized as a valid area for an encounter! Make sure to use the \'$sl progress\' command after each major battle to unlock new encounters!'
    
    encounterData = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounterName.lower()][0]

    encounterData['Pokemon'][playerIndex] = dexNum

    if all(num != -1 for num in encounterData['Pokemon']):
        encounterData['Completed'] = True
    
    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'{formatTextForDisplay(encounter)} successfully added for {player} for {formatTextForDisplay(encounterName)}!'
    
async def encounterMonGroup(encounterName, encounters):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    if not checkEncounter(encounterName, run):
        return f'\'{encounterName}\' was not recognized as a valid area for an encounter! Make sure to use the \'$sl progress\' command after each major battle to unlock new encounters!'
    
    encounterData = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounterName.lower()][0]

    responseText = ''

    for encounter in encounters:
        encounter = re.split(r'[\s]+', encounter.strip())
        if len(encounter) < 2:
            responseText += f'\'{encounter}\' was formatted incorrectly!\n'
            continue
        else:
            player = encounter[0].strip()
            encounter = ' '.join(word.lower().capitalize() for word in encounter[1:])

        playerIndex = matchPlayer(player, run)
        dexNum = getDexNum(encounter)

        if playerIndex is None:
            responseText += f'\'{player}\' was not recogized as a player in the currently selected run!\n'
            continue
    
        if dexNum == -1:
            responseText += f'\'{encounter}\' was not recognized as a pokemon!\n'
            continue

        encounterData['Pokemon'][playerIndex] = dexNum

        responseText += f'{formatTextForDisplay(encounter)} successfully added for {player} for {formatTextForDisplay(encounterName)}!\n'
    
    if all(num != -1 for num in encounterData['Pokemon']):
        encounterData['Completed'] = True
    
    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return responseText

#endregion

#region $sl encounters command
async def listEncounters():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    encounterData = [obj['Name'] for obj in run['Encounters'] if not obj['Completed']]

    if len(encounterData) == 0:
        return 'There are no available encounters! Use `$sl progress` after a major battle to unlock more!'

    embeds = []

    playerData = [set(player for i, player in enumerate(run['Players']) if encounter['Pokemon'][i] == -1) for encounter in run['Encounters'] if not encounter['Completed']]

    embed = discord.Embed(title=f'{currentRun["RunName"]} Available Encounters',
                          color=getGameEmbedColour(run['Game']))
    
    if run['Current-Progress'] <= 1 and run['Version-Group'] == 'heartgold-soulsilver':
        embed.set_author(name='Egg Id Website', url='https://www.pokewiki.de/Spezial:Geheimcode-Generator?uselang=en')
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(getGameMascot(run['Game'])))
    
    fieldTitles = ['Location', 'Players']
    fieldContent = ['', '']
    pageCount = 10

    for i, (encounter, playersEncounter) in enumerate(zip(encounterData, playerData), start=1):
        fieldContent[0] += f'{encounter}\n'
        fieldContent[1] += f'{"All Players" if len(playersEncounter) == len(run["Players"]) else " ".join(playersEncounter)}\n'
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['', '']
    
    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds

#endregion

#region $sl links and link-data command
async def listLinks():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    encounterData = [obj for obj in run['Encounters'] if obj['Completed'] and obj['Alive']]

    if len(encounterData) == 0:
        return 'There are no links alive! Wonder what fraud is to blame...'
    
    embeds = []
    linkEmoji = getGameLinkEmoji(run['Game'])

    embed = discord.Embed(title=f'{currentRun["RunName"]} Active Links',
                          description=linkEmoji.join(run['Players']),
                          color=getGameEmbedColour(run['Game']))
    
    fieldTitles = ['']
    fieldContent = ['']
    pageCount = 10

    for i, encounter in enumerate(encounterData, start=1):
        fieldContent[0] += f'{linkEmoji.join(getMonName(obj) for obj in encounter["Pokemon"])}\n'
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['']
    
    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds

async def getLinkData(input, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    playersText = ''
    linkEmoji = getGameLinkEmoji(run['Game'])

    for player_name in run['Players']:
        if player_name == run['Players'][-1]:
            playersText += f'{player_name}'
        else:
            playersText += f'{player_name}{linkEmoji}'

    embed = discord.Embed(title=f'Link Data',
                          description=playersText,
                          color=getGameEmbedColour(run['Game']))

    if checkEncounter(input, run):
        encounterData = [encounter for encounter in run['Encounters'] if encounter['Name'].lower() == input.lower()][0]
        encountersText = ''
        for index, dexNum in enumerate(encounterData['Pokemon']):
            if dexNum == -1:
                monName = 'X'
            else:
                monName = getMonName(dexNum)
                if monName is None:
                    monName = 'Invalid Name'
            if index == len(encounterData['Pokemon']) - 1:
                encountersText += f'{monName}\n'
            else:
                encountersText += f'{monName}{linkEmoji}'

        if encounterData['Alive']:
            status = 'Alive'
        else:
            status = 'Dead'

        embed.add_field(name=f'{encounterData["Name"]} - {status}',
                        value=encountersText,
                        inline=True)
        
        return embed
    else:
        dexNum = getDexNum(input)

        if dexNum == -1:
            return f'\'{input}\' was not recognized as a valid mon name or as an encounter location!'
        
        playerIndex = matchPlayer(player, run)

        if playerIndex is None:
            return 'The author of this input was not recognized as a player in the currently selected run!'
        
        encounterData = [obj for obj in run['Encounters'] if obj['Pokemon'][playerIndex] == dexNum]
        
        if len(encounterData) >= 1:
            encounterData = encounterData[0]
        else:
            return f'You do not own a {formatTextForDisplay(input)}!'

        encountersText = ''
        for index, dexNum in enumerate(encounterData['Pokemon']):
            if dexNum == -1:
                monName = 'X'
            else:
                monName = getMonName(dexNum)
                if monName is None:
                    monName = 'Invalid Name'
            if index == len(encounterData['Pokemon']) - 1:
                encountersText += f'{monName}\n'
            else:
                encountersText += f'{monName}{linkEmoji}'

        if encounterData['Alive']:
            status = 'Alive'
        else:
            status = 'Dead'

        embed.add_field(name=f'{encounterData["Name"]} - {status}',
                        value=encountersText,
                        inline=True)
        
        return embed
#endregion
    
#region $sl evolve and undo-evolve command
async def evolveMon(monName, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    dexNum = getDexNum(monName)
    mon = getMon(dexNum)

    if dexNum == -1 or mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon!'
    
    playerIndex = matchPlayer(player, run)

    if playerIndex is None:
        return 'The author of this input was not recognized as a player in the currently selected run!'
    
    if len(mon['Evolves-Into']) == 0:
        return f'{formatTextForDisplay(monName)} can\'t evolve!'
    
    encounterData = [obj for obj in run['Encounters'] if obj['Pokemon'][playerIndex] == dexNum and obj['Completed'] and obj['Alive']]

    if len(encounterData) >= 1:
        encounterData = encounterData[0]
    else:
        return f'You do not own a {formatTextForDisplay(monName)}!'
    
    evoMon = getMon(mon['Evolves-Into'][0]['DexNum'])

    encounterData['Pokemon'][playerIndex] = evoMon['DexNum']

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'Your {formatTextForDisplay(monName)} from {encounterData["Name"]} has evolved into a {formatTextForDisplay(evoMon["Name"])}!\nIf this was a mistake, use $sl undo-evolve {formatTextForDisplay(evoMon["Name"])}\nIf this is not the correct evolution, use $sl encounter {encounterData["Name"]}, evo-name-here'

async def undoEvolveMon(monName, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    dexNum = getDexNum(monName)
    mon = getMon(dexNum)

    if dexNum == -1 or mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon!'
    
    playerIndex = matchPlayer(player, run)

    if playerIndex is None:
        return 'The author of this input was not recognized as a player in the currently selected run!'
    
    if mon['Evolves-From'] is None:
        return f'{formatTextForDisplay(monName)} doesn\'t have a pre-evo!'
    
    encounterData = [obj for obj in run['Encounters'] if obj['Pokemon'][playerIndex] == dexNum and obj['Completed'] and obj['Alive']]

    if len(encounterData) >= 1:
        encounterData = encounterData[0]
    else:
        return f'You do not own a {formatTextForDisplay(monName)}!'
    
    pre_evo_mon = getMon(mon['Evolves-From'])

    encounterData['Pokemon'][playerIndex] = pre_evo_mon['DexNum']

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'Your {formatTextForDisplay(monName)} from {encounterData["Name"]} unevolved back into a {formatTextForDisplay(pre_evo_mon["Name"])}!'
#endregion

#region $sl death and undo-death command
async def newDeath(encounterName, reason):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if len(reason) > 500:
        return 'Make the reason for death shorter than 500 characters!'
    
    if not checkEncounter(encounterName, run):
        return f'\'{encounterName}\' was not recognized as a valid encounter name!'
    
    encounterData = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounterName.lower()][0]
    
    encounterData['Alive'] = False
    encounterData['Death-Reason'] = reason

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'The encounter from {encounterData["Name"]} has been marked as dead! If this was a mistake, use $sl undo-death {encounterData["Name"]}'

async def undoDeath(encounterName):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if not checkEncounter(encounterName, run):
        return f'\'{encounterName}\' was not recognized as a valid encounter name!'
    
    encounterData = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounterName.lower()][0]
    
    if encounterData['Alive']:
        return f'The encounter from {encounterData["Name"]} is alive and well! Use $sl death {encounterData["Name"]} if you wanted to mark the encounter as dead!'

    encounterData['Alive'] = True
    encounterData['Death-Reason'] = ''

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'The encounter from {encounterData["Name"]} has been revived!'

#endregion

#region $sl ask-shuckle command
async def askShuckle(userInput):
    #randNum = random.randint(0, 1)
    systemContent = loadShucklePersonality('original')
        
    messages = [
        {'role':'system', 'content': systemContent},

        {'role':'user', 'content':userInput}
    ]
    try:
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages = messages, temperature=0.8, max_tokens=500)

        return response.choices[0].message.content[:2000]
    except Exception as ex:
        print(ex)
        return 'Anderson ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
#endregion

#region $sl deaths command
async def listDeaths():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    embeds = []

    encounterData = [obj for obj in run['Encounters'] if not obj['Alive']]

    if len(encounterData) == 0:
        return 'There are no deaths yet! Some fraud is bound to make a mistake soon...'

    playersText = ''
    encountersText = ''
    linkEmoji = getGameLinkEmoji(run['Game'])

    for player in run['Players']:
        if player == run['Players'][-1]:
            playersText += f'{player}'
        else:
            playersText += f'{player}{linkEmoji}'

    embed = discord.Embed(title=f'{currentRun["RunName"]} Deaths',
                          description=playersText,
                          color=getGameEmbedColour(run['Game']))
    
    for encounter in encounterData:
        encountersText += f'{encounter["Name"]}\n'
        for index, dexNum in enumerate(encounter['Pokemon']):
            if dexNum == -1:
                monName = 'X'
            else:
                monName = getMonName(dexNum)
                if monName is None:
                    monName = 'Invalid Name'
            if index == len(encounter['Pokemon']) - 1:
                encountersText += f'{monName}\n'
            else:
                encountersText += f'{monName}{linkEmoji}'

        embed.add_field(name=encountersText,
                        value=encounter['Death-Reason'],
                        inline=True)
            
        embeds.append(copy.deepcopy(embed))

        embed.clear_fields()
        encountersText = ''
        playersText = ''
    
    return embeds
#endregion

#region $sl runs, reset, select-run command
def selectRun(name):
    run = getRun(name)

    if run is None:
        return 'The name of the run wasn\'t recognized!'
    
    currentRun['VersionGroup'] = copy.deepcopy(run['Version-Group'])
    currentRun['RunName'] = copy.deepcopy(run['Name'])

    return f'Focus set to run \'{run["Name"]}\'!'

def resetFocus():
    global currentRun

    currentRun = copy.deepcopy(defaultRun)

    return 'Run unfocused!'

async def listRuns():
    embeds = []

    embed = discord.Embed(title=f'Scuffed Soul Links Runs',
                          color=sharedEmbedColours.get('Default'))
    
    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    fieldTitles = ['Run Names', 'Players', 'Status']
    fieldContent = ['', '', '']
    pageCount = 10

    for i, run in enumerate(runs, start=1):
        fieldContent[0] += f'{run["Name"]}\n'
        fieldContent[1] += f'{run["Run-Status"]}\n'
        fieldContent[2] += f'{len(run["Players"])}\n'
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['', '', '']
    
    if fieldContent[0] != '':
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds

#endregion

#region $sl choose-team command
async def chooseTeam(links, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    playerIndex = matchPlayer(player, run)

    if playerIndex is None:
        return 'The author of this input was not recognized as a player in the currently selected run!'
    
    encounterData = []

    for link in links:
        tempLink = link
        link = getDexNum(link.strip())
        if link is None:
            return f'\'{tempLink}\' was not recognized as a valid pokemon name!'
        
        encounterLink = [obj for obj in run['Encounters'] if obj['Pokemon'][playerIndex] == link]

        if len(encounterLink) > 0: 
            try:
                encounterData.append(copy.deepcopy([obj for obj in run['Encounters'] if obj['Pokemon'][playerIndex] == link and obj['Completed'] and obj['Alive']][0]['Pokemon']))
            except:
                return f'\'{formatTextForDisplay(tempLink)}\' was not paired to a completed or alive link! Some fraud needs to mark their encounters or deaths!'
        else:
            return f'\'{formatTextForDisplay(tempLink)}\' was not recognized as a pokemon you own! Make sure you\'re listing out your pokemon, and not everyone elses pokemon'
    
    run['Teams'][run['Current-Progress']] = encounterData

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    randomUser = await pingUser()

    return f'Team successfully set for the upcoming battle with {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run["Current-Progress"]]["Battle-Name"]}. {randomUser} gets to go first.\nUse the $sl random command if you want to reroll who starts the battle first!'
#endregion

#region $sl next-battle command
async def nextBattle():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    return f'The next battle is with {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run["Current-Progress"]]["Battle-Name"]}, and the level cap is {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run["Current-Progress"]]["Level-Cap"]}.'
#endregion

#region $sl progress command
async def progressRun():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if (len([obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"]) - 1) > run['Current-Progress']:
        run['Current-Progress'] += 1

        run['Teams'].append([])

        for newEncounter in [obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run['Current-Progress']]['Encounters']:
            run['Encounters'].append({
                'Name': newEncounter,
                'Pokemon': [-1 for i in run['Players']],
                'Completed': False,
                'Alive': True,
                'Death-Reason': ''
            })
    else:
        return 'We\'re already in the end-game!'
    
    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return 'The run was successfully advanced! New encounters are available! Surely nobody threw too hard in that last battle...'
#endregion

#region $sl random command
async def pingUser():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    rand_num = random.randint(0, len(run['Players']) - 1)

    return run['Players'][rand_num]

#endregion

#region $sl add-note command
async def addNote(note):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if len(note) > 250:
        return 'Keep the notes short. Less than 250 characters.'
    
    run['Run-Notes'] += f'{note}\n'

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'Note successfully added to {run["Name"]}'
#endregion

#region $sl run-info command
def splitRunNotes(notes):
    runNotes = []
    while notes:
        if len(notes) <= 1024:
            runNotes.append(notes)
            break
    
        splitAt = notes.rfind('\n', 0, 1024)
        if splitAt == -1:
            splitAt = 1024

        runNotes.append(notes[:splitAt])
        notes = notes[splitAt:].lstrip('\n')

    return runNotes

async def seeStats():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    embeds = []

    if run['Run-Status'] == 'In Progress':
        descriptionText = 'This run is currently In Progress!'
    else:
        descriptionText = f'This run ended in {run["Run-Status"]}!'

    descriptionText += '\nTo see active and dead links, use the $sl links and $sl deaths commands!'

    playersText = ''
    linksText = ''
    linkEmoji = getGameLinkEmoji(run['Game'])

    for player in run['Players']:
        if player == run['Players'][-1]:
            playersText += f'{player}'
        else:
            playersText += f'{player}{linkEmoji}'

    embed = discord.Embed(title=f'{currentRun["RunName"]} Stats',
                          description=f'{descriptionText}\n{playersText}',
                          color=getGameEmbedColour(run['Game']))
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(getGameMascot(run['Game'])))
    
    for progress_index in range(run['Current-Progress'] + 1):
        embed.title = f'{currentRun["RunName"]} Info\nThe Team vs. {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][progress_index]["Battle-Name"]} at Lv. {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][progress_index]["Level-Cap"]}!'
        
        if len(run['Teams'][progress_index]) > 0:
            for encounter in run['Teams'][progress_index]:
                for i, dexNum in enumerate(encounter):
                    monName = getMonName(dexNum)
                    if monName is None:
                        monName = 'Invalid Name'
                    if i == len(encounter) - 1:
                        linksText += f'{monName}\n'
                    else:
                        linksText += f'{monName}{linkEmoji}'
        else:
            linksText = 'No team was specified for this battle!'
        
        embed.add_field(name='',
                        value=linksText,
                        inline=True)
        
        embeds.append(copy.deepcopy(embed))

        embed.clear_fields()
        linksText = ''

    embed.title = f'{currentRun["RunName"]} Info\nRun Notes'
    embed.description = descriptionText

    for note in splitRunNotes(run['Run-Notes']):
        embed.add_field(name='',
                        value=note,
                        inline=True)

        embeds.append(copy.deepcopy(embed))
        embed.clear_fields()

    return embeds
#endregion 

#region $sl win-run, fail-run, undo-status command
async def setRunStatus(status, guild):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if run['Run-Status'] == status:
        return f'The runs status is already {status}!'
    
    allRoles = await guild.fetch_roles()

    try:
        for role in allRoles:
            if run['Name'] in role.name:
                await role.delete()
    except Exception as ex:
        print(ex)

    run['Run-Status'] = status
    
    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'The runs status was set to {status}! If this was a mistake, use $sl undo-status!'

#endregion

#endregion

#region dex commands

#region evo chain image
async def createArrowImage(direction, type, method, value):
    arrowImg = Image.open(f'images/evo_helpers/arrows/arrow_{type}.png').convert('RGBA')
    if method == 'level-up':
        draw = ImageDraw.Draw(arrowImg)
        font = ImageFont.truetype('fonts/pkmndp.ttf', 10)
        draw.text((10,15), f"Lv. {value}", 'black', font=font)

        return arrowImg.rotate(direction)
    
    elif method == 'use-item':
        itemImage = await openHttpImage(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/{value}.png', False)

        arrowImg.paste(itemImage, (10, 4), mask=itemImage)
        itemImage.close()

    #use item-img covers trade, friendship and mega evos as well
    elif method == 'use-item-img':
        try:
            itemImage = Image.open(f'images/evo_helpers/{value}.png').convert('RGBA')
        except FileNotFoundError:
            itemImage = Image.open(f'images/evo_helpers/small_missing_no.png').convert('RGBA')
    
        arrowImg.paste(itemImage, (10, 4), mask=itemImage)
        itemImage.close()

    return arrowImg.rotate(direction)

async def pasteOnImage(backgroundImage, dexNum, positionX, positionY):
    image = await openHttpImage(getPokeAPISpriteUrl(dexNum))

    backgroundImage.paste(image, (positionX, positionY), mask=image)
    image.close()

    return backgroundImage

async def pasteArrowImage(backgroundImage, positionX, positionY, direction, type, method, value):
    arrowImage = await createArrowImage(direction, type, method, value)

    backgroundImage.paste(arrowImage, (positionX, positionY), mask=arrowImage)
    arrowImage.close()

    return backgroundImage

async def pastePokemonOntoBackground(backgroundImage, pokemonToPaste, arrowType, pokemonPositions, arrowPositions):
    for mon, monPos in zip(pokemonToPaste, pokemonPositions):
        backgroundImage = await pasteOnImage(backgroundImage, mon['DexNum'], monPos[0], monPos[1])

    for mon, arrowPos in zip(pokemonToPaste[1:], arrowPositions):
        backgroundImage = await pasteArrowImage(backgroundImage, arrowPos[0], arrowPos[1], arrowPos[2], arrowType, mon['Method'], mon['Value'])

    return backgroundImage

async def createEvoChainImage(dexNum, type):
    basePokemon = getMon(dexNum)
                
    while basePokemon['Evolves-From'] is not None:
        basePokemon = getMon(basePokemon['Evolves-From'])
    
    evoChainLength = 1
    if len(basePokemon['Evolves-Into']) > 0:
        evoChainLength = 2
        for evo in basePokemon['Evolves-Into']:
            evo = getMon(evo['DexNum'])
            if len(evo['Evolves-Into']) > 0:
                evoChainLength = 3

    backgroundImage = Image.open(f'images/type_backgrounds/{type}.png')

    if evoChainLength == 1:
        #no evolutions
        evoMons = [basePokemon]
        monPositions = [[150, 50]]
        arrowPositions = []
        
        backgroundImage = await pasteOnImage(backgroundImage, dexNum, 150, 50)
        
    elif evoChainLength == 2:
        #2 stage evo line, like vulpix
        if len(basePokemon['Evolves-Into']) == 1:
            #only one evo
            evoMons = [basePokemon, basePokemon['Evolves-Into'][0]]
            monPositions = [[75, 50], [225, 50]]
            arrowPositions = [[175, 90, 0]]

        elif len(basePokemon['Evolves-Into']) == 2:
            #2 evos, like slowpoke
            evoMons = [basePokemon, basePokemon['Evolves-Into'][0], basePokemon['Evolves-Into'][1]]
            monPositions = [[75, 50], [225, 0], [225, 100]]
            arrowPositions = [[175, 55, 45], [175, 125, -45]]

        elif len(basePokemon['Evolves-Into']) == 3:
            #3 evos, like tyrogue
            evoMons = [basePokemon, basePokemon['Evolves-Into'][0], basePokemon['Evolves-Into'][1], basePokemon['Evolves-Into'][2]]
            monPositions = [[75, 50], [225, 0], [225, 100], [300, 50]]
            arrowPositions = [[175, 55, 45], [175, 125, -45], [200, 90, 0]]

        elif len(basePokemon['Evolves-Into']) == 8:
            #eevee
            evoMons = [basePokemon, basePokemon['Evolves-Into'][0], basePokemon['Evolves-Into'][1], 
                       basePokemon['Evolves-Into'][2], basePokemon['Evolves-Into'][3], 
                       basePokemon['Evolves-Into'][4], basePokemon['Evolves-Into'][5], 
                       basePokemon['Evolves-Into'][6], basePokemon['Evolves-Into'][7]]
            monPositions = [[148, 50], [225, 0], [225, 100],
                            [300, 100], [75, 0], [0, 100],
                            [0, 0], [75, 100], [300, 0]]
            arrowPositions = []
            
    elif evoChainLength == 3:
            #3 stage evo line
            if len(basePokemon['Evolves-Into']) == 1:
                #only one middle evo
                middlePokemon = getMon(basePokemon['Evolves-Into'][0]['DexNum'])
                if len(middlePokemon['Evolves-Into']) == 1:
                    #only one final evo, like venusaur
                    evoMons = [basePokemon, basePokemon['Evolves-Into'][0], middlePokemon['Evolves-Into'][0]]
                    monPositions = [[0, 50], [150, 50], [300, 50]]
                    arrowPositions = [[100, 90, 0], [250, 90, 0]]

                elif len(middlePokemon['Evolves-Into']) == 2:
                    #two final evos like kirlia
                    evoMons = [basePokemon, basePokemon['Evolves-Into'][0], 
                               middlePokemon['Evolves-Into'][0], middlePokemon['Evolves-Into'][1]]
                    monPositions = [[0, 50], [150, 50], [300, 0], [300, 100]]
                    arrowPositions = [[100, 90, 0], [250, 55, 45], [250, 125, -45]]

            elif len(basePokemon['Evolves-Into']) == 2:
                #2 middle evos, like mr mime
                middlePokemon = [getMon(basePokemon['Evolves-Into'][0]['DexNum']), getMon(basePokemon['Evolves-Into'][1]['DexNum'])]

                evoMons = [basePokemon, basePokemon['Evolves-Into'][0], basePokemon['Evolves-Into'][1]]
                monPositions = [[0, 50], [150, 0], [150, 100]]
                arrowPositions = [[100, 55, 45], [100, 125, -45]]

                if len(middlePokemon[0]['Evolves-Into']) != 0:
                    evoMons.append(middlePokemon[0]['Evolves-Into'][0])
                    monPositions.append([300, 0])
                    arrowPositions.append([250, 55, 0])
                    
                if len(middlePokemon[1]['Evolves-Into']) != 0:
                    evoMons.append(middlePokemon[1]['Evolves-Into'][0])
                    monPositions.append([300, 100])
                    arrowPositions.append([250, 125, 0])
                
            elif len(basePokemon['Evolves-Into']) == 3:
                #3 evos with a 3rd stage, like applin
                middlePokemon = [getMon(basePokemon['Evolves-Into'][0]['DexNum']), getMon(basePokemon['Evolves-Into'][1]['DexNum']), getMon(basePokemon['Evolves-Into'][2]['DexNum'])]

                evoMons = [basePokemon, basePokemon['Evolves-Into'][0], basePokemon['Evolves-Into'][1], basePokemon['Evolves-Into'][2]]
                monPositions = [[0, 50], [150, 0], [150, 100], [200, 50]]
                arrowPositions = [[100, 55, 45], [100, 125, -45], [125, 90, 0]]

                if len(middlePokemon[0]['Evolves-Into']) != 0:
                    evoMons.append(middlePokemon[0]['Evolves-Into'][0])
                    monPositions.append([275, 0])
                    arrowPositions.append([250, 55, 0])

                if len(middlePokemon[1]['Evolves-Into']) != 0:
                    evoMons.append(middlePokemon[1]['Evolves-Into'][0])
                    monPositions.append([275, 100])
                    arrowPositions.append([250, 125, 0])

                if len(middlePokemon[2]['Evolves-Into']) != 0:
                    evoMons.append(middlePokemon[2]['Evolves-Into'][0])
                    monPositions.append([315, 50])
                    arrowPositions.append([275, 90, 0])
       

    backgroundImage = await pastePokemonOntoBackground(backgroundImage, evoMons, type, monPositions, arrowPositions)

    imageBuffer = BytesIO()

    backgroundImage.save(imageBuffer, format='PNG')

    backgroundImage.close()

    imageBuffer.seek(0)

    return imageBuffer.getvalue()
    #return discord.File(imageBuffer, filename=f'{type}.png')
#endregion

#region $sl dex command
async def makePokedexEmbed(mon, gameName):
    dexNum = getDexNum(mon)

    versionGroup = getGroup(gameName)

    if versionGroup is None:
        versionGroup = copy.deepcopy(currentRun['VersionGroup'])

    embeds = []

    if dexNum == -1:
        return f'The pokemon \'{mon}\' was not recognized!'
    
    if gameName is not None and versionGroup is None:
        return f'\'{gameName}\' was not recognized as a valid game name!'

    monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{dexNum}')

    if monData is None:
        return f'An error occured while checking the api!'

    monTypes = []
    typeEmojis = ''

    for type in monData['types']:
        typeName = type['type']['name'].capitalize()
        monTypes.append(typeName)
        typeEmojis += getTypeEmoji(typeName)
    
    movesets, versionGroup = await getMoves(monData['moves'], versionGroup)

    imageBuffer = await createEvoChainImage(dexNum, monTypes[0])

    stats = {obj['stat']['name']: obj['base_stat'] for obj in monData['stats']}

    embed = discord.Embed(title=f'#{monData["species"]["url"][42:].strip("/")} {getMonName(dexNum)} {typeEmojis}',
                          color=getTypeColour(monTypes[0]))

    if versionGroup != '':
        gameGen = getGroupGen(versionGroup)

        baseUrlAddition, extension, rollShiny = determineGenSpecificSprite(gameGen, versionGroup)

        embed.set_thumbnail(url=getPokeAPISpriteUrl(dexNum, baseUrlAddition=baseUrlAddition, extension=extension, rollShiny=rollShiny))

        serebiiLink = getSerebiiLink(gameGen, monData)
    else:
        embed.set_thumbnail(url=getPokeAPISpriteUrl(dexNum))
        serebiiLink = 'https://www.serebii.net'
        
    embed.set_author(name='Pokémon Data', url=serebiiLink)

    embed.set_image(url=f"attachment://{monTypes[0]}.png")

    embeds = addPaginatedLearnsetEmbeds(embed, embeds, movesets, 'Level', 'Level', stats, versionGroup, imageBuffer, monTypes)
    
    if len(movesets['Machine']) > 0:
        embeds = addPaginatedLearnsetEmbeds(embed, embeds, movesets, 'Machine', 'TM #', stats, versionGroup, imageBuffer, monTypes)

    if len(movesets['Tutor']) > 0:
        embeds = addPaginatedLearnsetEmbeds(embed, embeds, movesets, 'Tutor', 'Tutor', stats, versionGroup, imageBuffer, monTypes, uniqueFieldTextOverride='-')
    
    if len(movesets['Egg']) > 0:
        embeds = addPaginatedLearnsetEmbeds(embed, embeds, movesets, 'Egg', 'Egg Move', stats, versionGroup, imageBuffer, monTypes, uniqueFieldTextOverride='-')

    return embeds

def addCommonDexEmbedFields(embed, stats, versionGroup, level=0):
    if level > 0:
        embed.add_field(name=f'Stats - {sum(stats.values())} BST',
                    value=f'HP: {calculateHpStat(int(stats["hp"]), level)}\nAtk: {calculateStat(int(stats["attack"]), level)}\nDef: {calculateStat(int(stats["defense"]), level)}',
                    inline=True)
    
        embed.add_field(name=f'31 IVs, 0 EVs, Neutral',
                        value=f'Speed: {calculateStat(int(stats["speed"]), level)}\nSp.Atk: {calculateStat(int(stats["special-attack"]), level)}\nSp.Def: {calculateStat(int(stats["special-defense"]), level)}',
                        inline=True)
    
    else:
        embed.add_field(name=f'Stats - {sum(stats.values())} BST',
                        value=f'HP: {stats["hp"]}\nAtk: {stats["attack"]}\nDef: {stats["defense"]}',
                        inline=True)
        
        embed.add_field(name=f'᲼',
                        value=f'Speed: {stats["speed"]}\nSp.Atk: {stats["special-attack"]}\nSp.Def: {stats["special-defense"]}',
                        inline=True)

    embed.add_field(name=f'Moveset Data from {formatVersionGroupName(versionGroup)}',
                    value='',
                    inline=False)
    
    return embed

def addPaginatedLearnsetEmbeds(embed, embeds, movesets, movesetKey, uniqueFieldHeader, stats, versionGroup, imageBuffer, monTypes, uniqueFieldTextOverride=None):
    if not movesets[movesetKey]:
        return embeds
    
    fieldTitles = [uniqueFieldHeader, 'Name', 'Type']
    fieldContent = ['', '', '']

    pageCount = 20
    for i, move in enumerate(movesets[movesetKey], start=1):
        fieldContent[0] += f'{uniqueFieldTextOverride if uniqueFieldTextOverride is not None else move[movesetKey]}\n'
        fieldContent[1] += f'{move["Name"]}\n'
        fieldContent[2] += f'᲼{getTypeEmoji(move["Type"], moveCategory=move["Category"])}\n'

        if i % pageCount == 0:
            embed = addCommonDexEmbedFields(embed, stats, versionGroup)
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds, extraEmbedData=(imageBuffer, f'{monTypes[0]}', 'png'))
            fieldContent = ['', '', '']

    if fieldContent[0] != '':
        embed = addCommonDexEmbedFields(embed, stats, versionGroup)
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds, extraEmbedData=(imageBuffer, f'{monTypes[0]}', 'png'))

    return embeds
#endregion

#region $sl moves command
def machineSortKey(move):
    machineName = move.get('Machine')

    if machineName is None:
        move['Machine'] = '-'
        return (3, 0)

    if machineName.startswith('TM'):
        rank = 0
    elif machineName.startswith('TR'):
        rank = 1
    else:
        rank = 2

    machineNum = int(re.search(r"\d+", machineName).group())

    return (rank, machineNum)

async def getMoves(moves, versionGroup):
    if len(moves) == 0:
        return [], [], versionGroup

    if versionGroup == '':
        availableVersions = set()
        for move in moves:
            for details in move['version_group_details']:
                availableVersions.add(details['version_group']['name'])
        
        versionGroup = random.choice(list(availableVersions))
    
    moveset = []

    for move in moves:
        for version in move['version_group_details']:
            if version['version_group']['name'] == versionGroup:
                name = move['move']['name']
                words = re.split(r'[\s-.]+', name)
                name = ' '.join(word.capitalize() for word in words)
                moveset.append({'Name': name, 'Level': version['level_learned_at'], 'Method': version['move_learn_method']['name'], 'URL': move['move']['url']})
    
    if not moveset and moves:
        return await getMoves(moves, moves[random.randint(0, len(moves) - 1)]['version_group_details'][0]['version_group']['name'])
    
    levelUpMoveset = [obj for obj in moveset if obj['Method'] == 'level-up']
    machineMoveset = [obj for obj in moveset if obj['Method'] == 'machine']
    tutorMoveset = [obj for obj in moveset if obj['Method'] == 'tutor']
    eggMoveset = [obj for obj in moveset if obj['Method'] == 'egg']

    async with aiohttp.ClientSession() as session:
        levelUpTasks = [getPokeApiJsonData(move['URL'], session=session) for move in levelUpMoveset]
        levelUpMoveData = await asyncio.gather(*levelUpTasks)

        machineTasks = [getPokeApiJsonData(move['URL'], session=session) for move in machineMoveset]
        machineMoveData = await asyncio.gather(*machineTasks)

        tutorTasks = [getPokeApiJsonData(move['URL'], session=session) for move in tutorMoveset]
        tutorMoveData = await asyncio.gather(*tutorTasks)

        eggTasks = [getPokeApiJsonData(move['URL'], session=session) for move in eggMoveset]
        eggMoveData = await asyncio.gather(*eggTasks)

        machineUrls = []

        for move in machineMoveData:
            for machine in move['machines']:
                if machine['version_group']['name'] == versionGroup:
                    machineUrls.append(machine['machine']['url'])
        
        machineDataTasks = [getPokeApiJsonData(url, session=session) for url in machineUrls]
        machineItemData = await asyncio.gather(*machineDataTasks)

    levelUpMoveset = addMoveData(levelUpMoveset, levelUpMoveData)
    machineMoveset = addMoveData(machineMoveset, machineMoveData)
    tutorMoveset = addMoveData(tutorMoveset, tutorMoveData)
    eggMoveset = addMoveData(eggMoveset, eggMoveData)

    for move, data in zip(machineMoveset, machineItemData):
        move['Machine'] = str(data['item']['name']).upper()

    levelUpMoveset.sort(reverse=False, key=lambda item: item['Level'])
    machineMoveset.sort(key=machineSortKey)

    movesets = {
        'Level': levelUpMoveset,
        'Machine': machineMoveset,
        'Tutor': tutorMoveset,
        'Egg': eggMoveset
    }

    return movesets, versionGroup

def movesetTextLevel(moveset, level):
    fieldContent = ['', '', '']

    tempMoveset = []
    for move in moveset:
        if move['Level'] > level:
            break
        elif move['Name'] in [tempMove['Name'] for tempMove in tempMoveset]:
            continue
        tempMoveset.append(move)
        if len(tempMoveset) > 4:
            tempMoveset.pop(0)
    moveset = tempMoveset

    for move in moveset:
        if move['Level'] <= 1:
            comment = 'This moveset contains level 1 moves!\nDouble check the moveset with $sl dex or Serebii!'
        fieldContent[0] += f'{move["Name"]}\n'
        fieldContent[1] += f'᲼{getTypeEmoji(move["Type"], moveCategory=move["Category"])}\n'
        fieldContent[2] += f'{move["Power"]}᲼᲼{"   " if move["Power"] == "᲼-᲼" and move["Accuracy"] == "100" else ""}{move["Accuracy"]}\n'

    return fieldContent, comment

async def showMoveSet(mon, level):
    if not level.isnumeric() or int(level) > 100 or int(level) < 0:
        return f"Input invalid! Specify the pokemon\'s name and it's level! ```$sl moves Bulbasaur 24```"
    
    level = int(level)

    dexNum = getDexNum(mon)

    if dexNum == -1:
        return f"The pokemon \'{mon}\' was not recognized!"
    
    monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{dexNum}')

    if monData is None:
        return f'An error occured while checking the api!'

    monName = re.split(r'[\s-.]+', monData['name'])
    monName = ' '.join(word.capitalize() for word in monName)

    movesets, versionGroup = await getMoves(monData['moves'], currentRun['VersionGroup'])

    fieldContent, comment = movesetTextLevel(movesets['Level-Up'], level)

    stats = {obj['stat']['name']: obj['base_stat'] for obj in monData['stats']}

    embed = discord.Embed(title=f'Level {level} {monName}',
                          description=comment,
                          color=getTypeColour(monData['types'][0]['type']['name'].capitalize()))
    
    if versionGroup != '':
        gameGen = getGroupGen(versionGroup)

        baseUrlAddition, extension, rollShiny = determineGenSpecificSprite(gameGen, versionGroup)

        embed.set_thumbnail(url=getPokeAPISpriteUrl(dexNum, baseUrlAddition=baseUrlAddition, extension=extension, rollShiny=rollShiny))

        serebiiLink = getSerebiiLink(gameGen, monData)
    else:
        embed.set_thumbnail(url=getPokeAPISpriteUrl(dexNum))
        serebiiLink = 'https://www.serebii.net'

    embed.set_author(name='Moveset Data', url=serebiiLink)

    embed = addCommonDexEmbedFields(embed, stats, versionGroup, level=level)
    
    embed.add_field(name='Name',
                    value=fieldContent[0],
                    inline=True)
    
    embed.add_field(name='Type',
                    value=fieldContent[1],
                    inline=True)
    
    embed.add_field(name='Pwr ᲼ Acc',
                    value=fieldContent[2],
                    inline=True)
    
    return embed

def calculateHpStat(baseStat, level):
    if baseStat == 1:
        hpStat = 1
    else:
        hpStat = math.floor(((2 * baseStat + 31) * level)/100) + level + 10

    return hpStat

def calculateStat(baseStat, level):
    stat = math.floor(((2 * baseStat + 31) * level)/100) + 5

    return stat

#endregion

#endregion

#region $sl rare-candies command
async def makeRareCandiesEmbed():
    embeds = []

    embed = discord.Embed(title=f'Rare Candy Instructions',
                          description='',
                          color=7441607)
    
    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))
    
    embed.add_field(name='For DeSmuME DS Emulator',
                    value=  '\nEven though I\'ve had 151 beers, I remember how to use PKHex to get infinite rare candies... even the shadow people think you\'re a fraud!\n\n' +
                            'First you\'ll want to make sure you\'ve saved your game at least once, then go ahead and click on \'File/Export Backup Memory\' in DeSmuME. Save that file somewhere.\n\n' +
                            'Then open PKHex and load the save data. Go to the SAV tab above the box view, and edit the items in your bag.\n' +
                            'Then go to \'File/Export SAV\', you can overwrite the old .sav file you originally loaded at this point.\n\n' +
                            'Finally, go to \'File/Import Backup Memory\' in DeSmuME, and your game should load, complete with 999 rare candies in your bag!\n\n' +
                            'Now if you\'ll excuse me, I have a lobotomy appointment to attend. I\'ll be back after the procedure with a mind as smooth as a freshly polished Pokeball! Cheers!',
                    inline=False)
    
    embeds.append(copy.deepcopy(embed))

    embed.clear_fields()

    embed.add_field(name='For Citra 3DS Emulator',
                    value=  'Even though I\'ve had 151 beers, I remember how to use PKHex to get infinite rare candies... even the shadow people think you\'re a fraud!\n\n' +
                            'First you\'ll want to make sure you\'ve saved your game at least once, then go ahead and right-click on the game you\'re playing in Citra.\n' +
                            'Click on the \'Open Save Data Location\' option. That\'s the file you want to open in PKHex. Copy the path to that file.\n\n' +
                            'Then open PKHex and load the save data. You can paste the file path now to find it easily. Go to the SAV tab above the box view, and edit the items in your bag.\n' +
                            'Then go to \'File/Export SAV\', you can overwrite the old file you originally loaded at this point.\n\n' +
                            'And thats all, you\'re done! Enjoy your rare candies!\n\n'
                            'Now if you\'ll excuse me, I have a lobotomy appointment to attend. I\'ll be back after the procedure with a mind as smooth as a freshly polished Pokeball! Cheers!',
                    inline=False)
    
    embeds.append(embed)

    return embeds

#endregion

#region $sl catch command
async def calculateCatchRate(mon, level):
    if not level.isnumeric() or int(level) > 100 or int(level) < 0:
        return f"Input invalid! Specify the pokemon\'s name and it's level! ```$sl catch Bulbasaur 5```"
    
    level = int(level)

    dexNum = getDexNum(mon)

    if dexNum == -1:
        return f"The pokemon \'{mon}\' was not recognized!"
    
    monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{dexNum}')

    if monData is None:
        return f'An error occured while checking the api!'

    monSpecies = await getPokeApiJsonData(monData['species']['url'])

    if monSpecies is None:
        return f'An error occured while checking the api!'

    monName = re.split(r'[\s-.]+', monData['name'])
    monName = ' '.join(word.capitalize() for word in monName)

    capture_rate = monSpecies['capture_rate']

    gen = [obj for obj in gens if any(group["Name"] == currentRun["VersionGroup"] for group in obj["Version-Groups"])][0]

    if dexNum == 292:
        hp_stat = 1
    else:
        hp_stat = math.floor((((2 * int([obj for obj in monData["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"])) + random.randint(0, 31)) * level)/100) + level + 10

    catch_rate_full_poke = (((3 * hp_stat) - (2 * hp_stat))/(3 * hp_stat)) * capture_rate
    catch_rate_low_poke = (((3 * hp_stat) - 2)/(3 * hp_stat)) * capture_rate

    catch_rate_full_great = ((((3 * hp_stat) - (2 * hp_stat))/(3 * hp_stat)) * capture_rate) * 1.5
    catch_rate_low_great = ((((3 * hp_stat) - 2)/(3 * hp_stat)) * capture_rate) * 1.5

    catch_rate_full_ultra = ((((3 * hp_stat) - (2 * hp_stat))/(3 * hp_stat)) * capture_rate) * 2
    catch_rate_low_ultra = ((((3 * hp_stat) - 2)/(3 * hp_stat)) * capture_rate) * 2

    catch_rate_full_poke = 100 if catch_rate_full_poke >= 255 else (catch_rate_full_poke / 255) * 100
    catch_rate_low_poke = 100 if catch_rate_low_poke >= 255 else (catch_rate_low_poke / 255) * 100

    catch_rate_full_great = 100 if catch_rate_full_great >= 255 else (catch_rate_full_great / 255) * 100
    catch_rate_low_great = 100 if catch_rate_low_great >= 255 else (catch_rate_low_great / 255) * 100

    catch_rate_full_ultra = 100 if catch_rate_full_ultra >= 255 else (catch_rate_full_ultra / 255) * 100
    catch_rate_low_ultra = 100 if catch_rate_low_ultra >= 255 else (catch_rate_low_ultra / 255) * 100

    embed = discord.Embed(title=f'Catch Rate for {monName} at Level {level}',
                          color=[obj for obj in types if obj['Name'] == str(monData['types'][0]['type']['name']).capitalize()][0]['Colour'])
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(dexNum))
    
    embed.set_author(name='Catch Rate Calculator', url='https://www.dragonflycave.com/calculators/gen-v-catch-rate')

    embed.add_field(name='Full Health',
                    value=f'<:Poke_Ball:1190536922779627560> {"{:.2f}".format(catch_rate_full_poke)}%\n<:Great_Ball:1190536962520666123> {"{:.2f}".format(catch_rate_full_great)}%\n<:Ultra_Ball:1190536997794746469> {"{:.2f}".format(catch_rate_full_ultra)}%',
                    inline=True)

    embed.add_field(name='At 1 HP',
                    value=f'<:Poke_Ball:1190536922779627560> {"{:.2f}".format(catch_rate_low_poke)}%\n<:Great_Ball:1190536962520666123> {"{:.2f}".format(catch_rate_low_great)}%\n<:Ultra_Ball:1190536997794746469> {"{:.2f}".format(catch_rate_low_ultra)}%',
                    inline=True)

    return embed
#endregion