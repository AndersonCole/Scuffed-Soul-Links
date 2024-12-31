""" 
Contains the functions relating to the Minecraft Server

Cole Anderson, Dec 2024
"""

import discord
import json
import random
import regex as re
import time
import asyncio
import socket
import subprocess
import math
from rcon.source import rcon

with open('text_files/minecraft_server/serverIp.txt', 'r') as file:
    serverIp = file.read()

with open('text_files/minecraft_server/serverPort.txt', 'r') as file:
    serverPort = int(file.read())

with open('text_files/minecraft_server/rconIp.txt', 'r') as file:
    rconIp = file.read()

with open('text_files/minecraft_server/rconPort.txt', 'r') as file:
    rconPort = int(file.read())

with open('text_files/minecraft_server/rconPassword.txt', 'r') as file:
    rconPassword = file.read()

dimensions = [
    {'Name': 'Overworld', 'CmdName': 'minecraft:overworld'}, 
    {'Name': 'Nether', 'CmdName': 'minecraft:the_nether'}, 
    {'Name': 'End', 'CmdName': 'minecraft:the_end'}
]

#region help and setup commands
async def mcHelp():
    file = discord.File('images/minecraft/amber_shuckle.png', filename='amber_shuckle.png')
    shinyFile = discord.File('images/minecraft/amber_shiny_shuckle.png', filename='amber_shiny_shuckle.png')

    embed = discord.Embed(title='Shuckles Fossils Server Commands',
                            description='```$mc setup``` Gives info on required and recommended mods.\n' +
                                        '```$mc info``` Gives server info such as players online and time of day.\n' +
                                        '```$mc say Hello!``` Writes a message in the server chat.\n' +
                                        '```$mc locate help``` Check for more info on the locate command, modifiers return!\n' +
                                        '```$mc save``` The server has autosaving, but you can do this too.\n' +
                                        '\n\n' +
                                        '**Admin Only:**\n' +
                                        '```$mc start``` Starts the server\n' +
                                        '```$mc stop``` Stops the server\n' +
                                        '```$mc restart``` Stops the restarts the server.', 
                            color=14914576)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://amber_shiny_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://amber_shuckle.png')
        return embed, file

async def mcLocateHelp():
    file = discord.File('images/minecraft/amber_shuckle.png', filename='amber_shuckle.png')
    shinyFile = discord.File('images/minecraft/amber_shiny_shuckle.png', filename='amber_shiny_shuckle.png')

    embed = discord.Embed(title='Shuckles Fossils Server Locate Command',
                            description='Locate searches for the closest biome or structure to 0 0 0 in the overworld by default\n' +
                                        'You MUST specify the mod name if it\'s not a vanilla biome/structure! Examples are below:\n' +
                                        '```$mc locate plains``` Locates the nearest `minecraft:plains` biome from 0 0\n' +
                                        '```$mc locate byg:dead_sea``` Locates the nearest `byg:dead_sea` modded biome from 0 0\n' +
                                        '```$mc locate structure, #village``` Locates the nearest `#minecraft:village` from 0 0\n' +
                                        '```$mc locate structure, fortress, nether``` Locates the nearest `minecraft:fortress` in the nether from 0 0\n' +
                                        '```$mc locate byg:imparius_grove, end``` Locates the nearest `byg:imparius_grove` modded biome in the end from 0 0\n' +
                                        '```$mc locate forest, 1500 -1500``` Locates the nearest `minecraft:forest` in the overworld from X:1500 Z:-1500\n\n' +
                                        'As usual, all the modifiers can be applied in any order\n\n' +
                                        'For Vanilla Biomes, check: https://minecraft.wiki/w/Biome#Biome_IDs \n' +
                                        'For Vanilla Structures, check: https://minecraft.wiki/w/Structure#Data_values \n'
                                        'For BYG Biomes, check: https://oh-the-biomes-youll-go.fandom.com/wiki/Category:Biomes \n' +
                                        'Modded wikis may not be as good as the Vanilla wiki, so just go in game and try out /locate and /locatebiome and take a look at the options in a singleplayer world.\n' +
                                        'Everything should be case insensitive, and it will replace any spaces with underscores.',
                            color=14914576)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://amber_shiny_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://amber_shuckle.png')
        return embed, file

