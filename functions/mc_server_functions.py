""" 
Contains the functions relating to the Minecraft Server

Cole Anderson, Dec 2024
"""

import discord
import json
import random
import regex as re
import asyncio
import socket
import subprocess
import math
import copy
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

with open('text_files/minecraft_server/googleDriveLink.txt', 'r') as file:
    googleDriveLink = file.read()

with open('text_files/minecraft_server/modInfo.txt', 'r') as file:
    serverMods = json.loads(file.read())

with open('text_files/minecraft_server/moai.txt', 'r') as file:
    moaiLocations = json.loads(file.read())

with open('text_files/minecraft_server/boats.txt', 'r') as file:
    boatLocations = json.loads(file.read())

dimensions = [
    {'Name': 'Overworld', 'CmdName': 'minecraft:overworld'}, 
    {'Name': 'Nether', 'CmdName': 'minecraft:the_nether'}, 
    {'Name': 'End', 'CmdName': 'minecraft:the_end'},
    {'Name': 'Anu\'s Lair', 'CmdName': 'fossil:anu_lair'}
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
                                        '```$mc loot boat, X: 100 Y: 30 Z: 100``` Marks a structure as looted. Valid options are `moai` and `boat`\n' +
                                        '```$mc save``` The server has autosaving, but you can do this too.\n\n\n' +
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
    embeds = []

    rand_num = random.randint(1, 100)

    serverOn = await serverOnline()

    embed = discord.Embed(title='Fossils Server Mods Info and Setup',
                            description=f'Server Ip: **{serverIp}**\n' +
                                        f'World Seed: **923372312397535711**\n' +
                                        f'Server Status: {"Online" if serverOn else "Offline"}\n\n'
                                        f'The server is run on Minecraft 1.18.2 using Fabric.\n' +
                                        f'Download Fabric here: https://fabricmc.net/use/installer/ \n\n'
                                        f'Modpack Downloads: {googleDriveLink} \n\n'
                                        f'Check the other embed pages for info on what mods are actually included.\n' + 
                                        f'If you don\'t care, download Fabric, then grab the recommended.zip from the Google Drive and throw it in your mods folder.\n\n' +
                                        f'Make sure to edit your installation in the Minecraft Launcher! Set the `-Xmx` field to something like 8Gb like so `-Xmx8G` to allow Minecraft to use more RAM!',
                            color=14914576)
    
    if rand_num == 69:
        embed.set_thumbnail(url='https://i.imgur.com/Np0NjY2.png')
    else:
        embed.set_thumbnail(url='https://i.imgur.com/oC02eDj.png')

    embeds.append(copy.deepcopy(embed))

    modCount = len([obj for obj in serverMods if obj['Type'] == 'Mod'])
    datapackCount = len([obj for obj in serverMods if obj['Type'] == 'Datapack'])
    resourcepackCount = len([obj for obj in serverMods if obj['Type'] == 'Resource Pack'])

    embed.title = 'Table of Contents'
    embed.description=(f'Required mods are marked with a ★\n' +
                       f'Recommended mods are marked with a ☆\n\n' +
                       f'**Mods**: Pages 3-{modCount+2} \n' +
                       f'**Datapacks**: Pages {modCount+3}-{modCount+datapackCount+2} \n' +
                       f'**Resource Packs**: Pages {modCount+datapackCount+3}-{modCount+datapackCount+resourcepackCount+3}')
    
    embeds.append(copy.deepcopy(embed))

    
    for mod in serverMods:
        embed.title = f'{"★ " if mod["Required"] == "Req" else ("☆ " if mod["Required"] == "Rec" else "")}{mod["Name"]} {mod["Type"]}'
        embed.description = f'{mod["Content"]}'
        embed.set_author(name=f'{mod["Type"]} Page Link', url=mod['Link'])
        embed.set_footer(text=f'More info can be found at the {mod["Type"]}\'s page')
        embed.set_thumbnail(url=mod["ImageLink"])

        embeds.append(copy.deepcopy(embed))

    embed = discord.Embed(title='Resource Pack Order',
                            description='Resource packs should stay zipped inside of the resource packs folder\n\n' +
                                        'Assuming you\'re using the recommended mod pack,\n' +
                                        'I find it works best to have the Travelers Backpack at the top(ignore the incompatability warning), ' +
                                        'with Vanilla Tweaks right under, then the two included continuity resource packs under that.\n\n' +
                                        'Everything should work as intended like this.',
                            color=14914576)
    
    if rand_num == 69:
        embed.set_thumbnail(url='https://i.imgur.com/Np0NjY2.png')
    else:
        embed.set_thumbnail(url='https://i.imgur.com/oC02eDj.png')

    embeds.append(embed)

    return embeds

#endregion

#region rcon server info commands
async def serverOnline():
    try:
        with socket.create_connection((serverIp, serverPort), timeout=3):
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

    playersText = playersOnline.split(':')[1].strip()

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

    daytime = int(re.search(r'\d+$', daytime.strip()).group())

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

    embed = discord.Embed(title=f'Fossils Server Info',
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

            if '"' in dimension:
                dimensionData = re.split('"', dimension)[1]
                playerDimensionText += f'{getDimensionName(dimensionData.strip())}\n'
            else:
                return f'Couldn\'t get data on {player}!', file
            
            if ':' in coordinates:
                coordinateData = re.split(':', coordinates)[1]
                playerCoordinateText += f'{formatPlayerCoordinates(coordinateData.strip()[1:-1])}\n'
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
    
    if 'moai' in modifiers['Target']:
        return await unlootedMoais()
    
    if 'hell_boat' in modifiers['Target']:
        return await unlootedBoats()

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

async def unlootedMoais():
    embeds = []

    embed = discord.Embed(title=f'Unlooted Moai\'s',
                            description='Copy paste the line of text to mark it as looted',
                            color=14914576)
    
    locationText = ''

    pageCount = 15
    for moai in moaiLocations:
        if moai['Looted'] is False:
            if pageCount > 0:
                locationText += f'X: {moai["X"]} Y: {moai["Y"]} Z: {moai["Z"]}\n'
                pageCount -= 1
            else:
                embed.add_field(name='Location',
                                value=locationText,
                                inline=True)

                embeds.append(copy.deepcopy(embed))

                embed.clear_fields()
                locationText = ''
                pageCount = 15

    embed.add_field(name='Location',
                        value=locationText,
                        inline=True)
    
    embeds.append(embed)

    return embeds

async def unlootedBoats():
    embeds = []

    embed = discord.Embed(title=f'Unlooted Hell Boats',
                            description='Copy paste the line of text to mark it as looted',
                            color=14914576)
    
    locationText = ''

    pageCount = 15
    for boat in boatLocations:
        if boat['Looted'] is False:
            if pageCount > 0:
                locationText += f'X: {boat["X"]} Y: {boat["Y"]} Z: {boat["Z"]}\n'
                pageCount -= 1
            else:
                embed.add_field(name='Location',
                                value=locationText,
                                inline=True)

                embeds.append(copy.deepcopy(embed))

                embed.clear_fields()
                locationText = ''
                pageCount = 15

    embed.add_field(name='Location',
                        value=locationText,
                        inline=True)
    
    embeds.append(embed)

    return embeds

async def saveStructureData():
    global moaiLocations
    global boatLocations

    with open('text_files/minecraft_server/moai.txt', 'w') as file:
        file.write(json.dumps(moaiLocations))

    with open('text_files/minecraft_server/moai.txt', 'r') as file:
        moaiLocations = json.loads(file.read())

    with open('text_files/minecraft_server/boats.txt', 'w') as file:
        file.write(json.dumps(boatLocations))

    with open('text_files/minecraft_server/boats.txt', 'r') as file:
        boatLocations = json.loads(file.read())

async def mcLoot(structure, location):
    coord_pattern = re.compile(r"x: (-?\d+) y: (-?\d+) z: (-?\d+)")
    match = coord_pattern.search(location)

    if match:
        x, y, z = map(int, match.groups())
    else:
        return 'Coordinates are formatted wrong! Just copy paste them from the list of unlooted structures!'
    
    if structure == 'moai':
        try:
            [obj for obj in moaiLocations if obj['X'] == x and obj['Y'] == y and obj['Z'] == z][0]['Looted'] = True
        except:
            return 'Coordinates didn\'t lead to a valid Moai location!'
    elif structure == 'boat':
        try:
            [obj for obj in boatLocations if obj['X'] == x and obj['Y'] == y and obj['Z'] == z][0]['Looted'] = True
        except:
            return 'Coordinates didn\'t lead to a valid Hell Boat!'
    else:
        return f'I don\'t know what a \'{structure}\' is!'

    await saveStructureData()

    return 'Structure marked as looted!'

#endregion

#region start stop and restart

async def mcStart():
    try:
        working_directory = 'C:\\Users\\Cole A\\Documents\\1Minecraft Server\\Fossils Server'

        subprocess.Popen('C:\\Users\\Cole A\\Documents\\1Minecraft Server\\Fossils Server\\start.bat', cwd=working_directory, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return 'Server starting up!'
    except FileNotFoundError:
        return 'Server start.bat file not found! Check to make sure the path is correct!'
    except:
        return 'Failed to start the server!'

async def mcBeginStop():
    await mcSay(f'The server will shutdown in one minute, prepare yourself!')

    asyncio.create_task(mcStop())

async def mcStop():
    await asyncio.sleep(60)

    await rcon(
        f'stop',
        host=rconIp, port=rconPort, passwd=rconPassword
    )

async def mcRestart():
    await mcBeginStop()

    asyncio.create_task(mcWaitStart())

async def mcWaitStart():
    await asyncio.sleep(90)

    await mcStart()

#endregion