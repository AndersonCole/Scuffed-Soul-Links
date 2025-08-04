""" 
Contains the functions for using the soul link bot. 
Usually returns data in a discord embed

Cole Anderson, Dec 2023
"""
import discord
import openai
import requests
import json
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
from functions.shared_functions import *
from dictionaries.shared_dictionaries import sharedFileLocations, sharedImagePaths, types, categories
from dictionaries.soul_link_dictionaries import soulLinksFileLocations, defaultRun, gens, games

openai.api_key = loadDataVariableFromFile(sharedFileLocations.get('ChatGPT'), False)

pokemon = loadDataVariableFromFile(sharedFileLocations.get('Pokemon'))

runs = loadDataVariableFromFile(soulLinksFileLocations.get('Runs'))

currentRun = copy.deepcopy(defaultRun)

#region help command
#dev commands, undo-death {name}, reset, undo-status
async def help():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

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
                                      '```$sl moves Bulbasaur 24``` Shows the four moves the mon has at a specific level\n' +
                                      '```$sl add-nickname Ttar, Tyranitar``` Adds nicknames to link to original names\n' +
                                      '```$sl nicknames``` Prints out all nicknames\n' +
                                      '```$sl catch Bulbasaur 5``` Caclulates the catch rate for the selected gen given the pokemon and level\n' +
                                      '```$sl rare-candies``` Shuckle explains how to aquire rare candies using PKHex\n\n' +
                                      'For Data on forms, type the pokemon\'s name like giratina origin, vulpix alola, charizard mega y, appletun gmax\n' +
                                      'Accessing data for a pokemon\'s default form will always work with their base name',
                          color=3553598)
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://shiny_swole_shuckle.png')
        return embed, shinyFile
    else: 
        embed.set_thumbnail(url='attachment://swole_shuckle.png')
        return embed, file
#endregion

#region text parsing functions
def getMon(dex_num):
    try:
        return [obj for obj in pokemon if obj['DexNum'] == dex_num][0]
    except:
        return None

def getMonFromName(originalName):
    try:
        return [obj for obj in pokemon if obj['Name'] == originalName][0]
    except:
        return None

def getMonName(dex_num):
    try:
        mon = [obj for obj in pokemon if obj['DexNum'] == dex_num][0]['Name']
        return formatTextForDisplay(mon)
    except:
        return None

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

def getRun(run_name):
    try:
        return [obj for obj in runs if obj['Name'] == run_name][0]
    except:
        return None
    
def matchPlayer(player, run):
    try:
        return run['Players'].index(player)
    except:
        return None
    
def checkEncounter(name, run):
    return any(encounter['Name'].lower() == name.lower() for encounter in run['Encounters'])

def tryAddPlayerData(player_string, encounter, player_len):
    if len(encounter) == player_len:
        player_string += 'All Players\n'
    else:
        for player in encounter:
            player_string += f'{player} '
        player_string += '\n'

    if len(player_string) > 1024:
        return False
    return True

def tryAddLinkData(encounter_string, encounter, link_emoji):
    for index, dex_num in enumerate(encounter['Pokemon']):
        mon_name = getMonName(dex_num)
        if mon_name is None:
            mon_name = 'Invalid Name'
        if index == len(encounter['Pokemon']) - 1:
            encounter_string += f'{mon_name}\n'
        else:
            encounter_string += f'{mon_name}{link_emoji}'
    
    if len(encounter_string) > 1024:
        return False
    return True

def tryAddRunData(run, name_string):
    name_string += f'{run["Name"]}\n'

    if len(name_string) > 1024:
        return False
    return True
#endregion

#region $sl new-sl command and createRole func
async def createNewRun(game, name, players):
    versionGroup = getGroup(game)

    if versionGroup is None:
        return 'The name of the game wasn\'t recognized!'
    
    if len(name) > 50:
        return 'Limit the name of the run to less than 50 characters!'
    
    if checkDuplicateName(name):
        return 'The run name has been used before! Use unique names!'

    teamArray = []
    for i in range(15):
        teamArray.append([])

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
        'Teams': teamArray,
        'Run-Notes': ''
    })

    currentRun['VersionGroup'] = versionGroup
    currentRun['RunName'] = name

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return 'Success'

async def createRole(players, guild):
    try:
        run = getRun(currentRun['RunName'])
        
        if run is None:
            raise Exception('Somehow the run name is invalid. Get <@341722760852013066> to look into it lol')

        game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]

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

        await role.edit(color=game_data['Colour'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())])

        for player in players:
            user_id = int(player[2:-1])
            user = guild.get_member(user_id)

            await user.add_roles(role)
    except Exception as ex:
        print(ex)
#endregion