async def mcSetup():
    return ['embeds! file sharing! yay!']

#endregion

#region rcon server info commands
async def serverOnline():
    try:
        with socket.create_connection((serverIp, serverPort), timeout=5):
            return True
    except:
        return False

def getDimensionName(dimension):
    try:
        return [obj for obj in dimensions if obj['CmdName'] == dimension][0]['Name']
    except:
        return None
    
def formatPlayerCoordinates(coordinates):
    if ',' in coordinates:
        splitCoords = re.split(',', coordinates)
        splitCoords = [int(math.floor(float(obj.strip()[:-1]))) for obj in splitCoords]

        return f'{splitCoords[0]} {splitCoords[1]} {splitCoords[2]}'
    else:
        return None


async def mcInfo():
    file = discord.File('images/minecraft/amber_shuckle.png', filename='amber_shuckle.png')
    shinyFile = discord.File('images/minecraft/amber_shiny_shuckle.png', filename='amber_shiny_shuckle.png')

    playersOnline = await rcon(
        f'list',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

    playersText = playersOnline.split(':')[1]

    if len(playersText) > 1:
        if ',' in playersText:
            players = playersText.split(',')
        else:
            players = [playersText]
    else:
        players = []

    daytime = await rcon(
        f'time query daytime',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

    daytime = int(daytime)

    if daytime >= 23000:
        timeText = 'Sunrise'
    elif daytime >= 21000:
        timeText = 'Late Night'
    elif daytime >= 17000:
        timeText = 'Night'
    elif daytime >= 13000:
        timeText = 'Early Night'
    elif daytime >= 12000:
        timeText = 'Sunset'
    elif daytime >= 9000:
        timeText = 'Afternoon'
    elif daytime >= 5000:
        timeText = 'Midday'
    elif daytime >= 1000:
        timeText = 'Morning'
    else:
        timeText = 'Sunrise'

    embed = discord.Embed(title=f'Fossil Server Info',
                          description=f'Players Online: {len(players)}\nCurrent Overworld Time: **{timeText}**',
                          color=14914576)
    
    if len(players) > 0:
        playerNameText = ''
        playerDimensionText = ''
        playerCoordinateText = ''

        for player in players:
            playerNameText += f'{player.strip()}\n'

            dimension = await rcon(
                f'execute as {player.strip()} run data get entity @s Dimension',
                host=rconIp, port=rconPort, passwd=rconPassword
            )

            coordinates = await rcon(
                f'execute as {player.strip()} run data get entity @s Pos',
                host=rconIp, port=rconPort, passwd=rconPassword
            )

            if ':' in dimension:
                dimensionData = re.split(':', dimension)[1]
                playerDimensionText += f'{getDimensionName(dimensionData.strip()[1:-1])}'
            else:
                return f'Couldn\'t get data on {player}!', file
            
            if ':' in coordinates:
                coordinateData = re.split(':', coordinates)[1]
                playerCoordinateText += f'{formatPlayerCoordinates(coordinateData.strip()[1:-1])}'
            else:
                return f'Couldn\'t get data on {player}!', file

        embed.add_field(name='Players',
                    value=playerNameText,
                    inline=True)
        
        embed.add_field(name='Dimension',
                    value=playerDimensionText,
                    inline=True)
        
        embed.add_field(name='Location',
                    value=playerCoordinateText,
                    inline=True)


    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://amber_shiny_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://amber_shuckle.png')
        return embed, file
    
async def mcSay(message, author='Shuckle'):
    authorColour = 'dark_green'
    if author == 'Shuckle':
        authorColour = 'gold'

    shuckleMessage = json.dumps({
        'text': f'[{author}]: ',
        'color': authorColour,
        'extra': [
            {'text': message, 'color': 'white'}
        ]
    })

    await rcon(
        f'tellraw @a {shuckleMessage}',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

async def mcSave(author):
    await rcon(
        f'save-all',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

    await mcSay(f'{author} initialized a manual server save! If it causes lag blame them!')

def getLocateModifiers(inputs):
    modifiers = {
        'Dimension': 'minecraft:overworld',
        'Coordinates': '0 0 0',

        'SearchFor': 'biome',
        'Target': ''
    }

    errorText = ''

    for input in inputs:
        if str(input).strip().lower() == 'overworld':
            modifiers['Dimension'] = 'minecraft:overworld'
        elif str(input).strip().lower() == 'nether':
            modifiers['Dimension'] = 'minecraft:the_nether'
        elif str(input).strip().lower() == 'end':
            modifiers['Dimension'] = 'minecraft:the_end'

        elif str(input).strip().lower() == 'biome':
            modifiers['SearchFor'] = 'biome'
        elif str(input).strip().lower() == 'structure':
            modifiers['SearchFor'] = ' structure'

        elif bool(re.match(r'^-?\d+(\.\d+)?\s+-?\d+(\.\d+)?$', str(input).strip())):
            coords = re.split(r'[\s]+', input.strip())
            if len(coords) == 2:
                try:
                    modifiers['Coordinates'] = f'{int(coords[0])} 0 {int(coords[1])}'
                except:
                    errorText += f'\'{input}\' was not understood as valid coordinates!\n'
            else:
                errorText += f'\'{input}\' was not understood as valid coordinates!\n'

        else:
            input = str(input).strip().lower()
            if ':' not in input:
                if input[0] == '#':
                    input = f'#minecraft:{input[1:]}'
                else:
                    input = f'minecraft:{input}'
                modifiers['Target'] = re.sub(r'\s', '_', input)
            else:
                modifiers['Target'] = re.sub(r'\s', '_', input)

    return modifiers, errorText


async def mcLocate(author, inputs):
    modifiers, errorText = getLocateModifiers(inputs)
    if errorText != '':
        return errorText
    
    response = await rcon(
        f'execute in {modifiers["Dimension"]} positioned {modifiers["Coordinates"]} run locate{modifiers["SearchFor"]} {modifiers["Target"]}',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

    if response[:9] == 'Could not':
        return f'Could not find a {modifiers["Target"]} in the {getDimensionName(modifiers["Dimension"])} near {modifiers["Coordinates"]}!'
    else:
        targetCoords = (re.search(r'\[([^\]]+)\]', response)).group(1).split(',')

        message = f'{author} found a {modifiers["Target"]} in the {getDimensionName(modifiers["Dimension"])} at {targetCoords[0].strip()} {targetCoords[1].strip()} {targetCoords[2].strip()}'
        
        await mcSay(message)

        return message

#endregion

#region start stop and restart

async def mcStart():
    try:
        subprocess.run('C:\\Users\\Cole A\\Documents\\1Minecraft Server\\Fossils Server\\start.bat', check=True, shell=True)
        return 'Server starting up!'
    except FileNotFoundError:
        return 'Server start.bat file not found! Check to make sure the path is correct!'
    except:
        return 'Failed to start the server!'

async def mcBeginStop():
    await mcSay(f'The server will shutdown in one minute, prepare yourself!')

    stopThread = asyncio.create_task(mcStop)
    stopThread.start()

async def mcStop():
    await asyncio.sleep(60)

    await rcon(
        f'stop',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

async def mcRestart():
    await mcBeginStop()

    startThread = asyncio.create_task(mcWaitStart)
    startThread.start()

async def mcWaitStart():
    await asyncio.sleep(90)

    response = await mcStart()

    print(response)

#endregion