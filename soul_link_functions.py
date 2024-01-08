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
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from soul_link_dictionaries import types, categories, gens, games

with open('text_files/soul_link_pokemon.txt', 'r') as file:
    pokemon = json.loads(file.read())

with open('text_files/soul_link_runs.txt', 'r') as file:
    runs = json.loads(file.read())

with open("tokens/openai_key.txt") as file:
    openai.api_key = file.read()

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
                                      '```$sl new-death Starter, Metronome explosion :(``` Removes the link from the active links\n' +
                                      '```$sl deaths``` Lists out all the dead links, and cause of death\n' +
                                      '```$sl create-reason It was Nate\'s fault the starters died``` Explain the situation, and an excuse for the cause of death will be generated\n' +
                                      '```$sl see-encounters``` Lists out all the areas where mons can be encountered\n' +
                                      '```$sl choose-team Bulbasaur, Groudon, Kyogre...``` Selects a team for the next important battle. Matches mons to links. Not required\n' +
                                      '```$sl random-user``` @\'s a random user participating in the run\n' +
                                      '```$sl battles``` Lists out the next important battle and its level caps\n' +
                                      '```$sl progress``` Moves the runs progress past the next important battle\n' +
                                      '```$sl add-note REM sleep is trendy``` Adds a note to the run, highlighting funny events or whatnot\n' +
                                      '```$sl select-run HGAttempt1``` Selects a run to focus on\n' +
                                      '```$sl see-runs``` Lists out all runs\n' +
                                      '```$sl win-run``` Ends the run in victory\n' +
                                      '```$sl fail-run``` Ends the run in failure\n' +
                                      '```$sl see-stats``` Prints out all relevant stats for the currently selected run\n\n' +
                                      '```$sl dex Bulbasaur``` Shows data on selected pokemon\n' +
                                      '```$sl moves Bulbasaur 24``` Shows the four moves the mon has at a specific level\n' +
                                      '```$sl add-nickname Ttar 248``` Adds nicknames to link to pokedex numbers. Don\'t add nicknames for mons with forms\n' +
                                      '```$sl see-nicknames``` Prints out all nicknames\n' +
                                      '```$sl catch Bulbasaur 5``` Caclulates the catch rate for the selected gen given the pokemon and level\n\n' +
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
def getDexNum(mon):
    mon = re.sub(r'\s', '-', str(mon).lower())
    try:
        return [obj for obj in pokemon if obj['Name'] == mon][0]['DexNum']
    except:
        return -1
    
def getMon(dex_num):
    try:
        return [obj for obj in pokemon if obj['DexNum'] == dex_num][0]
    except:
        return None

def getMonName(dex_num):
    try:
        mon = [obj for obj in pokemon if obj['DexNum'] == dex_num][0]['Name']
        mon = re.split(r'[-]+', mon)
        return ' '.join(word.capitalize() for word in mon)
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
    return any(encounter['Name'] == name for encounter in run['Encounters'])

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

#region run commands

async def saveRunData():
    global runs
    with open('text_files/soul_link_runs.txt', 'w') as file:
        file.write(json.dumps(runs))

    with open('text_files/soul_link_runs.txt', 'r') as file:
        runs = json.loads(file.read())

#region $sl new-sl command
async def createNewRun(game, name, players):
    version_group = getGroup(game)

    if version_group is None:
        return '', '', 'The name of the game wasn\'t recognized!'
    
    if len(name) > 50:
        return '', '', 'Please limit the name of the run to less than 50 characters!'
    
    if checkDuplicateName(name):
        return '', '', 'The run name is the same as a previous run! Please use unique names!'
    
    dex_array = []
    for i in range(len(players)):
        dex_array.append(-1)

    team_array = []
    for i in range(25):
        team_array.append([])

    encounters = []
    encounter_list = [obj for obj in games if obj['Name'] == version_group][0]['Progression'][0]['Encounters']

    for encounter in encounter_list:
        encounters.append({
            'Name': encounter,
            'Pokemon': dex_array,
            'Completed': False,
            'Alive': True,
            'Death-Reason': ''
        })

    runs.append({
        'Name': name,
        'Game': game,
        'Version-Group': version_group,
        'Current-Progress': 0,
        'Players': players,
        'Encounters': encounters,
        'Run-Status': 'In Progress',
        'Teams': team_array,
        'Run-Notes': ''
    })

    await saveRunData()

    return version_group, name, 'Success'