#region $sl encounter command
async def encounterMon(encounter_name, encounter, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    player_index = matchPlayer(player, run)
    dex_num = getDexNum(encounter)

    if player_index is None:
        return f'{player} was not recogized as a player in the currently selected run!'
    
    if dex_num == -1:
        return f'{encounter} was not recognized as a pokemon!'
    
    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid area for an encounter! Make sure to use the \'$sl progress\' command after each major battle to unlock new encounters!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounter_name.lower()][0]

    encounter_data['Pokemon'][player_index] = dex_num

    if all(num != -1 for num in encounter_data['Pokemon']):
        encounter_data['Completed'] = True
    
    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'{encounter} successfully added for {player} for {encounter_name}!'
    
async def encounterMonGroup(encounter_name, encounters):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid area for an encounter! Make sure to use the \'$sl progress\' command after each major battle to unlock new encounters!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounter_name.lower()][0]

    response_string = ''

    for encounter in encounters:
        encounter = re.split(r'[\s]+', encounter.strip())
        if len(encounter) < 2:
            response_string += f'\'{encounter}\' was formatted incorrectly!\n'
            continue
        else:
            player = encounter[0].strip()
            encounter.pop(0)
            encounter = ' '.join(word.capitalize() for word in encounter)

        player_index = matchPlayer(player, run)
        dex_num = getDexNum(encounter)

        if player_index is None:
            response_string += f'{player} was not recogized as a player in the currently selected run!\n'
            continue
    
        if dex_num == -1:
            response_string += f'\'{encounter}\' was not recognized as a pokemon!\n'
            continue

        encounter_data['Pokemon'][player_index] = dex_num

        response_string += f'{encounter} successfully added for {player} for {encounter_name}!\n'
    
    if all(num != -1 for num in encounter_data['Pokemon']):
        encounter_data['Completed'] = True
    
    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return response_string

#endregion

#region $sl encounters command
async def listEncounters():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    embeds = []

    encounter_data = [obj['Name'] for obj in run['Encounters'] if not obj['Completed']]
    player_data = [set(player for i, player in enumerate(run['Players']) if encounter['Pokemon'][i] == -1) for encounter in run['Encounters'] if not encounter['Completed']]
    game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]

    embed = discord.Embed(title=f'{currentRun["RunName"]} Available Encounters',
                          color=game_data['Colour'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())])
    
    if run['Current-Progress'] <= 1 and run['Version-Group'] == 'heartgold-soulsilver':
        embed.set_author(name='Egg Id Website', url='https://www.pokewiki.de/Spezial:Geheimcode-Generator?uselang=en')
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{game_data["Mascot"][[game_name.lower() for game_name in game_data["Games"]].index(run["Game"].lower())]}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{game_data["Mascot"][[game_name.lower() for game_name in game_data["Games"]].index(run["Game"].lower())]}.png')
    
    encounter_string = ''
    player_string = ''

    for encounter, players_encounter in zip(encounter_data, player_data):
        if tryAddPlayerData(player_string, players_encounter, len(run['Players'])):
            encounter_string += f'{encounter}\n'
            if len(players_encounter) == len(run['Players']):
                player_string += 'All Players\n'
            else:
                for player in players_encounter:
                    player_string += f'{player} '
                player_string += '\n'
        else:
            embed.add_field(name='Location',
                    value=encounter_string,
                    inline=True)
    
            embed.add_field(name='Players',
                            value=player_string,
                            inline=True)
            
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            encounter_string = ''
            player_string = ''

            encounter_string += f'{encounter}\n'
            if len(players_encounter) == len(run['Players']):
                player_string += 'All Players\n'
            else:
                for player in players_encounter:
                    player_string += f'{player} '
                player_string += '\n'

    embed.add_field(name='Location',
                    value=encounter_string,
                    inline=True)
    
    embed.add_field(name='Players',
                    value=player_string,
                    inline=True)
    
    embeds.append(embed)
    
    return embeds

#endregion

#region $sl links and link-data command
async def listLinks():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    embeds = []

    encounter_data = [obj for obj in run['Encounters'] if obj['Completed'] and obj['Alive']]
    game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]
    
    player_string = ''
    encounter_string = ''
    link_emoji = game_data['Link-Emoji'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())]

    for player in run['Players']:
        if player == run['Players'][-1]:
            player_string += f'{player}'
        else:
            player_string += f'{player}{link_emoji}'

    embed = discord.Embed(title=f'{currentRun["RunName"]} Active Links',
                          description=player_string,
                          color=game_data['Colour'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())])
    
    for encounter in encounter_data:
        if tryAddLinkData(encounter_string, encounter, link_emoji):
            for index, dex_num in enumerate(encounter['Pokemon']):
                mon_name = getMonName(dex_num)
                if mon_name is None:
                    mon_name = 'Invalid Name'
                if index == len(encounter['Pokemon']) - 1:
                    encounter_string += f'{mon_name}\n'
                else:
                    encounter_string += f'{mon_name}{link_emoji}'
        else:
            embed.add_field(name='',
                            value=encounter_string,
                            inline=True)
            
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            encounter_string = ''
            player_string = ''

            for dex_num in encounter['Pokemon']:
                mon_name = getMonName(dex_num)
                if mon_name is None:
                    mon_name = 'Invalid Name'
                if dex_num == encounter['Pokemon'][-1]:
                    encounter_string += f'{mon_name}\n'
                else:
                    encounter_string += f'{mon_name}{link_emoji}'
    
    embed.add_field(name='',
                    value=encounter_string,
                    inline=True)
    
    embeds.append(embed)
    
    return embeds    

async def getLinkData(input, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]

    player_string = ''
    link_emoji = game_data['Link-Emoji'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())]

    for player_name in run['Players']:
        if player_name == run['Players'][-1]:
            player_string += f'{player_name}'
        else:
            player_string += f'{player_name}{link_emoji}'

    embed = discord.Embed(title=f'Link Data',
                          description=player_string,
                          color=game_data['Colour'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())])

    if checkEncounter(input, run):
        encounter_data = [encounter for encounter in run['Encounters'] if encounter['Name'].lower() == input.lower()][0]
        encounter_string = ''
        for index, dex_num in enumerate(encounter_data['Pokemon']):
            if dex_num == -1:
                mon_name = 'X'
            else:
                mon_name = getMonName(dex_num)
                if mon_name is None:
                    mon_name = 'Invalid Name'
            if index == len(encounter_data['Pokemon']) - 1:
                encounter_string += f'{mon_name}\n'
            else:
                encounter_string += f'{mon_name}{link_emoji}'

        if encounter_data['Alive']:
            status = 'Alive'
        else:
            status = 'Dead'

        embed.add_field(name=f'{encounter_data["Name"]} - {status}',
                        value=encounter_string,
                        inline=True)
        
        return embed
    else:
        dex_num = getDexNum(input)

        if dex_num == -1:
            return f'{input} was not recognized as a valid mon name or as an encounter location!'
        
        player_index = matchPlayer(player, run)

        if player_index is None:
            return 'The author of this input was not recognized as a player in the currently selected run!'
        
        encounter_data = [obj for obj in run['Encounters'] if obj['Pokemon'][player_index] == dex_num]
        
        if len(encounter_data) >= 1:
            encounter_data = encounter_data[0]
        else:
            return f'You do not own a {input}!'

        encounter_string = ''
        for index, dex_num in enumerate(encounter_data['Pokemon']):
            if dex_num == -1:
                mon_name = 'X'
            else:
                mon_name = getMonName(dex_num)
                if mon_name is None:
                    mon_name = 'Invalid Name'
            if index == len(encounter_data['Pokemon']) - 1:
                encounter_string += f'{mon_name}\n'
            else:
                encounter_string += f'{mon_name}{link_emoji}'

        if encounter_data['Alive']:
            status = 'Alive'
        else:
            status = 'Dead'

        embed.add_field(name=f'{encounter_data["Name"]} - {status}',
                        value=encounter_string,
                        inline=True)
        
        return embed
