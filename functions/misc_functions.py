import discord
import copy
import regex as re
from dictionaries.shared_dictionaries import sharedImagePaths, sharedFileLocations, sharedEmbedColours
from functions.shared_functions import (
   checkForNickname, getMonFromName, formatTextForBackend, formatTextForDisplay, buildNicknameLookupTable, 
   saveDataVariableToFile, rollForShiny, pokemon, users, getUserIdFromNickname, getDexNum, getUserPing
)

def shuckleHelp():
    embed = discord.Embed(title=f'Shuckle Bot Commands',
                                description='```$sl help``` Shows all the soul link commands\n' +
                                            '```$routes help``` Shows all the routes commands\n' +
                                            '```$dps help``` Shows all the PoGo dps commands\n' +
                                            '```$max help``` Shows all the PoGo dynamax commands\n' +
                                            '```$pvp help``` Shows all the PoGo Pvp commands\n' +
                                            '```$pogo help``` Shows all the PoGo event commands\n' +
                                            '```$mc help``` Shows all minecraft server commands\n' +
                                            '```$format help``` Shows how to call the mimikyu format command\n' +
                                            '```$coins``` Gets the coins link\n' +
                                            '```$shuckle make-csv I <3 kanto, ooooo charizard!``` Takes any text input, and pulls out the pokemon names within, giving you a csv list of matching names\n\n' +
                                            '```$shuckle add-nickname Ttar, Tyranitar``` Adds a nickname to a pokemon\n' +
                                            '```$shuckle add-nickname nickname, @user``` Adds a nicknames to a user\n' +
                                            '```$shuckle remove-nickname Ttar``` Removes a nickname from a pokemon\n' +
                                            '```$shuckle remove-nickname nickname``` Removes a nickname from a user\n\n' +
                                            '```$shuckle mon-nicknames``` Prints out all pokemon nicknames\n' +
                                            '```$shuckle user-nicknames``` Prints out all user nicknames',
                                color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    return embed

def mimikyuFormat(userInput):
    try:
        if userInput == 'help':
            raise Exception
        
        if ',' in userInput:
            splitInput = userInput.split(',')
            battle_name = splitInput[0].strip()
            level_cap = int(splitInput[1])
            encounters = []
            for text in splitInput[2:]:
                encounters.append(text.strip())

            encounters_text = '['
            if encounters == []:
                encounters_text += ']'
            for encounter in encounters:
                if encounter == encounters[-1]:
                    encounters_text += f'\'{encounter}\']'
                else:
                    encounters_text += f'\'{encounter}\', '
                
            return '{' + f'\'Stage\': 0, \'Battle-Name\': \'{battle_name}\', \'Level-Cap\': {level_cap}, \'Encounters\': {encounters_text}' + '}'
        else:
            raise Exception
    except:
        return ('Mimikyu Lives On! But... you\'ve still learned nothing and went and fucked something up.\n' +
                'Only send messages like this ```$format Misty, 20, Route 3, Route 4```' +
                'In this order, name of the next battle ex. Gym 2 or Misty, level cap for the next battle, then all the encounters before the next battle.')

def csvSortKey(mon):
    return getDexNum(mon)

async def getCSVFromInput(text):
    monNames = [mon['Name'] for mon in pokemon]
    matchingMonOutput = ''
    matchingMonNames = set()
    for name in reversed(monNames):
        if name in text:
            matchingMonNames.add(name)
            text = text.replace(name, '')
    matchingMonNames = sorted(list(matchingMonNames), key=csvSortKey)

    for mon in matchingMonNames:
        matchingMonOutput += f'{mon},'

    return f'```{{{matchingMonOutput[:-1]}}}```'

#region nicknames
async def saveMonNicknameData():
    buildNicknameLookupTable()

    await saveDataVariableToFile(sharedFileLocations.get('Pokemon'), pokemon)

async def addNickname(nickname, original):
    if getMonFromName(original):
        return await addMonNickname(nickname, original)
    return await addUserNickname(nickname, original)

async def removeNickname(nickname):
    if getMonFromName(nickname):
        return await removeMonNickname(nickname)
    return await removeUserNickname(nickname)

async def addMonNickname(nickname, originalName):
    mon = getMonFromName(originalName)

    if mon is None:
        return f'\'{originalName}\' is not a valid mon!'

    if getMonFromName(nickname):
        return 'You can\'t make a nickname the same as another pokemon\'s name! Be original!'

    if getUserIdFromNickname(nickname):
        return 'You can\'t make a pokemon nickname the same as a user nickname! Be original!'

    mon['Nicknames'].append(formatTextForBackend(nickname))

    await saveMonNicknameData()

    return f'Nickname \'{nickname}\' successfully added for {formatTextForDisplay(mon["Name"])}'

async def addUserNickname(nickname, originalId):
    if re.search(r'<@\d+>', originalId) is None:
        return 'You have to specify a user to make a nickname for by pinging them!'

    originalId = getUserIdFromNickname(originalId)
    
    if getMonFromName(nickname):
        return 'You can\'t make a user nickname the same as a pokemon name! Be original!'

    if getUserIdFromNickname(nickname):
        return 'You can\'t make a user nickname the same as another user\'s nickname! Be original!'

    if len([obj for obj in users if obj['User'] == originalId]) == 0:
            users.append({
                'User': originalId,
                'Nicknames': []
            })

    [obj for obj in users if obj['User'] == originalId][0]['Nicknames'].append(formatTextForBackend(nickname))

    await saveDataVariableToFile(sharedFileLocations.get('UserNicknames'), users)

    return f'Nickname \'{formatTextForDisplay(nickname)}\' successfully added for {getUserPing(originalId)}!'

async def removeMonNickname(nickname):
    originalMonName = checkForNickname(nickname)

    if originalMonName is None:
        return f'\'{nickname}\' is not a valid nickname!'

    if originalMonName == nickname:
        return f'\'{nickname}\' is not a valid nickname!'

    mon = getMonFromName(originalMonName)

    mon['Nicknames'].remove(formatTextForBackend(nickname))

    await saveMonNicknameData()

    return f'Nickname \'{nickname}\' successfully removed from {formatTextForDisplay(mon["Name"])}'

async def removeUserNickname(nickname):
    originalUser = getUserIdFromNickname(nickname)

    if originalUser is None:
        return f'\'{nickname}\' is not a valid nickname!'

    if originalUser == nickname:
        return f'\'{nickname}\' is not a valid nickname!'

    [obj for obj in users if obj['User'] == originalUser][0]['Nicknames'].remove(formatTextForBackend(nickname))

    await saveMonNicknameData()

    return f'Nickname \'{nickname}\' successfully removed from {originalUser}'

def listMonNicknames():
    embeds = []

    embed = discord.Embed(title='Shuckle\'s Pokemon Nicknames', 
                          color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    nicknames = []

    withNicknames = [obj for obj in pokemon if len(obj['Nicknames']) > 0]

    for mon in withNicknames:
        for nickname in mon['Nicknames']:
            nicknames.append({
                "Original": mon["Name"],
                "Nickname": nickname
            })

    originalNameText = ''
    nicknameText = ''
    
    pageCount = 15
    for nickname in nicknames:
        if pageCount > 0:
            originalNameText += f'{formatTextForDisplay(nickname["Original"])}\n'
            nicknameText += f'{formatTextForDisplay(nickname["Nickname"])}\n'
            pageCount -= 1
        else:
            embed.add_field(name='Nickname',
                            value=nicknameText,
                            inline=True)
            
            embed.add_field(name='Original',
                            value=originalNameText,
                            inline=True)
            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()
            originalNameText = ''
            nicknameText = ''
            pageCount = 15
    
    if pageCount < 15:
        embed.add_field(name='Nickname',
                            value=nicknameText,
                            inline=True)
            
        embed.add_field(name='Original',
                        value=originalNameText,
                        inline=True)
        embeds.append(embed)
        
    return embeds

def listUserNicknames():
    embeds = []

    embed = discord.Embed(title='Shuckle\'s User Nicknames', 
                          color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    for user in users:
        embed.description = f'{getUserPing(user["User"])}\'s Nicknames'

        for nickname in user['Nicknames']:
            nicknameText = ''

            nicknameText += f'{formatTextForDisplay(nickname)}\n'

            embed.add_field(name='',
                            value=nicknameText,
                            inline=False)

        embeds.append(copy.deepcopy(embed))
        
        embed.clear_fields()

    return embeds
#endregion

async def order66(guild):
    try:
        for i in range(66):
            role = await guild.create_role(name=f'Fraud Role #{i}')

            await role.edit(color=9314812)

            user = guild.get_member(341696864833241090)

            await user.add_roles(role)
    except Exception as ex:
        print(ex)
    
    return 'It has been done'

async def healTheWorld(guild):
    all_roles = await guild.fetch_roles()

    try:
        for role in all_roles:
            if 'Fraud Role' in role.name:
                await role.delete()
    except Exception as ex:
        print(ex)

    return 'And it shall be done, as it was in the beginning, as it has always been\nPeace shall descend graciously upon the land, and all will be mended'