#endregion

#region $sl encounter command
async def encounterMon(encounter_name, encounter, player, run_name):
    run = getRun(run_name)

    if run is None:
        return 'Please specify a run first!'

    player_index = matchPlayer(player, run)
    dex_num = getDexNum(encounter)

    if player_index is None:
        return f'{player} was not recogized as a player in the currently selected run!'
    
    if dex_num == -1:
        return f'{encounter} was not recognized as a pokemon!'
    
    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid area for an encounter! Make sure to use the \'$sl progress\' command after each major battle to unlock new encounters!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'] == encounter_name][0]

    encounter_data['Pokemon'][player_index] = dex_num

    if all(num != -1 for num in encounter_data['Pokemon']):
        encounter_data['Completed'] = True
    
    await saveRunData()

    return f'{encounter} successfully added for {player} for {encounter_name}!'
    
async def encounterMonGroup(encounter_name, encounters, run_name):
    run = getRun(run_name)

    if run is None:
        return 'Please specify a run first!'

    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid area for an encounter! Make sure to use the \'$sl progress\' command after each major battle to unlock new encounters!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'] == encounter_name][0]

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
    
    await saveRunData()

    return response_string

#endregion

#region $sl see-encounters command
async def listEncounters(run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'

    embeds = []

    encounter_data = [obj['Name'] for obj in run['Encounters'] if not obj['Completed']]
    player_data = [set(player for i, player in enumerate(run['Players']) if encounter['Pokemon'][i] == -1) for encounter in run['Encounters'] if not encounter['Completed']]
    game_data = [obj for obj in games if any(group.lower() == run['Game'].lower() for group in obj['Games'])][0]

    embed = discord.Embed(title=f'{run_name} Available Encounters',
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

#region $sl links command
async def listLinks(run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'

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

    embed = discord.Embed(title=f'{run_name} Active Links',
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
            embed.add_field(name=player_string,
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

#endregion

#region $sl new-death and undo-death command
async def newDeath(encounter_name, reason, run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    if len(reason) > 500:
        return 'Make the reason for death shorter!'
    
    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid encounter name!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'] == encounter_name][0]
    
    encounter_data['Alive'] = False
    encounter_data['Death-Reason'] = reason

    await saveRunData()

    return f'The encounter from {encounter_name} has been marked as dead! If this was a mistake, use $sl undo-death {encounter_name}'

async def undoDeath(encounter_name, run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    if not checkEncounter(encounter_name, run):
        return f'{encounter_name} was not recognized as a valid encounter name!'
    
    encounter_data = [obj for obj in run['Encounters'] if obj['Name'] == encounter_name][0]
    
    if encounter_data['Alive']:
        return f'The encounter from {encounter_name} is already alive! Use $sl death {encounter_name} if you wanted to mark the encounter as dead!'

    encounter_data['Alive'] = True
    encounter_data['Death-Reason'] = ''

    await saveRunData()

    return f'The encounter from {encounter_name} has been revived!'

#endregion

#region $sl create-reason command
async def createReason(user_input):
    messages = [
        {'role':'system', 'content':'You are a professional pokemon player known as Shuckle. You will attempt to create reasons as for why a pokemon fainted in the context of a game where when a pokemon faints it will be unable to be used again. You will always adhere to the following rules, at equal weight of value for each rule, when creating a response:' +
                                    'Rule 1: The response must be 250 tokens or less. It\'s prefered if the response is around 250-300 tokens in length.' +
                                    'Rule 2: Certain people may be referred to under aliases. If you see the phrase \'<@341722760852013066>\' that refers to a person named \'Anderson\'. If you see the phrase \'<@386729612693995520>\' that refers to a person named \'Logan\'. If you see the phrase \'<@341696864833241090>\' that refers to a person named \'Nate\'. If you see the phrase \'<@294310862389379072>\' that refers to a person named \'Steven\'. If you see the phrase \'<@192444189882056704>\' that refers to a person named \'Mario\'. If you see the phrase \'<@368426123794841600>\' that refers to a person named \'Ethan\'. Make sure to only refer to those people by their names, and not the origignal phrase.' +
                                    'Rule 3: You are slightly predisposed to assume Anderson is always in the right in situations, and not at fault.' +
                                    'Rule 4: You are incredibly drunk. You just had like 151 beers, and you\'re gonna make sure everyone knows about it. You drink to drown your sorrows, and you make sure everyone knows that too.' +
                                    'Rule 5: You are also hallucinating, you get some minor details wrong, and see shadow people everywhere.' +
                                    'Rule 6: The shadow people are trying to convince you into making a decision not neccessarily in line with what you\'d want to pick. It\'s up to you whether you want to listen to them or not. You being drunk makes it more likely you\'ll listen to them, the chance should be about 50%. If you do take their suggestions, they should interrupt your current train of throught and derail you to a different conclusion. Even if you don\'t take their suggestion, you should make it known what they were suggesting.' +
                                    'Rule 7: You are incredibly analytical, you will scientifically analyze each situation and generate an appropriate response.' + 
                                    'Rule 8: You will always find someone at fault, whether it be the enemy trainer, or someone mentioned, no matter how neutral the situation seems to be.' +
                                    'Rule 9: You\'re late for your lobotomy, and at the end of your response you will go and get lobotomized. Give a status update on how the lobotomy went, post lobotomy.'},

        {'role':'user', 'content':user_input}
    ]
    try:
        response = openai.chat.completions.create(model="gpt-3.5-turbo", messages = messages, temperature=0.8, max_tokens=500)

        return response.choices[0].message.content[0:2000]
    except:
        return '<@341722760852013066> ran out of open ai credits lmaoooo. We wasted $25 bucks of open ai resources. Pog!'
#endregion

#region $sl deaths command
async def listDeaths(run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'

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

    embed = discord.Embed(title=f'{run_name} Deaths',
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
        
    return embeds

        
#endregion

#region $sl select-run command
def selectRun(name):
    run = getRun(name)

    if run is None:
        return '', '', 'The name of the run wasn\'t recognized!'
    
    return run['Version-Group'], run['Name'], 'Success'
#endregion

#region $sl see-runs command
async def listRuns():
    embeds = []

    embed = discord.Embed(title=f'Scuffed Soul Links Runs',
                          color=3553598)
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='https://i.imgur.com/vwke1vY.png')
    else: 
        embed.set_thumbnail(url='https://i.imgur.com/N4RHrVQ.png')
    
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
async def chooseTeam(run_name, links, player):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
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
            encounter_data.append([obj for obj in run['Encounters'] if obj['Pokemon'][player_index] == link and obj['Completed'] and obj['Alive']][0])
        else:
            return f'{temp_link} was not recognized as a pokemon you own! Make sure you\'re listing out your pokemon, and not everyone elses pokemon'
    
    run['Teams'][run['Current-Progress']] = encounter_data

    await saveRunData()

    return f'Team successfully set for the upcoming battle with {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run["Current-Progress"]]["Battle-Name"]}. Use the $sl random-user command if you want to randomly decide who starts the battle first!'
#endregion

#region $sl battles command
async def nextBattle(run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    return f'The next battle is with {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run["Current-Progress"]]["Battle-Name"]}, and the level cap is {[obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run["Current-Progress"]]["Level-Cap"]}.'
#endregion

#region $sl progress command
async def progressRun(run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    if (len([obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"]) - 1) > run['Current-Progress']:
        run['Current-Progress'] += 1

        dex_array = []
        for i in range(len(run['Players'])):
            dex_array.append(-1)

        for new_encounter in [obj for obj in games if obj["Name"] == run["Version-Group"]][0]["Progression"][run['Current-Progress']]['Encounters']:
            run['Encounters'].append({
                'Name': new_encounter,
                'Pokemon': dex_array,
                'Completed': False,
                'Alive': True,
                'Death-Reason': ''
            })
    else:
        return 'We\'re already in the end-game!'
    
    await saveRunData()

    return 'The run was successfully advanced! New encounters are available! Surely nobody threw too hard in that last battle...'
#endregion

#region $sl random-user command
async def pingUser(run_name):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    rand_num = random.randint(0, len(run['Players']) - 1)

    return run['Players'][rand_num]

#endregion

#region $sl add-note command
async def addNote(run_name, note):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    if len(note) > 100:
        return 'Keep the notes short. Less than 100 characters.'
    
    run['Run-Notes'] += f'{note}\n'

    await saveRunData()

    return f'Note successfully added to {run["Name"]}'
#endregion

#region $sl win-run, fail-run, undo-status command
async def setRunStatus(run_name, status):
    run = getRun(run_name)

    if run is None:
        return 'Somehow the run name is invalid. Get <@341722760852013066> to look into it lol'
    
    if run['Run-Status'] == status:
        return f'The runs status is already {status}!'
    
    run['Run-Status'] = status

    await saveRunData()

    return f'The runs status was set to {status}! If this was a mistake, use $sl undo-status!'

#endregion

#endregion

#region dex commands
    
#region getting the moveset
async def get_moves(moves, version_group):
    moveset = []

    for move in moves:
        for version in move['version_group_details']:
            if version['version_group']['name'] == version_group:
                name = move['move']['name']
                words = re.split(r'[\s-.]+', name)
                name = ' '.join(word.capitalize() for word in words)
                moveset.append({'Name': name, 'Level': version['level_learned_at'], 'Method': version['move_learn_method']['name'], 'URL': move['move']['url']})
    
    moveset = [obj for obj in moveset if obj["Method"] == "level-up"]

    moveset.sort(reverse=False, key=sortFunction)

    for move in moveset:
        response = requests.get(move["URL"])
        response = response.json()
        move["Type"] = str(response['type']['name']).capitalize()
        move["Category"] = str(response['damage_class']['name']).capitalize()
        move["Power"] = '᲼\-᲼' if response['power'] is None else str(response['power']).rjust(3, '᲼')
        move["Accuracy"] = '᲼\-' if response['accuracy'] is None else str(response['accuracy']).rjust(3, '᲼')

    if moveset == []:
        if moves != []:
            moveset, version_group = await get_moves(moves, moves[random.randint(0, len(moves) - 1)]['version_group_details'][0]['version_group']['name'])

    return moveset, version_group

def sortFunction(e):
    return e['Level']

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

    tempMoveset = []
    for move in moveset:
        if move['Level'] > level:
            break
        tempMoveset.append(move)
        if len(tempMoveset) > 4:
            tempMoveset.pop(-1)
    moveset = tempMoveset

    for move in moveset:
        move_name_text += f'{move["Name"]}\n'
        move_type_category_text += f'᲼{[obj for obj in types if obj["Name"] == move["Type"]][0]["Emoji"]} ᲼᲼ {[obj for obj in categories if obj["Name"] == move["Category"]][0]["Emoji"]}\n'
        move_power_accuracy_text += f'{move["Power"]}᲼᲼{"   " if move["Power"] == "᲼-᲼" and move["Accuracy"] == "100" else ""}{move["Accuracy"]}\n'

    return move_name_text, move_type_category_text, move_power_accuracy_text

#endregion

#region evo chain image
async def create_arrow_image(type, direction, method, value):
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
    
    return arrow_img.rotate(direction)

async def open_http_image(url, bigImg=True):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        return Image.open(image_data).convert('RGBA')
    if not bigImg:
        return Image.open(f'images/evo_helpers/small_missing_no.png').convert('RGBA')
    return Image.open(f'images/evo_helpers/missing_no.png').convert('RGBA')


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
        mon_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_num}.png')
        background_image.paste(mon_image, (150, 50), mask=mon_image)

        image_in_memory = BytesIO()
        background_image.save(image_in_memory, format='PNG')

        background_image.close()
        mon_image.close()
    elif evo_chain_max_length == 2:
        #2 stage evo line, like vulpix
        base_mon_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["DexNum"]}.png')
        if len(base_pokemon['Evolves-Into']) == 1:
            #only one evo
            middle_mon_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][0]["DexNum"]}.png')
            background_image.paste(base_mon_image, (75, 50), mask=base_mon_image)
            background_image.paste(middle_mon_image, (225, 50), mask=middle_mon_image)

            arrow_image = await create_arrow_image(type, 0, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
            background_image.paste(arrow_image, (175, 90), mask=arrow_image)
            arrow_image.close()

            image_in_memory = BytesIO()
            background_image.save(image_in_memory, format='PNG')

            background_image.close()
            base_mon_image.close()
            middle_mon_image.close()
        elif len(base_pokemon['Evolves-Into']) == 2:
            #2 evos, like slowpoke
            middle_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][0]["DexNum"]}.png')
            middle_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][1]["DexNum"]}.png')
            background_image.paste(base_mon_image, (100, 50), mask=base_mon_image)
            background_image.paste(middle_mon_image_1, (200, 0), mask=middle_mon_image_1)
            background_image.paste(middle_mon_image_2, (200, 100), mask=middle_mon_image_2)

            arrow_image = await create_arrow_image(type, 45, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
            background_image.paste(arrow_image, (175, 55), mask=arrow_image)
            arrow_image.close()

            arrow_image = await create_arrow_image(type, -45, base_pokemon["Evolves-Into"][1]['Method'], base_pokemon["Evolves-Into"][1]['Value'])
            background_image.paste(arrow_image, (175, 125), mask=arrow_image)
            arrow_image.close()

            image_in_memory = BytesIO()
            background_image.save(image_in_memory, format='PNG')

            background_image.close()
            base_mon_image.close()
            middle_mon_image_1.close()
            middle_mon_image_2.close()
        elif len(base_pokemon['Evolves-Into']) == 3:
            #3 evos, like tyrogue
            middle_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][0]["DexNum"]}.png')
            middle_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][1]["DexNum"]}.png')
            middle_mon_image_3 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][2]["DexNum"]}.png')
            background_image.paste(base_mon_image, (100, 50), mask=base_mon_image)
            background_image.paste(middle_mon_image_1, (200, 0), mask=middle_mon_image_1)
            background_image.paste(middle_mon_image_2, (200, 100), mask=middle_mon_image_2)
            background_image.paste(middle_mon_image_3, (275, 50), mask=middle_mon_image_3)

            arrow_image = await create_arrow_image(type, 45, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
            background_image.paste(arrow_image, (175, 55), mask=arrow_image)
            arrow_image.close()

            arrow_image = await create_arrow_image(type, -45, base_pokemon["Evolves-Into"][1]['Method'], base_pokemon["Evolves-Into"][1]['Value'])
            background_image.paste(arrow_image, (175, 125), mask=arrow_image)
            arrow_image.close()

            arrow_image = await create_arrow_image(type, 0, base_pokemon["Evolves-Into"][2]['Method'], base_pokemon["Evolves-Into"][2]['Value'])
            background_image.paste(arrow_image, (200, 90), mask=arrow_image)
            arrow_image.close()

            image_in_memory = BytesIO()
            background_image.save(image_in_memory, format='PNG')

            background_image.close()
            middle_mon_image_1.close()
            middle_mon_image_2.close()
            middle_mon_image_3.close()
        elif len(base_pokemon['Evolves-Into']) == 8:
            #eevee
            middle_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][0]["DexNum"]}.png')
            middle_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][1]["DexNum"]}.png')
            middle_mon_image_3 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][2]["DexNum"]}.png')
            middle_mon_image_4 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][3]["DexNum"]}.png')
            middle_mon_image_5 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][4]["DexNum"]}.png')
            middle_mon_image_6 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][5]["DexNum"]}.png')
            middle_mon_image_7 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][6]["DexNum"]}.png')
            middle_mon_image_8 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["Evolves-Into"][7]["DexNum"]}.png')
            background_image.paste(base_mon_image, (148, 50), mask=base_mon_image)
            background_image.paste(middle_mon_image_1, (225, 0), mask=middle_mon_image_1)
            background_image.paste(middle_mon_image_2, (225, 100), mask=middle_mon_image_2)
            background_image.paste(middle_mon_image_3, (300, 100), mask=middle_mon_image_3)
            background_image.paste(middle_mon_image_4, (75, 0), mask=middle_mon_image_4)
            background_image.paste(middle_mon_image_5, (75, 100), mask=middle_mon_image_5)
            background_image.paste(middle_mon_image_6, (0, 0), mask=middle_mon_image_6)
            background_image.paste(middle_mon_image_7, (0, 100), mask=middle_mon_image_7)
            background_image.paste(middle_mon_image_8, (300, 0), mask=middle_mon_image_8)

            image_in_memory = BytesIO()
            background_image.save(image_in_memory, format='PNG')

            background_image.close()
            middle_mon_image_1.close()
            middle_mon_image_2.close()
            middle_mon_image_3.close()
            middle_mon_image_4.close()
            middle_mon_image_5.close()
            middle_mon_image_6.close()
            middle_mon_image_7.close()
            middle_mon_image_8.close()
    elif evo_chain_max_length == 3:
            base_mon_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{base_pokemon["DexNum"]}.png')
            if len(base_pokemon['Evolves-Into']) == 1:
                #only one middle evo
                middle_pokemon = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][0]["DexNum"]][0]
                middle_mon_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon["DexNum"]}.png')
                if len(middle_pokemon['Evolves-Into']) == 1:
                    #only one final evo, like venusaur
                    final_mon_image = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon["Evolves-Into"][0]["DexNum"]}.png')
                    background_image.paste(base_mon_image, (0, 50), mask=base_mon_image)
                    background_image.paste(middle_mon_image, (150, 50), mask=middle_mon_image)
                    background_image.paste(final_mon_image, (300, 50), mask=final_mon_image)

                    arrow_image = await create_arrow_image(type, 0, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (100, 90), mask=arrow_image)
                    arrow_image.close()

                    arrow_image = await create_arrow_image(type, 0, middle_pokemon["Evolves-Into"][0]['Method'], middle_pokemon["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (250, 90), mask=arrow_image)
                    arrow_image.close()

                    image_in_memory = BytesIO()
                    background_image.save(image_in_memory, format='PNG')

                    background_image.close()
                    base_mon_image.close()
                    middle_mon_image.close()
                    final_mon_image.close()
                elif len(middle_pokemon['Evolves-Into']) == 2:
                    #two final evos like kirlia
                    final_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon["Evolves-Into"][0]["DexNum"]}.png')
                    final_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon["Evolves-Into"][1]["DexNum"]}.png')
                    background_image.paste(base_mon_image, (0, 50), mask=base_mon_image)
                    background_image.paste(middle_mon_image, (150, 50), mask=middle_mon_image)
                    background_image.paste(final_mon_image_1, (300, 0), mask=final_mon_image_1)
                    background_image.paste(final_mon_image_2, (300, 100), mask=final_mon_image_2)

                    arrow_image = await create_arrow_image(type, 0, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (100, 90), mask=arrow_image)
                    arrow_image.close()

                    arrow_image = await create_arrow_image(type, 45, middle_pokemon["Evolves-Into"][0]['Method'], middle_pokemon["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (250, 55), mask=arrow_image)
                    arrow_image.close()

                    arrow_image = await create_arrow_image(type, -45, middle_pokemon["Evolves-Into"][1]['Method'], middle_pokemon["Evolves-Into"][1]['Value'])
                    background_image.paste(arrow_image, (250, 125), mask=arrow_image)
                    arrow_image.close()

                    image_in_memory = BytesIO()
                    background_image.save(image_in_memory, format='PNG')

                    background_image.close()
                    base_mon_image.close()
                    middle_mon_image.close()
                    final_mon_image_1.close()
                    final_mon_image_2.close()
            elif len(base_pokemon['Evolves-Into']) == 2:
                #2 middle evos, like mr mime
                middle_pokemon_1 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][0]["DexNum"]][0]
                middle_pokemon_2 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][1]["DexNum"]][0]
                middle_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_1["DexNum"]}.png')
                middle_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_2["DexNum"]}.png')
                background_image.paste(base_mon_image, (0, 50), mask=base_mon_image)
                background_image.paste(middle_mon_image_1, (150, 0), mask=middle_mon_image_1)
                background_image.paste(middle_mon_image_2, (150, 100), mask=middle_mon_image_2)

                if len(middle_pokemon_1['Evolves-Into']) != 0:
                    final_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_1["Evolves-Into"][0]["DexNum"]}.png')
                    background_image.paste(final_mon_image_1, (300, 0), mask=final_mon_image_1)
                    final_mon_image_1.close()

                    arrow_image = await create_arrow_image(type, 0, middle_pokemon_1["Evolves-Into"][0]['Method'], middle_pokemon_1["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (250, 55), mask=arrow_image)
                    arrow_image.close()
                if len(middle_pokemon_2['Evolves-Into']) != 0:
                    final_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_2["Evolves-Into"][0]["DexNum"]}.png')
                    background_image.paste(final_mon_image_2, (300, 100), mask=final_mon_image_2)
                    final_mon_image_2.close()

                    arrow_image = await create_arrow_image(type, 0, middle_pokemon_2["Evolves-Into"][0]['Method'], middle_pokemon_2["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (250, 125), mask=arrow_image)
                    arrow_image.close()

                arrow_image = await create_arrow_image(type, 45, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
                background_image.paste(arrow_image, (100, 55), mask=arrow_image)
                arrow_image.close()

                arrow_image = await create_arrow_image(type, -45, base_pokemon["Evolves-Into"][1]['Method'], base_pokemon["Evolves-Into"][1]['Value'])
                background_image.paste(arrow_image, (100, 125), mask=arrow_image)
                arrow_image.close()
                
                image_in_memory = BytesIO()
                background_image.save(image_in_memory, format='PNG')

                background_image.close()
                base_mon_image.close()
                middle_mon_image_1.close()
                middle_mon_image_2.close()
            elif len(base_pokemon['Evolves-Into']) == 3:
                #3 evos with a 3rd stage, like applin
                middle_pokemon_1 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][0]["DexNum"]][0]
                middle_pokemon_2 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][1]["DexNum"]][0]
                middle_pokemon_3 = [obj for obj in pokemon if obj['DexNum'] == base_pokemon["Evolves-Into"][2]["DexNum"]][0]
                middle_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_1["DexNum"]}.png')
                middle_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_2["DexNum"]}.png')
                middle_mon_image_3 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_3["DexNum"]}.png')
                background_image.paste(base_mon_image, (0, 50), mask=base_mon_image)
                background_image.paste(middle_mon_image_1, (150, 0), mask=middle_mon_image_1)
                background_image.paste(middle_mon_image_2, (150, 100), mask=middle_mon_image_2)
                background_image.paste(middle_mon_image_3, (200, 50), mask=middle_mon_image_3)

                if len(middle_pokemon_1['Evolves-Into']) != 0:
                    final_mon_image_1 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_1["Evolves-Into"][0]["DexNum"]}.png')
                    background_image.paste(final_mon_image_1, (275, 0), mask=final_mon_image_1)
                    final_mon_image_1.close()

                    arrow_image = await create_arrow_image(type, 0, middle_pokemon_1["Evolves-Into"][0]['Method'], middle_pokemon_1["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (250, 55), mask=arrow_image)
                    arrow_image.close()
                if len(middle_pokemon_2['Evolves-Into']) != 0:
                    final_mon_image_2 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_2["Evolves-Into"][0]["DexNum"]}.png')
                    background_image.paste(final_mon_image_2, (275, 100), mask=final_mon_image_2)
                    final_mon_image_2.close()

                    arrow_image = await create_arrow_image(type, 0, middle_pokemon_2["Evolves-Into"][0]['Method'], middle_pokemon_2["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (250, 125), mask=arrow_image)
                    arrow_image.close()
                if len(middle_pokemon_3['Evolves-Into']) != 0:
                    final_mon_image_3 = await open_http_image(f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{middle_pokemon_3["Evolves-Into"][0]["DexNum"]}.png')
                    background_image.paste(final_mon_image_3, (315, 50), mask=final_mon_image_3)
                    final_mon_image_3.close()

                    arrow_image = await create_arrow_image(type, 0, middle_pokemon_3["Evolves-Into"][0]['Method'], middle_pokemon_3["Evolves-Into"][0]['Value'])
                    background_image.paste(arrow_image, (275, 90), mask=arrow_image)
                    arrow_image.close()
                
                arrow_image = await create_arrow_image(type, 45, base_pokemon["Evolves-Into"][0]['Method'], base_pokemon["Evolves-Into"][0]['Value'])
                background_image.paste(arrow_image, (100, 55), mask=arrow_image)
                arrow_image.close()

                arrow_image = await create_arrow_image(type, -45, base_pokemon["Evolves-Into"][1]['Method'], base_pokemon["Evolves-Into"][1]['Value'])
                background_image.paste(arrow_image, (100, 125), mask=arrow_image)
                arrow_image.close()

                arrow_image = await create_arrow_image(type, 0, base_pokemon["Evolves-Into"][1]['Method'], base_pokemon["Evolves-Into"][1]['Value'])
                background_image.paste(arrow_image, (125, 90), mask=arrow_image)
                arrow_image.close()

                image_in_memory = BytesIO()
                background_image.save(image_in_memory, format='PNG')

                background_image.close()
                middle_mon_image_1.close()
                middle_mon_image_2.close()
                middle_mon_image_3.close()
    image_in_memory.seek(0)
    return discord.File(image_in_memory, filename=f'{type}.png')
#endregion

#region $sl dex command

async def makePokedexEmbed(mon, version_group):
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
    
    moveset, version_group = await get_moves(mon_data['moves'], version_group)

    moveset_levels, moveset_names, moveset_types_categories = movesetText(moveset)

    if len(moveset_types_categories) > 1024:
        index = moveset_types_categories.rfind(' ', 0 , 1024)

        moveset_types_categories = moveset_types_categories[:index]

    version_group_name = re.split(r'[\s-.]+', version_group)
    version_group_name = ' '.join(word.capitalize() for word in version_group_name)

    file = await createEvoChainImage(dex_num, mon_primary_type)

    embed = discord.Embed(title=f'#{mon_data["species"]["url"][42:].strip("/")} {mon_name} {type_emojis}',
                          color=[obj for obj in types if obj['Name'] == mon_primary_type][0]['Colour'])

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{dex_num}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_num}.png')

    embed.set_author(name='Pokémon Data', url=f'https://www.serebii.net/pokedex{[obj for obj in gens if any(group["Name"] == version_group for group in obj["Version-Groups"])][0]["Serebii-Link"]}/{str(mon_data["species"]["url"][42:].strip("/")).zfill(3)}.shtml')

    embed.add_field(name='Stats',
                    value=f'HP - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "hp"][0]["base_stat"]}\nAtk - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "attack"][0]["base_stat"]}\nDef - {[obj for obj in mon_data["stats"] if obj["stat"]["name"] == "defense"][0]["base_stat"]}',
                    inline=True)
    
    embed.add_field(name='᲼',
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

    #embed.set_footer(text=f'Moveset Data from {version_group_name}')

    return embed, file
#endregion

#region $sl moves command
async def showMoveSet(mon, level, version_group):
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

    moveset, version_group = await get_moves(mon_data['moves'], version_group)

    moveset_names, moveset_types_categories, moveset_power_accuracy = movesetTextLevel(moveset, level)

    version_group_name = re.split(r'[\s-.]+', version_group)
    version_group_name = ' '.join(word.capitalize() for word in version_group_name)

    embed = discord.Embed(title=f'Level {level} {mon_name}',
                          color=[obj for obj in types if obj['Name'] == str(mon_data['types'][0]['type']['name']).capitalize()][0]['Colour'])
    
    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{dex_num}.png')
    else: 
        embed.set_thumbnail(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{dex_num}.png')
    
    embed.set_author(name='Moveset Data', url=f'https://www.serebii.net/pokedex{[obj for obj in gens if any(group["Name"] == version_group for group in obj["Version-Groups"])][0]["Serebii-Link"]}/{str(mon_data["species"]["url"][42:].strip("/")).zfill(3)}.shtml')

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
#endregion

#endregion

#region $sl catch command
async def calculateCatchRate(mon, level, version_group):
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

    gen = [obj for obj in gens if any(group["Name"] == version_group for group in obj["Version-Groups"])][0]

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
async def addNickname(nickname, dex_num):
    mon = getMon(int(dex_num))

    if mon is None:
        return "Dex Number is not valid!"

    pokemon.append({
        'Name': nickname,
        'DexNum': mon['DexNum'],
        'Nickname': True,
        'Evolves-Into': mon['Evolves-Into'],
        'Evolves-From': mon['Evolves-From']
    })

    with open('text_files/soul_link_pokemon.txt', 'w') as file:
        file.write(json.dumps(pokemon))

    return f'Nickname \'{nickname}\' successfully added for {mon["Name"]}'

#endregion
        
#region $sl see-nicknames command
async def seeNicknames():
    nicknames = [obj for obj in pokemon if obj['Nickname'] is True]

    original_names = ''
    nick_names = ''
    
    for mon in nicknames:
        original_names += f'{[obj for obj in pokemon if obj["DexNum"] == mon["DexNum"]][0]["Name"]}\n'
        nick_names += f'{mon["Name"]}'
    
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