#endregion
    
#region $sl evolve and undo-evolve command
async def evolveMon(mon_name, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    dex_num = getDexNum(mon_name)
    mon = getMon(dex_num)

    if dex_num == -1 or mon is None:
        return f'{mon_name} was not recognized as a valid pokemon!'
    
    player_index = matchPlayer(player, run)

    if player_index is None:
        return 'The author of this input was not recognized as a player in the currently selected run!'
    
    if len(mon['Evolves-Into']) == 0:
        return f'{mon_name} can\'t evolve!'
    

    encounter_data = [obj for obj in run['Encounters'] if obj['Pokemon'][player_index] == dex_num and obj['Completed'] and obj['Alive']]

    if len(encounter_data) >= 1:
        encounter_data = encounter_data[0]
    else:
        return f'You do not own a {mon_name}!'
    
    evo_mon = getMon(mon['Evolves-Into'][0]['DexNum'])

    encounter_data['Pokemon'][player_index] = evo_mon['DexNum']

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'Your {mon_name} from {encounter_data["Name"]} has evolved into a {evo_mon["Name"]}!\nIf this was a mistake, use $sl undo-evolve {evo_mon["Name"]}\nIf this is not the correct evolution, use $sl encounter {encounter_data["Name"]}, evo-name-here'

async def undoEvolveMon(mon_name, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    dex_num = getDexNum(mon_name)
    mon = getMon(dex_num)

    if dex_num == -1 or mon is None:
        return f'{mon_name} was not recognized as a valid pokemon!'
    
    player_index = matchPlayer(player, run)

    if player_index is None:
        return 'The author of this input was not recognized as a player in the currently selected run!'
    
    if mon['Evolves-From'] is None:
        return f'{mon_name} doesn\'t have a pre-evo!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Pokemon'][player_index] == dex_num and obj['Completed'] and obj['Alive']]

    if len(encounter_data) >= 1:
        encounter_data = encounter_data[0]
    else:
        return f'You do not own a {mon_name}!'
    
    pre_evo_mon = getMon(mon['Evolves-From'])

    encounter_data['Pokemon'][player_index] = pre_evo_mon['DexNum']

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'Your {mon_name} from {encounter_data["Name"]} unevolved back into a {pre_evo_mon["Name"]}!'
#endregion

#region $sl death and undo-death command
async def newDeath(encounter_name, reason):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if len(reason) > 500:
        return 'Make the reason for death shorter!'
    
    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid encounter name!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounter_name.lower()][0]
    
    encounter_data['Alive'] = False
    encounter_data['Death-Reason'] = reason

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'The encounter from {encounter_name} has been marked as dead! If this was a mistake, use $sl undo-death {encounter_name}'

async def undoDeath(encounter_name):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid encounter name!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'].lower() == encounter_name.lower()][0]
    
    if encounter_data['Alive']:
        return f'The encounter from {encounter_name} is already alive! Use $sl death {encounter_name} if you wanted to mark the encounter as dead!'

    encounter_data['Alive'] = True
    encounter_data['Death-Reason'] = ''

    await saveDataVariableToFile(soulLinksFileLocations.get('Runs'), runs)

    return f'The encounter from {encounter_name} has been revived!'

#endregion

#region $sl ask-shuckle command
async def askShuckle(user_input):
    rand_num = random.randint(1, 100)
    if rand_num > 90:
        systemContent = loadShucklePersonality('merry')

    else:
        systemContent = loadShucklePersonality('original')
        
    messages = [
        {'role':'system', 'content': systemContent},

        {'role':'user', 'content':user_input}
    ]
    try:
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages = messages, temperature=0.8, max_tokens=500)

        return response.choices[0].message.content[:2000]
    except Exception as ex:
        print(ex)
        return '<@341722760852013066> ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
#endregion

#region $sl deaths command
async def listDeaths():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'

    embeds = []

    encounter_data = [obj for obj in run['Encounters'] if not obj['Alive']]
    game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]

    player_string = ''
    encounter_string = ''
    link_emoji = game_data['Link-Emoji'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())]

    for player in run['Players']:
        if player == run['Players'][-1]:
            player_string += f'{player}'
        else:
            player_string += f'{player}{link_emoji}'

    embed = discord.Embed(title=f'{currentRun["RunName"]} Deaths',
                          description=player_string,
                          color=game_data['Colour'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())])
    
    for encounter in encounter_data:
        encounter_string += f'{encounter["Name"]}\n'
        for index, dex_num in enumerate(encounter['Pokemon']):
            if dex_num == -1:
                mon_name = 'X'
            else:
                mon_name = getMonName(dex_num)
                if mon_name is None:
                    mon_name = 'Invalid Name'
            if index == len(encounter['Pokemon']) - 1:
                encounter_string += f'{mon_name}\n'
            else:
                encounter_string += f'{mon_name}{link_emoji}'

        embed.add_field(name=encounter_string,
                        value=encounter['Death-Reason'],
                        inline=True)
            
        embeds.append(copy.deepcopy(embed))

        embed.clear_fields()
        encounter_string = ''
        player_string = ''
        
    if len(embeds) == 0:
        return 'There are no deaths! Yet...'
    
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
                          color=3553598)
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=sharedImagePaths.get('ShinyShuckle'))
    else: 
        embed.set_thumbnail(url=sharedImagePaths.get('Shuckle'))
    
    name_string = ''
    status_string = ''
    player_string = ''

    for run in runs:
        if tryAddRunData(run, name_string):
            name_string += f'{run["Name"]}\n'
            status_string += f'{run["Run-Status"]}\n'
            player_string += f'{len(run["Players"])}\n'
        else:
            embed.add_field(name='Run Names',
                    value=name_string,
                    inline=True)
    
            embed.add_field(name='Player Count',
                            value=player_string,
                            inline=True)
            
            embed.add_field(name='Status',
                            value=status_string,
                            inline=True)
            
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            name_string = f'{run["Name"]}\n'
            status_string = f'{run["Run-Status"]}\n'
            player_string = f'{len(run["Players"])}\n'

    embed.add_field(name='Run Names',
                    value=name_string,
                    inline=True)
    
    embed.add_field(name='Player Count',
                    value=player_string,
                    inline=True)
    
    embed.add_field(name='Status',
                    value=status_string,
                    inline=True)
    
    embeds.append(embed)
    
    return embeds

#endregion

#region $sl choose-team command
async def chooseTeam(links, player):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    player_index = matchPlayer(player, run)

    if player_index is None:
        return 'The author of this input was not recognized as a player in the currently selected run!'
    
    encounter_data = []

    for link in links:
        temp_link = link
        link = getDexNum(str(link).strip())
        if link is None:
            return f'{temp_link} was not recognized as a valid pokemon name!'
        
        encounter_link = [obj for obj in run['Encounters'] if obj['Pokemon'][player_index] == link]

        if len(encounter_link) > 0: 
            try:
                encounter_data.append([obj for obj in run['Encounters'] if obj['Pokemon'][player_index] == link and obj['Completed'] and obj['Alive']][0])
            except:
                return f'{temp_link} was not paired to a completed or alive link! Some fraud needs to mark their encounters or deaths!'
        else:
            return f'{temp_link} was not recognized as a pokemon you own! Make sure you\'re listing out your pokemon, and not everyone elses pokemon'
    
    run['Teams'][run['Current-Progress']] = encounter_data

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

        for new_encounter in [obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run['Current-Progress']]['Encounters']:
            run['Encounters'].append({
                'Name': new_encounter,
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
async def seeStats():
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    embeds = []

    game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]

    if run['Run-Status'] == 'In Progress':
        description_string = 'This run is currently In Progress!'
    else:
        description_string = f'This run ended in {run["Run-Status"]}!'

    description_string += '\nTo see active and dead links, use the $sl links and $sl deaths commands!'

    player_string = ''
    link_string = ''
    link_emoji = game_data['Link-Emoji'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())]

    for player in run['Players']:
        if player == run['Players'][-1]:
            player_string += f'{player}'
        else:
            player_string += f'{player}{link_emoji}'

    embed = discord.Embed(title=f'{currentRun["RunName"]} Stats',
                          description=f'{description_string}\n{player_string}',
                          color=game_data['Colour'][[game_name.lower() for game_name in game_data['Games']].index(run['Game'].lower())])
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{game_data["Mascot"][[game_name.lower() for game_name in game_data["Games"]].index(run["Game"].lower())]}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{game_data["Mascot"][[game_name.lower() for game_name in game_data["Games"]].index(run["Game"].lower())]}.png')
    
    for progress_index in range(run['Current-Progress'] + 1):
        embed.title = f'{currentRun["RunName"]} Info\nThe Team vs. {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][progress_index]["Battle-Name"]} at Lv. {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][progress_index]["Level-Cap"]}!'
        
        if len(run['Teams'][progress_index]) > 0:
            for encounter in run['Teams'][progress_index]:
                for index, dex_num in enumerate(encounter['Pokemon']):
                    mon_name = getMonName(dex_num)
                    if mon_name is None:
                        mon_name = 'Invalid Name'
                    if index == len(encounter['Pokemon']) - 1:
                        link_string += f'{mon_name}\n'
                    else:
                        link_string += f'{mon_name}{link_emoji}'
        else:
            link_string = 'No team was specified for this battle!'
        
        embed.add_field(name='',
                        value=link_string,
                        inline=True)
        
        embeds.append(copy.deepcopy(embed))

        embed.clear_fields()
        link_string = ''

    embed.title = f'{currentRun["RunName"]} Info\nRun Notes'
    embed.description = description_string

    embed.add_field(name='',
                    value=run['Run-Notes'][:1024],
                    inline=True)
    
    embeds.append(embed)

    return embeds
#endregion 

#region $sl win-run, fail-run, undo-status command
async def setRunStatus(status, guild):
    run = getRun(currentRun['RunName'])

    if run is None:
        return 'Specify a run first!'
    
    if run['Run-Status'] == status:
        return f'The runs status is already {status}!'
    
    all_roles = await guild.fetch_roles()

    try:
        for role in all_roles:
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
async def open_http_image(url, bigImg=True):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        return Image.open(image_data).convert('RGBA')
    if not bigImg:
        return Image.open(f'images/evo_helpers/small_missing_no.png').convert('RGBA')
    return Image.open(f'images/evo_helpers/missing_no.png').convert('RGBA')

async def createArrowImage(direction, type, method, value):
    arrow_img = Image.open(f'images/evo_helpers/arrows/arrow_{type}.png').convert('RGBA')
    if method == 'level-up':
        draw = ImageDraw.Draw(arrow_img)
        font = ImageFont.truetype('fonts/pkmndp.ttf', 10)
        draw.text((10,15), f"Lv. {value}", 'black', font=font)
    elif method == 'trade':
        item_image = Image.open(f'images/evo_helpers/linking-cord.png').convert('RGBA')
        arrow_img.paste(item_image, (10, 4), mask=item_image)
        item_image.close()
    elif method == 'use-item':
        item_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/{value}.png', False)
        arrow_img.paste(item_image, (10, 4), mask=item_image)
        item_image.close()
    elif method == 'happiness':
        item_image = Image.open(f'images/evo_helpers/heart.png').convert('RGBA')
        arrow_img.paste(item_image, (10, 4), mask=item_image)
        item_image.close()
    elif method == 'mega-evo':
        item_image = Image.open(f'images/evo_helpers/mega_evo.png').convert('RGBA')
        arrow_img.paste(item_image, (10, 4), mask=item_image)
        item_image.close()
    
    return arrow_img.rotate(direction)

async def pasteOnImage(backgroundImage, dexNum, positionX, positionY):
    image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dexNum}.png')

    backgroundImage.paste(image, (positionX, positionY), mask=image)
    image.close()

    return backgroundImage

async def pasteArrowImage(backgroundImage, positionX, positionY, direction, type, method, value):
    arrowImage = await createArrowImage(direction, type, method, value)

    backgroundImage.paste(arrowImage, (positionX, positionY), mask=arrowImage)
    arrowImage.close()

    return backgroundImage


async def createEvoChainImage(dex_num, type):
    base_pokemon = [obj for obj in pokemon if obj['DexNum'] == dex_num][0]
                
    while base_pokemon['Evolves-From'] is not None:
        base_pokemon = [obj for obj in pokemon if obj['DexNum'] == base_pokemon['Evolves-From']][0]
    
    evo_chain_max_length = 1
    if len(base_pokemon['Evolves-Into']) > 0:
        evo_chain_max_length = 2
        for evo in base_pokemon['Evolves-Into']:
            evo = [obj for obj in pokemon if obj['DexNum'] == evo['DexNum']][0]
            if len(evo['Evolves-Into']) > 0:
                evo_chain_max_length = 3

    background_image = Image.open(f'images/type_backgrounds/{type}.png')

    if evo_chain_max_length == 1:
        #no evolutions
        background_image = await pasteOnImage(background_image, dex_num, 150, 50)
        
    elif evo_chain_max_length == 2:
        #2 stage evo line, like vulpix
        if len(base_pokemon['Evolves-Into']) == 1:
            #only one evo
            background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 75, 50)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][0]['DexNum'], 225, 50)

            background_image = await pasteArrowImage(background_image, 175, 90, 0, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])

        elif len(base_pokemon['Evolves-Into']) == 2:
            #2 evos, like slowpoke
            background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 100, 50)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][0]['DexNum'], 200, 0)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][1]['DexNum'], 200, 100)

            background_image = await pasteArrowImage(background_image, 175, 55, 45, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])
            background_image = await pasteArrowImage(background_image, 175, 125, -45, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][1]['Value'])

        elif len(base_pokemon['Evolves-Into']) == 3:
            #3 evos, like tyrogue
            background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 100, 50)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][0]['DexNum'], 200, 0)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][1]['DexNum'], 200, 100)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][2]['DexNum'], 275, 50)

            background_image = await pasteArrowImage(background_image, 175, 55, 45, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])
            background_image = await pasteArrowImage(background_image, 175, 125, -45, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][1]['Value'])
            background_image = await pasteArrowImage(background_image, 200, 90, 0, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][2]['Value'])

        elif len(base_pokemon['Evolves-Into']) == 8:
            #eevee
            background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 148, 50)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][0]['DexNum'], 225, 0)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][1]['DexNum'], 225, 100)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][2]['DexNum'], 300, 100)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][3]['DexNum'], 75, 0)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][4]['DexNum'], 75, 100)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][5]['DexNum'], 0, 0)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][6]['DexNum'], 0, 100)
            background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][7]['DexNum'], 300, 0)
            
    elif evo_chain_max_length == 3:
            #3 stage evo line
            if len(base_pokemon['Evolves-Into']) == 1:
                #only one middle evo
                middle_pokemon = [obj for obj in pokemon if obj['DexNum'] == base_pokemon['Evolves-Into'][0]['DexNum']][0]
                if len(middle_pokemon['Evolves-Into']) == 1:
                    #only one final evo, like venusaur
                    background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 0, 50)
                    background_image = await pasteOnImage(background_image, middle_pokemon['DexNum'], 150, 50)
                    background_image = await pasteOnImage(background_image, middle_pokemon['Evolves-Into'][0]['DexNum'], 300, 50)

                    background_image = await pasteArrowImage(background_image, 100, 90, 0, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])
                    background_image = await pasteArrowImage(background_image, 250, 90, 0, type, middle_pokemon['Evolves-Into'][0]['Method'], middle_pokemon['Evolves-Into'][0]['Value'])

                elif len(middle_pokemon['Evolves-Into']) == 2:
                    #two final evos like kirlia
                    background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 0, 50)
                    background_image = await pasteOnImage(background_image, middle_pokemon['DexNum'], 150, 50)
                    background_image = await pasteOnImage(background_image, middle_pokemon['Evolves-Into'][0]['DexNum'], 300, 0)
                    background_image = await pasteOnImage(background_image, middle_pokemon['Evolves-Into'][1]['DexNum'], 300, 100)

                    background_image = await pasteArrowImage(background_image, 100, 90, 0, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])
                    background_image = await pasteArrowImage(background_image, 250, 55, 45, type, middle_pokemon['Evolves-Into'][0]['Method'], middle_pokemon['Evolves-Into'][0]['Value'])
                    background_image = await pasteArrowImage(background_image, 250, 125, -45, type, middle_pokemon['Evolves-Into'][1]['Method'], middle_pokemon['Evolves-Into'][1]['Value'])

            elif len(base_pokemon['Evolves-Into']) == 2:
                #2 middle evos, like mr mime
                middle_pokemon_1 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon['Evolves-Into'][0]['DexNum']][0]
                middle_pokemon_2 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon['Evolves-Into'][1]['DexNum']][0]

                background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 0, 50)
                background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][0]['DexNum'], 150, 0)
                background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][1]['DexNum'], 150, 100)

                background_image = await pasteArrowImage(background_image, 100, 55, 45, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])
                background_image = await pasteArrowImage(background_image, 100, 125, -45, type, base_pokemon['Evolves-Into'][1]['Method'], base_pokemon['Evolves-Into'][1]['Value'])

                if len(middle_pokemon_1['Evolves-Into']) != 0:
                    background_image = await pasteOnImage(background_image, middle_pokemon_1['Evolves-Into'][0]['DexNum'], 300, 0)

                    background_image = await pasteArrowImage(background_image, 250, 55, 0, type, middle_pokemon_1['Evolves-Into'][0]['Method'], middle_pokemon_1['Evolves-Into'][0]['Value'])
                    
                if len(middle_pokemon_2['Evolves-Into']) != 0:
                    background_image = await pasteOnImage(background_image, middle_pokemon_2['Evolves-Into'][0]['DexNum'], 300, 100)

                    background_image = await pasteArrowImage(background_image, 250, 125, 0, type, middle_pokemon_2['Evolves-Into'][0]['Method'], middle_pokemon_2['Evolves-Into'][0]['Value'])

            elif len(base_pokemon['Evolves-Into']) == 3:
                #3 evos with a 3rd stage, like applin
                middle_pokemon_1 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][0]["DexNum"]][0]
                middle_pokemon_2 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][1]["DexNum"]][0]
                middle_pokemon_3 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][2]["DexNum"]][0]

                background_image = await pasteOnImage(background_image, base_pokemon['DexNum'], 0, 50)
                background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][0]['DexNum'], 150, 0)
                background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][1]['DexNum'], 150, 100)
                background_image = await pasteOnImage(background_image, base_pokemon['Evolves-Into'][2]['DexNum'], 200, 50)

                background_image = await pasteArrowImage(background_image, 100, 55, 45, type, base_pokemon['Evolves-Into'][0]['Method'], base_pokemon['Evolves-Into'][0]['Value'])
                background_image = await pasteArrowImage(background_image, 100, 125, -45, type, base_pokemon['Evolves-Into'][1]['Method'], base_pokemon['Evolves-Into'][1]['Value'])
                background_image = await pasteArrowImage(background_image, 125, 90, 0, type, base_pokemon['Evolves-Into'][2]['Method'], base_pokemon['Evolves-Into'][2]['Value'])

                if len(middle_pokemon_1['Evolves-Into']) != 0:
                    background_image = await pasteOnImage(background_image, middle_pokemon_1['Evolves-Into'][0]['DexNum'], 275, 0)

                    background_image = await pasteArrowImage(background_image, 250, 55, 0, type, middle_pokemon_1['Evolves-Into'][0]['Method'], middle_pokemon_1['Evolves-Into'][0]['Value'])
                    
                if len(middle_pokemon_2['Evolves-Into']) != 0:
                    background_image = await pasteOnImage(background_image, middle_pokemon_2['Evolves-Into'][0]['DexNum'], 275, 100)

                    background_image = await pasteArrowImage(background_image, 250, 125, 0, type, middle_pokemon_2['Evolves-Into'][0]['Method'], middle_pokemon_2['Evolves-Into'][0]['Value'])

                if len(middle_pokemon_3['Evolves-Into']) != 0:
                    background_image = await pasteOnImage(background_image, middle_pokemon_3['Evolves-Into'][0]['DexNum'], 315, 50)

                    background_image = await pasteArrowImage(background_image, 275, 90, 0, type, middle_pokemon_3['Evolves-Into'][0]['Method'], middle_pokemon_3['Evolves-Into'][0]['Value'])
    
    image_in_memory = BytesIO()

    background_image.save(image_in_memory, format='PNG')

    background_image.close()

    image_in_memory.seek(0)

    return discord.File(image_in_memory, filename=f'{type}.png')
#endregion

#region $sl dex command

async def makePokedexEmbed(mon):
    dex_num = getDexNum(mon)

    if dex_num == -1:
        return f"The pokemon \'{mon}\' was not recognized!", None
    
    mon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{dex_num}')
    mon_data = mon_data.json()

    mon_name = re.split(r'[\s-.]+', mon_data['name'])
    mon_name = ' '.join(word.capitalize() for word in mon_name)

    mon_primary_type = ''
    mon_secondary_type = ''

    if len(mon_data['types']) == 2:
        mon_primary_type = str(mon_data['types'][0]['type']['name']).capitalize()
        mon_secondary_type = str(mon_data['types'][1]['type']['name']).capitalize()
    else:
        mon_primary_type = str(mon_data['types'][0]['type']['name']).capitalize()
        mon_secondary_type = ''

    type_emojis = [obj for obj in types if obj["Name"] == mon_primary_type][0]["Emoji"]
    if mon_secondary_type != '':
        type_emojis += [obj for obj in types if obj["Name"] == mon_secondary_type.capitalize()][0]["Emoji"]
    
    moveset, versionGroup = await getMoves(mon_data['moves'], currentRun['VersionGroup'])

    moveset_levels, moveset_names, moveset_types_categories = movesetText(moveset)

    if len(moveset_types_categories) > 1024:
        index = moveset_types_categories.rfind(' ', 0 , 1024)

        moveset_types_categories = moveset_types_categories[:index]

    version_group_name = re.split(r'[\s-.]+', versionGroup)
    version_group_name = ' '.join(word.capitalize() for word in version_group_name)

    file = await createEvoChainImage(dex_num, mon_primary_type)

    embed = discord.Embed(title=f'#{mon_data["species"]["url"][42:].strip("/")} {mon_name} {type_emojis}',
                          color=[obj for obj in types if obj['Name'] == mon_primary_type][0]['Colour'])

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{dex_num}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_num}.png')

    embed.set_author(name='Pokémon Data', url=f'https://www.serebii.net/pokedex{[obj for obj in gens if any(group["Name"] == versionGroup for group in obj["Version-Groups"])][0]["Serebii-Link"]}/{str(mon_data["species"]["url"][42:].strip("/")).zfill(3)}.shtml')

    embed.add_field(name=f'Stats - {int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "attack"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "defense"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "speed"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-attack"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-defense"][0]["base_stat"])} BST',
                    value=f'HP - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"]}\nAtk - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "attack"][0]["base_stat"]}\nDef - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "defense"][0]["base_stat"]}',
                    inline=True)
    
    embed.add_field(name=f'᲼',
                    value=f'Spd - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "speed"][0]["base_stat"]}\nSp.Atk - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-attack"][0]["base_stat"]}\nSp.Def - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-defense"][0]["base_stat"]}',
                    inline=True)

    embed.add_field(name=f'Moveset Data from {version_group_name}',
                    value='',
                    inline=False)
    
    embed.add_field(name='Level',
                    value=moveset_levels,
                    inline=True)
    
    embed.add_field(name='Name',
                    value=moveset_names,
                    inline=True)
    
    embed.add_field(name='Type ᲼ Cat.',
                    value=moveset_types_categories,
                    inline=True)

    embed.set_image(url=f"attachment://{mon_primary_type}.png")

    return embed, file
#endregion

#region $sl moves command
async def getMoves(moves, versionGroup):
    if versionGroup == '':
        versionGroup = moves[random.randint(0, len(moves) - 1)]['version_group_details'][0]['version_group']['name']
    
    moveset = []

    for move in moves:
        for version in move['version_group_details']:
            if version['version_group']['name'] == versionGroup:
                name = move['move']['name']
                words = re.split(r'[\s-.]+', name)
                name = ' '.join(word.capitalize() for word in words)
                moveset.append({'Name': name, 'Level': version['level_learned_at'], 'Method': version['move_learn_method']['name'], 'URL': move['move']['url']})
    
    moveset = [obj for obj in moveset if obj["Method"] == "level-up"]

    moveset.sort(reverse=False, key=lambda item: item['Level'])

    async with aiohttp.ClientSession() as session:
        tasks = [fetchMoveDetails(asyncio.Semaphore(15), session, move['URL']) for move in moveset]
        moveDataResponses = await asyncio.gather(*tasks)

    for move, response in zip(moveset, moveDataResponses):
        move["Type"] = str(response['type']['name']).capitalize()
        move["Category"] = str(response['damage_class']['name']).capitalize()
        move["Power"] = '᲼\-᲼' if response['power'] is None else str(response['power']).rjust(3, '᲼')
        move["Accuracy"] = '᲼\-' if response['accuracy'] is None else str(response['accuracy']).rjust(3, '᲼')

    if not moveset and moves:
        return await getMoves(moves, moves[random.randint(0, len(moves) - 1)]['version_group_details'][0]['version_group']['name'])

    return moveset, versionGroup

async def fetchMoveDetails(semaphores, session, url):
    async with semaphores:
        async with session.get(url) as response:
            return await response.json()
        
def movesetText(moveset):
    level_text = ''
    move_name_text = ''
    move_type_category_text = ''

    for move in moveset:
        level_text += f'{move["Level"]}\n'
        move_name_text += f'{move["Name"]}\n'
        move_type_category_text += f'᲼{[obj for obj in types if obj["Name"] == move["Type"]][0]["Emoji"]} ᲼᲼ {[obj for obj in categories if obj["Name"] == move["Category"]][0]["Emoji"]}\n'

    return level_text, move_name_text, move_type_category_text

def movesetTextLevel(moveset, level):
    move_name_text = ''
    move_type_category_text = ''
    move_power_accuracy_text = ''
    comment = ''

    temp_moveset = []
    for move in moveset:
        if move['Level'] > level:
            break
        elif move['Name'] in [temp_move['Name'] for temp_move in temp_moveset]:
            continue
        temp_moveset.append(move)
        if len(temp_moveset) > 4:
            temp_moveset.pop(0)
    moveset = temp_moveset


    for move in moveset:
        if move['Level'] <= 1:
            comment = 'This moveset contains level 1 moves!\nDouble check the moveset with $sl dex or Serebii!'
        move_name_text += f'{move["Name"]}\n'
        move_type_category_text += f'᲼{[obj for obj in types if obj["Name"] == move["Type"]][0]["Emoji"]} ᲼᲼ {[obj for obj in categories if obj["Name"] == move["Category"]][0]["Emoji"]}\n'
        move_power_accuracy_text += f'{move["Power"]}᲼᲼{"   " if move["Power"] == "᲼-᲼" and move["Accuracy"] == "100" else ""}{move["Accuracy"]}\n'

    return move_name_text, move_type_category_text, move_power_accuracy_text, comment

async def showMoveSet(mon, level):
    if not level.isnumeric() or int(level) > 100 or int(level) < 0:
        return f"Input invalid! Specify the pokemon\'s name and it's level! ```$sl moves Bulbasaur 24```"
    
    level = int(level)

    dex_num = getDexNum(mon)

    if dex_num == -1:
        return f"The pokemon \'{mon}\' was not recognized!"
    
    mon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{dex_num}')
    mon_data = mon_data.json()

    mon_name = re.split(r'[\s-.]+', mon_data['name'])
    mon_name = ' '.join(word.capitalize() for word in mon_name)

    moveset, versionGroup = await getMoves(mon_data['moves'], currentRun['VersionGroup'])

    moveset_names, moveset_types_categories, moveset_power_accuracy, comment = movesetTextLevel(moveset, level)

    version_group_name = re.split(r'[\s-.]+', versionGroup)
    version_group_name = ' '.join(word.capitalize() for word in version_group_name)

    embed = discord.Embed(title=f'Level {level} {mon_name}',
                          description=comment,
                          color=[obj for obj in types if obj['Name'] == str(mon_data['types'][0]['type']['name']).capitalize()][0]['Colour'])
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{dex_num}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_num}.png')
    
    embed.set_author(name='Moveset Data', url=f'https://www.serebii.net/pokedex{[obj for obj in gens if any(group["Name"] == versionGroup for group in obj["Version-Groups"])][0]["Serebii-Link"]}/{str(mon_data["species"]["url"][42:].strip("/")).zfill(3)}.shtml')

    embed.add_field(name=f'31 IVs, 0 EVs, Neutral',
                    value=f'HP - {calculateHP(int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"]), level)}\nAtk - {calculateStat(int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "attack"][0]["base_stat"]), level)}\nDef - {calculateStat(int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "defense"][0]["base_stat"]), level)}',
                    inline=True)
    
    embed.add_field(name=f'{int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "attack"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "defense"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "speed"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-attack"][0]["base_stat"]) + int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-defense"][0]["base_stat"])} BST',
                    value=f'Spd - {calculateStat(int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "speed"][0]["base_stat"]), level)}\nSp.Atk - {calculateStat(int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-attack"][0]["base_stat"]), level)}\nSp.Def - {calculateStat(int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "special-defense"][0]["base_stat"]), level)}',
                    inline=True)
    
    embed.add_field(name=f'Moveset Data from {version_group_name}',
                    value='',
                    inline=False)
    
    embed.add_field(name='Name',
                    value=moveset_names,
                    inline=True)
    
    embed.add_field(name='Type ᲼ Cat.',
                    value=moveset_types_categories,
                    inline=True)
    
    embed.add_field(name='Pwr ᲼ Acc',
                    value=moveset_power_accuracy,
                    inline=True)
    
    return embed

def calculateHP(base_stat, level):
    if base_stat == 1:
        hp_stat = 1
    else:
        hp_stat = math.floor(((2 * base_stat + 31) * level)/100) + level + 10

    return hp_stat

def calculateStat(base_stat, level):
    stat = math.floor(((2 * base_stat + 31) * level)/100) + 5

    return stat

#endregion

#endregion

#region $sl rare-candies command
async def makeRareCandiesEmbed():
    embeds = []

    embed = discord.Embed(title=f'Rare Candy Instructions',
                          description='',
                          color=7441607)
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=sharedImagePaths.get('ShinyShuckle'))
    else: 
        embed.set_thumbnail(url=sharedImagePaths.get('Shuckle'))
    
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
                            'First you\'ll want to make sure you\'ve saved your game at least once, then go ahead and right-click on the game you\'re playing in Citra. Click on the \'Open Save Data Location\' option. That\'s the file you want to open in PKHex. Copy the path to that file.\n\n' +
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

    dex_num = getDexNum(mon)

    if dex_num == -1:
        return f"The pokemon \'{mon}\' was not recognized!"
    
    mon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{dex_num}')
    mon_data = mon_data.json()

    mon_species = requests.get(mon_data['species']['url'])
    mon_species = mon_species.json()

    mon_name = re.split(r'[\s-.]+', mon_data['name'])
    mon_name = ' '.join(word.capitalize() for word in mon_name)

    capture_rate = mon_species['capture_rate']

    gen = [obj for obj in gens if any(group["Name"] == currentRun["VersionGroup"] for group in obj["Version-Groups"])][0]

    if dex_num == 292:
        hp_stat = 1
    else:
        hp_stat = math.floor((((2 * int([obj for obj in mon_data["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"])) + random.randint(0, 31)) * level)/100) + level + 10

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

    embed = discord.Embed(title=f'Catch Rate for {mon_name} at Level {level}',
                          color=[obj for obj in types if obj['Name'] == str(mon_data['types'][0]['type']['name']).capitalize()][0]['Colour'])
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{dex_num}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_num}.png')
    
    embed.set_author(name='Catch Rate Calculator', url='https://www.dragonflycave.com/calculators/gen-v-catch-rate')

    embed.add_field(name='Full Health',
                    value=f'<:Poke_Ball:1190536922779627560> {"{:.2f}".format(catch_rate_full_poke)}%\n<:Great_Ball:1190536962520666123> {"{:.2f}".format(catch_rate_full_great)}%\n<:Ultra_Ball:1190536997794746469> {"{:.2f}".format(catch_rate_full_ultra)}%',
                    inline=True)

    embed.add_field(name='At 1 HP',
                    value=f'<:Poke_Ball:1190536922779627560> {"{:.2f}".format(catch_rate_low_poke)}%\n<:Great_Ball:1190536962520666123> {"{:.2f}".format(catch_rate_low_great)}%\n<:Ultra_Ball:1190536997794746469> {"{:.2f}".format(catch_rate_low_ultra)}%',
                    inline=True)

    return embed
#endregion

#region nicknames
#region $sl add-nickname command
async def addNickname(nickname, originalName):
    global pokemon
    originalName = re.sub(r'\s', '-', str(originalName).lower().strip())
    mon = getMonFromName(originalName)

    if mon is None:
        return f'\'{originalName}\' is not a valid mon!'

    pokemon.append({
        'Name': re.sub(r'\s', '-', str(nickname).lower().strip()),
        'DexNum': mon['DexNum'],
        'Nickname': True,
        'Evolves-Into': mon['Evolves-Into'],
        'Evolves-From': mon['Evolves-From']
    })

    await saveDataVariableToFile(sharedFileLocations.get('Pokemon'), pokemon)

    return f'Nickname \'{nickname}\' successfully added for {mon["Name"]}'

#endregion
        
#region $sl nicknames command
async def seeNicknames():
    nicknames = [obj for obj in pokemon if obj['Nickname'] is True]

    original_names = ''
    nick_names = ''
    
    for mon in nicknames:
        original_names += f'{[obj for obj in pokemon if obj["DexNum"] == mon["DexNum"]][0]["Name"]}\n'
        nick_names += f'{mon["Name"]}\n'
    
    embed = discord.Embed(title='Scuffed Soul Links Nicknames', 
                          color=3553598)
    
    embed.add_field(name='Nicknames',
                    value=nick_names,
                    inline=True)
    
    embed.add_field(name='Original',
                    value=original_names,
                    inline=True)
    
    return embed

#endregion
        
#endregion