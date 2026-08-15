""" 
Contains the functions relating to PoGo events

Cole Anderson, Aug 2025
"""

import discord
import aiohttp
import json
import copy
import regex as re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import math
from dictionaries.shared_dictionaries import sharedImagePaths, sharedEmbedColours
from dictionaries.pogo_dictionaries import pogoFileLocations, eventColours, filterLists, timezones, defaultOddsModifiers, trackedEmojis
from dictionaries.pvp_dictionaries import pvpFileLocations
from functions.shared_functions import (
    formatTextForDisplay, getMonFromName, getRegionFromDexNum,
    getPokeAPISpriteUrl, getTypesFromPokeAPI, getTypeColour, verifyRegion, getMon, addPaginatedEmbedFields,
    rollForShiny, getDexNum, getPokeApiJsonData, getPoGoCPMultiplier, calcPoGoCP, calcPoGoStat, calcPoGoStatsFromBaseStats,
    loadDataVariableFromFile, saveDataVariableToFile, formatTextForBackend, checkClassification, pogoPokemon
)

trackedMons = loadDataVariableFromFile(pogoFileLocations.get('TrackedMons'))

fakeRankOnes = loadDataVariableFromFile(pvpFileLocations.get('FakeR1'))

#region help command
async def pogoHelp():
    embed = discord.Embed(title='Shuckles PoGo Commands',
                            description='```$pogo add-mon Kartana, 323, 182, 139``` Registers a mons base stats in Atk/Def/HP order\n' +
                                        '```$pogo delete-mon Kartana``` Deletes a mon from the registered list\n' +
                                        '```$pogo list-mons``` Lists all the registered mons\n\n' +
                                        '```$pogo stats Kartana``` Calculates what the pokemons stats would be like in Go using its most recent main series stats\n'
                                        '```$pogo stats Kartana, noNerf``` Calculates what it would be like without any stat nerfs\n`noNerf`, `3Nerf` and `9Nerf` are the allowed nerf exceptions\n'
                                        '```$pogo stats 59, 181, 131, 59, 31, 109``` Calculates stats for Go based on the entered HP, Atk, Def, SpAtk, SpDef and Spd stats\nNerf exceptions can be applied here too\n\n'
                                        '```$pogo user-nickname John Alola, @Logan``` Adds a user nickname to be used when tracking\n' +
                                        '```$pogo track bulbasaur, xxs, xxl``` Adds a mon to your tracking list\nAllowed options are `all` `hundo` `lucky` `shiny` `gl` `ul` `shadow` `purified` `xxs` `xxl`\n' +
                                        '```$pogo untrack bulbasaur, all``` Removes a mon from your tracking list. Uses the same allowed options\n' +
                                        '```$pogo tracked bulbasaur, John Alola``` Shows what a user has tracked for a specific pokemon\n' +
                                        '```$pogo tracked-list region/class, filter, John Alola``` Shows what a user has tracked for either a region or a class of pokemon\n' + 
                                        'Allowed region/class options are every region name `all` `regional` `rare` `starters` `baby` `legendary` `mythical` `ultra-beast` `paradox` `mega` `hasMega` `gmax` `hasGmax`\n' +
                                        'Allowed filter options are `all` `hundo` `lucky` `shiny` `pvp` `rocket` `size`\n\n' +
                                        '```$pogo events help``` Shows all event searches\n\n' +
                                        '```$pogo odds Shuckle``` Shows the odds of getting something\n' +
                                        '```$pogo odds modifiers``` Lists out all the available odds modifers',
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))
    
    return embed

async def pogoEventsHelp():
    embed = discord.Embed(title='Shuckles PoGo Event Commands',
                            description='```$pogo events all``` Shows upcoming and current events\n' +
                                        '```$pogo events commDays``` Shows upcoming community days\n' +
                                        '```$pogo events hourEvents``` Shows Max Mondays, Spotlight Hours and Raid Hours\n' +
                                        '```$pogo events raids``` Shows upcoming raid boss changovers, and other raid events\n' +
                                        '```$pogo events gbl``` Shows upcoming GBL league rotations\n\n'
                                        'All event data is scraped from LeekDuck',
                            color=sharedEmbedColours.get('Default'))

    embed.set_author(name='Events Data Source', url='https://github.com/bigfoott/ScrapedDuck')

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))
    
    return embed  
#endregion

#region event commands
def getDateForComparison(date):
    if date.endswith('Z'):
        return datetime.fromisoformat(date[:-1])
    return datetime.fromisoformat(date)

def eventSortKey(event):
    startDate = getDateForComparison(event['start'])
    endDate = getDateForComparison(event['end'])

    if (endDate-startDate).days >= 21:
        return endDate
    return startDate

async def retrieveEventsFromAPI(eventFilterList):
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get('https://raw.githubusercontent.com/bigfoott/ScrapedDuck/data/events.json') as response:
                response.raise_for_status()

                events = json.loads(await response.text())
    except Exception as ex:
        print(ex)
        return None
    
    sortedEvents = sorted(events, key=eventSortKey, reverse=False)

    filteredEvents = []
    for event in sortedEvents:
        event['eventType'] = event['eventType'].replace(' skeleton-loading', '')
        if event['eventType'] in eventFilterList:
            if event['eventType'] == 'go-battle-league':
                splitName = re.split(r'[\|]+', event['name'])
                event['name'] = splitName[0]
            filteredEvents.append(event)

    return filteredEvents

def getDateTimeFormatString():
    return '%Y-%m-%dT%H:%M:%S.%f'

def formatTimeForDisplay(time):
    if time.endswith('Z'):
        time = datetime.strptime(time[:-1], getDateTimeFormatString())
        time = time.replace(tzinfo=timezone.utc)

        epochTime = int(time.timestamp())

        return f'<t:{epochTime}:F>'
    
    time = datetime.strptime(time, getDateTimeFormatString())

    return f'{time.strftime("%A, %B %d, %Y %I:%M %p")}'

def formatTimeZoneForDisplay(time, timezone):
    time = datetime.strptime(time, getDateTimeFormatString())
    time = time.replace(tzinfo=ZoneInfo(timezone))

    epochTime = int(time.timestamp())

    return f'<t:{epochTime}:F>'

def formatEventDates(start, end):
    if start.endswith('Z'):
        start = start[:-1]
    if end.endswith('Z'):
        end = end[:-1]
    start = datetime.strptime(start, getDateTimeFormatString())
    end = datetime.strptime(end, getDateTimeFormatString())

    return f'{start.strftime("%m/%d")} - {end.strftime("%m/%d")}'

def doubleSpacing(length):
    if length > 49:
        return '\n'
    return ''

async def createEventsEmbeds(filterFor):
    filterList = filterLists.get(filterFor.lower().strip(), None)
    if filterList is None:
        return 'I don\'t understand what events you\'re trying to get info on!\n\nCheck `$pogo help` to see all valid searches!'
    
    events = await retrieveEventsFromAPI(filterList)

    if events is None:
        return 'There was an error while checking the api!'

    if len(events) == 0:
        return 'There was no data on the requested events!'
    
    embeds = []
    
    embed = discord.Embed()

    firstEmbed = discord.Embed(title='Upcoming PoGo Events',
                                color=eventColours.get(filterFor.lower().strip(), sharedEmbedColours.get('Default')))
    firstEmbed.set_author(name='More Info at LeekDuck', url='https://leekduck.com/events')

    firstEmbed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))
    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    embeds.append(firstEmbed)

    eventNames = ''
    eventDates = ''

    for event in events:
        eventNames += f'{event["name"]}\n'
        eventDates += f'{formatEventDates(event["start"], event["end"])}\n{doubleSpacing(len(event["name"]))}'

        embed.title = event["name"]

        embed.description = f'Start Time: {formatTimeForDisplay(event["start"])}\nEnd Time: {formatTimeForDisplay(event["end"])}'
        if not event['start'].endswith('Z'):
            embed.description += f'\n\nNZ Start Time: {formatTimeZoneForDisplay(event["start"], timezones.get("NZ"))}\nHawaii End Time: {formatTimeZoneForDisplay(event["end"], timezones.get("Hawaii"))}'

        embed.colour = eventColours.get(event['eventType'], sharedEmbedColours.get('Default'))

        embed.set_image(url=event['image'])

        embed.set_author(name='More info at LeekDuck', url=event['link'])

        embed.set_footer(text=formatTextForDisplay(event["eventType"]))

        embeds.append(copy.deepcopy(embed))

    firstEmbed.add_field(name='Event Name',
                         value=eventNames)
    firstEmbed.add_field(name='Event Dates',
                         value=eventDates)

    return embeds
    
#endregion

#region odds command
def oddsModifiers():
    embed = discord.Embed(title='Shuckles PoGo Odds Modifiers',
                            description='```$pogo odds Shuckle, 15/15/15``` IVs: Sets the minimum acceptable IVs\n' +
                                        '```$pogo odds Shuckle, Floor10``` Floor: Sets the iv floor of the encounter\n\n' +
                                        '```$pogo odds Shuckle, Shiny20``` Shiny: Sets the odds of getting a shiny\n' +
                                        '```$pogo odds Shuckle, Background10``` Background: Sets the odds of getting a background\n' +
                                        '```$pogo odds Shuckle, Extra10``` Extra: Sets the odds of getting something extra, like a special move\n' +
                                        '```$pogo odds Shuckle, BottleCap``` BottleCap: Finds the odds of getting something silver cappable\n\n' +
                                        'Everything should be case insensitive.\nThe denominator of the odds fraction should be entered for shiny, background and extra chances',
                            color=sharedEmbedColours.get('Default'))

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))

    return embed

def getIvText(ivs):
    extraIvText = ' or better'
    if ivs['Attack'] == 15 and ivs['Defence'] == 15 and ivs['Stamina'] == 15:
        extraIvText = ''
    return f'**{ivs["Attack"]}/{ivs["Defence"]}/{ivs["Stamina"]}**{extraIvText} IVs'

def getExtraText(extraText):
    if extraText == '':
        return ''
    return f'{extraText}with '

def getTargetText(extraText, ivs, floor, bottleCap):
    if bottleCap:
        return f'{getExtraText(extraText)}a **{floor} IV Floor**'
    return f'{getExtraText(extraText)}{getIvText(ivs)}, and a **{floor} IV Floor**'

def tryingForShiny(shinyChance):
    if shinyChance is not None:
        return True
    return False

def raiseIvsToFloor(ivs, floor):
    if floor > ivs['Attack']:
        ivs['Attack'] = floor
    if floor > ivs['Defence']:
        ivs['Defence'] = floor
    if floor > ivs['Stamina']:
        ivs['Stamina'] = floor

    return ivs

async def calculateOdds(monName, extraInputs=None):
    modifiers = copy.deepcopy(defaultOddsModifiers)

    if extraInputs != None:
        modifiers, errorText = determineOddsModifierValues([str(i).strip().lower() for i in extraInputs], modifiers)
        if errorText != '':
            return errorText
        
    mon = getMonFromName(monName)

    if mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon! Don\'t you want the embed to look good?'
    
    totalIvCombos = (16 - modifiers['Floor']) ** 3

    if modifiers['BottleCap']:
        acceptableIvCombos = ((15 - modifiers['Floor']) * 3) + 1

    else:
        acceptableAttackIvs = 16 - modifiers['Ivs']['Attack']
        acceptableDefenceIvs = 16 - modifiers['Ivs']['Defence']
        acceptableStaminaIvs = 16 - modifiers['Ivs']['Stamina']

        acceptableIvCombos = acceptableAttackIvs * acceptableDefenceIvs * acceptableStaminaIvs
    
    totalProbability = acceptableIvCombos / totalIvCombos

    inverseProbability = totalIvCombos / acceptableIvCombos
    
    if modifiers['LuckyChance'] is not None:
        luckyChance = 1 / modifiers['LuckyChance']

        if modifiers['BottleCap']:
            acceptableLuckyIvCombos = ((15 - 12) * 3) + 1
        else:
            luckyIvs = raiseIvsToFloor(copy.copy(modifiers['Ivs']), 12)
            acceptableLuckyIvCombos = (16 - luckyIvs['Attack']) * (16 - luckyIvs['Defence']) * (16 - luckyIvs['Stamina'])

        luckyProbability = acceptableLuckyIvCombos / 64

        totalProbability = ((1 - luckyChance) * totalProbability) + (luckyChance * luckyProbability)

        inverseProbability = 1 / totalProbability

    extraOddsText = ''

    if modifiers['BottleCap']:
        extraOddsText += '**Silver Cappable**, '
    if modifiers['ShinyChance'] is not None:
        extraOddsText += '**Shiny**, '
        totalProbability *=  (1 / modifiers['ShinyChance'])
        inverseProbability *=  modifiers['ShinyChance']
    if modifiers['BackgroundChance'] is not None:
        extraOddsText += '**Background**, '
        totalProbability *= (1 / modifiers['BackgroundChance'])
        inverseProbability *=  modifiers['BackgroundChance']
    if modifiers['ExtraChance'] is not None:
        extraOddsText += '**Special Move**, '
        totalProbability *= (1 / modifiers['ExtraChance'])
        inverseProbability *=  modifiers['ExtraChance']
    if modifiers['LuckyChance'] is not None:
        extraOddsText += '**Potentially Lucky** '

    try:
        attemptsFor50 = math.ceil(math.log(0.5) / math.log(1 - totalProbability))

        attemptsFor95 = math.ceil(math.log(0.05) / math.log(1 - totalProbability))
    except:
        attemptsFor50 = 1
        attemptsFor95 = 1

    embed = discord.Embed(title=f'PoGo Odds Calulation for {formatTextForDisplay(mon["Name"])}',
                          description=(f'Target: {getTargetText(extraOddsText, modifiers["Ivs"], modifiers["Floor"], modifiers["BottleCap"])}\n' +
                                       f'**1/{(inverseProbability):.1f}**\n\n' +
                                       f'{attemptsFor50} attempts for a 50% chance\n' +
                                       f'{attemptsFor95} attempts for a 95% chance'),
                          color=getTypeColour((await getTypesFromPokeAPI(mon['DexNum']))[0]))
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(mon['DexNum'], rollShiny=False, forceShiny=tryingForShiny(modifiers['ShinyChance'])))
    
    return embed

        
def determineOddsModifierValues(extraInputs, modifiers):
    errorText = ''

    for input in extraInputs:
        if '/' in input:
            ivs = re.split(r'[/]+', input)
            try:
                for iv in ivs:
                    if 0 > int(iv) or int(iv) > 15:
                        raise Exception
                modifiers['Ivs']['Attack'] = int(ivs[0])
                modifiers['Ivs']['Defence'] = int(ivs[1])
                modifiers['Ivs']['Stamina'] = int(ivs[2])
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid iv combo! Format it like 15/15/15! And keep them between 0-15!\n'
        elif input.startswith('floor'):
            try:
                floorIv = int(input[5:])
                if floorIv > 15 or floorIv < 0:
                    raise Exception
                modifiers['Floor'] = floorIv
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid floor iv! Keep it between 0-15!\n'
        elif input.startswith('shiny'):
            try:
                shinyChance = int(input[5:])
                if shinyChance <= 0:
                    raise Exception
                modifiers['ShinyChance'] = shinyChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid shiny chance!\n'
        elif input.startswith('background'):
            try:
                backgroundChance = int(input[10:])
                if backgroundChance <= 0:
                    raise Exception
                modifiers['BackgroundChance'] = backgroundChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid background chance!\n'
        elif input.startswith('extra'):
            try:
                extraChance = int(input[5:])
                if extraChance <= 0:
                    raise Exception
                modifiers['ExtraChance'] = extraChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid extra chance!\n'
        elif input.startswith('lucky'):
            try:
                luckyChance = int(input[5:])
                if luckyChance <= 0:
                    raise Exception
                modifiers['LuckyChance'] = luckyChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid lucky chance!\n'
        elif input == 'bottlecap':
            modifiers['BottleCap'] = True
        
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if modifiers['LuckyChance'] is not None and (modifiers['ShinyChance'] is not None or
                                                 modifiers['BackgroundChance'] is not None or
                                                 modifiers['ExtraChance'] is not None):
        errorText += f'You can\'t specify extra conditions when trading!'

    if modifiers['BottleCap'] and (modifiers['Ivs']['Attack'] != 15 or
                                   modifiers['Ivs']['Defence'] != 15 or
                                   modifiers['Ivs']['Stamina'] != 15):
        errorText += f'You can\'t specify custom IVs when looking to bottle cap something! Don\'t be so picky, enjoy the timegate!'

    modifiers['Ivs'] = raiseIvsToFloor(modifiers['Ivs'], modifiers['Floor'])

    return modifiers, errorText
#endregion

#region track commands
async def trackMon(monName, extraInputs, author):
    if len([obj for obj in trackedMons if obj['User']['Id'] == author]) == 0:
        trackedMons.append({
            'User': {
                'Id': author,
                'Nicknames': []
            },
            'Pokemon': []
        })

    mon = getMonFromName(monName)

    if mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon!'

    toTrack, errorText = determineTracking([str(i).strip().lower() for i in extraInputs])
    if errorText != '':
        return errorText
    
    userTracked = [obj for obj in trackedMons if obj['User']['Id'] == author][0]['Pokemon']

    if len([obj for obj in userTracked if obj['DexNum'] == mon['DexNum']]) == 0:
        userTracked.append({
            'DexNum': mon['DexNum'],
            'Tracked': []
        })
    
    userTrackedMon = [obj for obj in userTracked if obj['DexNum'] == mon['DexNum']][0]

    userTrackedMon['Tracked'] = list(set(userTrackedMon['Tracked']).union(toTrack))

    await saveDataVariableToFile(pogoFileLocations.get('TrackedMons'), trackedMons)

    return f'Tracking for \'{formatTextForDisplay(monName)}\' updated!'

async def removeTrackedMon(monName, extraInputs, author):
    if len([obj for obj in trackedMons if obj['User']['Id'] == author]) == 0:
        return 'You don\'t even have anything tracked yet!'
    
    mon = getMonFromName(monName)

    if mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon!'
    
    toRemove, errorText = determineTracking([str(i).strip().lower() for i in extraInputs])
    if errorText != '':
        return errorText
    
    userTracked = [obj for obj in trackedMons if obj['User']['Id'] == author][0]['Pokemon']

    if len(userTracked) == 0:
        return 'You don\'t even have anything tracked yet!'

    if len([obj for obj in userTracked if obj['DexNum'] == mon['DexNum']]) == 0:
        return 'You don\'t have anything tracked for that pokemon!'
    
    userTrackedMon = [obj for obj in userTracked if obj['DexNum'] == mon['DexNum']][0]

    userTrackedMon['Tracked'] = list(set(userTrackedMon['Tracked']).difference(toRemove))

    if len(userTrackedMon['Tracked']) == 0:
        userTracked.remove(userTrackedMon)
    
    await saveDataVariableToFile(pogoFileLocations.get('TrackedMons'), trackedMons)

    return f'Tracking for \'{formatTextForDisplay(monName)}\' updated!'

def determineTracking(extraInputs):
    errorText = ''
    toTrack = []

    for input in extraInputs:
        if input == 'all':
            toTrack = ['hundo', 'lucky', 'shiny', 'gl', 'ul', 'shadow', 'purified', 'xxs', 'xxl']

        elif input in {'100', 'hundo', '4*'}:
            toTrack.append('hundo')

        elif input in {'lucky'}:
            toTrack.append('lucky')

        elif input in {'shiny'}:
            toTrack.append('shiny')

        elif input in {'gl', 'great'}:
            toTrack.append('gl')

        elif input in {'ul', 'ultra'}:
            toTrack.append('ul')

        elif input in {'shadow', 'rocket'}:
            toTrack.append('shadow')

        elif input in {'puri', 'purified'}:
            toTrack.append('purified')

        elif input in {'xxs', 'small', 'smol'}:
            toTrack.append('xxs')

        elif input in {'xxl', 'large', 'beeg'}:
            toTrack.append('xxl')

        else:
            errorText += f'The input \'{input}\' wasn\'t recognized!\n'

    return set(toTrack), errorText

async def addUserNickname(nickname, originalId):
    if len([obj for obj in trackedMons if obj['User']['Id'] == originalId]) == 0:
        trackedMons.append({
            'User': {
                'Id': originalId,
                'Nicknames': []
            },
            'Pokemon': []
        })

    [obj for obj in trackedMons if obj['User']['Id'] == originalId][0]['User']['Nicknames'].append(formatTextForBackend(nickname))

    await saveDataVariableToFile(pogoFileLocations.get('TrackedMons'), trackedMons)

    return f'Nickname \'{formatTextForDisplay(nickname)}\' successfully added!'

def getAuthorFromNickname(nickname):
    if len([obj for obj in trackedMons if obj['User']['Id'] == nickname]) > 0:
        return nickname
    
    for user in trackedMons:
        if formatTextForBackend(nickname) in user['User']['Nicknames']:
            return user['User']['Id']
        
    return None

def trackedSortKey(tracked):
    if tracked == 'hundo':
        return 0
    elif tracked == 'lucky':
        return 1
    elif tracked == 'shiny':
        return 2
    elif tracked == 'gl':
        return 3
    elif tracked == 'ul':
        return 4
    elif tracked == 'shadow':
        return 5
    elif tracked == 'purified':
        return 6
    elif tracked == 'xxs':
        return 7
    elif tracked == 'xxl':
        return 8
    return 0

def getTrackedEmojis(tracked, isList):
    tracked.sort(key=trackedSortKey)

    if len(tracked) == 9 and isList:
        return f'{trackedEmojis.get("all")}'

    emojiText = ''
    skipNext = False

    for i, want in enumerate(tracked):
        if skipNext:
            skipNext = False
            continue

        try:
            if want == 'gl':
                if tracked[i+1] == 'ul':
                    emojiText += f'{trackedEmojis.get("gl_ul")} '
                    skipNext = True
                else:
                    raise Exception
            elif want == 'shadow':
                if tracked[i+1] == 'purified':
                    emojiText += f'{trackedEmojis.get("shadow_purified")} '
                    skipNext = True
                else:
                    raise Exception
            elif want == 'xxs':
                if tracked[i+1] == 'xxl':
                    emojiText += f'{trackedEmojis.get("xxs_xxl")} '
                    skipNext = True
                else:
                    raise Exception
            else:
                raise Exception
        except:
            emojiText += f'{trackedEmojis.get(want)} '

    return emojiText


async def checkTrackedMon(monName, user, guild):
    mon = getMonFromName(monName)
        
    if mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon!'
    
    author = getAuthorFromNickname(user)

    if author is None:
        return 'This user doesn\'t have anything tracked!'
    
    discordUser = guild.get_member(int(author[2:-1]))

    if discordUser is None:
        return 'That user is not in your current server!'

    if len([obj for obj in trackedMons if obj['User']['Id'] == author]) == 0:
        return 'This user doesn\'t have anything tracked!'
    
    if len([obj for obj in trackedMons if obj['User']['Id'] == author][0]['Pokemon']) == 0:
        return 'This user doesn\'t have anything tracked!'

    userTracked = [obj for obj in trackedMons if obj['User']['Id'] == author][0]['Pokemon']

    if len([obj for obj in userTracked if obj['DexNum'] == mon['DexNum']]) == 0:
        return f'{formatTextForDisplay(discordUser.name)} does not need any {formatTextForDisplay(mon["Name"])}!'
    
    userTrackedMon = [obj for obj in userTracked if obj['DexNum'] == mon['DexNum']][0]

    monTypes = await getTypesFromPokeAPI(mon['DexNum'])

    pogoMon = next((dpsMon for dpsMon in pogoPokemon if dpsMon['ImageDexNum'] == mon['DexNum']), {})

    if len(pogoMon) == 0:
        monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{mon["DexNum"]}')

        if monData is None:
            return f'An error occured while checking the api!'

        stats = []

        for i in range(6):
            stats.append(int(monData['stats'][i]['base_stat']))

        pogoMon['Attack'], pogoMon['Defence'], pogoMon['Stamina'], nerfAmount = calcPoGoStatsFromBaseStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5])
    
    embed = discord.Embed(title=f'{formatTextForDisplay(mon["Name"])} tracked by {formatTextForDisplay(discordUser.name)}',
                          description=f'Attack: {pogoMon["Attack"]}\n'
                                      f'Defence: {pogoMon["Defence"]}\n'
                                      f'Stamina: {pogoMon["Stamina"]}',
                          color=getTypeColour(monTypes[0]))
    
    embed.add_field(name=getTrackedEmojis(userTrackedMon['Tracked'], False),
                    value='',
                    inline=False)
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(mon['DexNum']))

    if len([obj for obj in fakeRankOnes if obj['DexNum'] == mon['DexNum']]) > 0:
        leagues = [obj for obj in fakeRankOnes if obj['DexNum'] == mon['DexNum']][0]['Leagues']

        for league in leagues:
            if league in userTrackedMon['Tracked']:
                embed.set_footer(text='Beware of possible fake rank ones!')

    return embed

async def checkTrackedListMons(classification, filter, user, guild):
    author = getAuthorFromNickname(user)

    if author is None:
        return 'This user doesn\'t have anything tracked!'
    
    discordUser = guild.get_member(int(author[2:-1]))

    if discordUser is None:
        return 'That user is not in your current server!'
    
    if len([obj for obj in trackedMons if obj['User']['Id'] == author]) == 0:
        return 'This user doesn\'t have anything tracked!'
    
    if len([obj for obj in trackedMons if obj['User']['Id'] == author][0]['Pokemon']) == 0:
        return 'This user doesn\'t have anything tracked!'

    filter = formatTextForBackend(filter)
    classification = formatTextForBackend(classification)

    toDisplay, pageCount = determineDisplay(filter)
    if len(toDisplay) == 0:
        return f'{filter} was not not recognized as a valid search term!\nCheck `$pogo help` for valid terms!'

    userTracked = sorted([obj for obj in trackedMons if obj['User']['Id'] == author][0]['Pokemon'], key=lambda x: x['DexNum'])

    trackedList = []

    if verifyRegion(classification):
        for tracked in userTracked:
            if classification == getRegionFromDexNum(tracked['DexNum']):
                trackedToDisplay = set(tracked['Tracked']) & set(toDisplay)
                if trackedToDisplay:
                    trackedList.append({
                        'DexNum': tracked['DexNum'],
                        'Tracked': list(trackedToDisplay)
                    })
    else:
        monClassification, inverse = determineClassification(classification)
        if monClassification is None:
            return f'{classification} was not understood as a valid class of pokemon!\nCheck `$pogo help` for valid classes!'
        
        for tracked in userTracked:
            if monClassification == 'All' or inverseClassification(inverse, checkClassification(tracked['DexNum'], monClassification)):
                trackedToDisplay = set(tracked['Tracked']) & set(toDisplay)
                if trackedToDisplay:
                    trackedList.append({
                        'DexNum': tracked['DexNum'],
                        'Tracked': list(trackedToDisplay)
                    })

    if len(trackedList) == 0:
        return f'{formatTextForDisplay(discordUser.name)} does not need anything {formatTextForDisplay(filter)} from {formatTextForDisplay(classification)}!'

    embeds = []

    embed = discord.Embed(title=f'{formatTextForDisplay(classification)}, {formatTextForDisplay(filter)} Pokemon tracked by {formatTextForDisplay(discordUser.name)}',
                            description='',
                            color=sharedEmbedColours.get('Default'))
    
    fieldTitles = ['Mon', 'Tracked']
    fieldContent = ['', '']

    for i, mon in enumerate(trackedList, start=1):
        fieldContent[0] += f'{formatTextForDisplay(getMon(mon["DexNum"])["Name"])}\n'
        fieldContent[1] += f'{getTrackedEmojis(mon["Tracked"], True)}\n'
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['', '']
    
    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds

def determineDisplay(filter):
    if filter == 'all':
        return ['hundo', 'lucky', 'shiny', 'gl', 'ul', 'shadow', 'purified', 'xxs', 'xxl'], 6
    
    elif filter == 'hundo':
        return ['hundo'], 20
    
    elif filter == 'lucky':
        return ['lucky'], 20

    elif filter == 'shiny':
            return ['shiny'], 20
    
    elif filter == 'pvp':
        return ['gl', 'ul'], 20

    elif filter == 'rocket':
            return ['shadow', 'purified'], 20
    
    elif filter == 'size':
            return ['xxs', 'xxl'], 20
    
    return [], 0

def determineClassification(classification):
    inverse = False
    if classification.startswith('!'):
        inverse = True
        classification = classification[1:]

    if classification == 'all':
        return 'All', False
    elif classification in {'region', 'regional'}:
        return 'PoGoRegional', inverse
    elif classification in {'rare'}:
        return 'PoGoRare', inverse
    elif classification in {'starter', 'starters', 'firstpartner', 'first-partner'}:
        return 'Starters', inverse
    elif classification in {'baby', 'babies', 'eggs'}:
        return 'Baby', inverse
    elif classification in {'legendary', 'legends', 'legend', 'raid', 'raids'}:
        return 'Legendary', inverse
    elif classification in {'mythical', 'mythicals', 'myth'}:
        return 'Mythical', inverse
    elif classification in {'ultrabeast', 'ultrabeasts', 'ultra-beast', 'ultra-beasts', 'ub', 'ubs'}:
        return 'UltraBeast', inverse
    elif classification in {'paradox', 'paradoxes', 'past', 'future'}:
        return 'Paradox', inverse
    elif classification in {'mega', 'megas', 'ismega', 'is-mega', 'megaevo', 'megaevos', 'mega-evo', 'mega-evos', 'mega-evolution', 'mega-evolutions'}:
        return 'Mega', inverse
    elif classification in {'hasmega', 'has-mega', 'megapreevo', 'mega-pre-evo'}:
        return 'HasMega', inverse
    elif classification in {'gigantamax', 'gmax', 'g-max'}:
        return 'Gigantamax', inverse
    elif classification in {'hasgmax', 'has-gmax', 'gmaxpreevo', 'gmax-pre-evo'}:
        return 'HasGigantamax', inverse

    return None, inverse

def inverseClassification(inverse, classificationResult):
    if inverse:
        return not classificationResult
    return classificationResult
#endregion

#region go stat convert
async def convertToGoStats(stats, nerfOverride=None):
    try:
        stats = [int(obj) for obj in stats]
    except:
        return 'Not all 6 stats were numbers!'
    
    if nerfOverride is not None:
        nerfOverride = calcNerfOverride(nerfOverride)
        if (isinstance(nerfOverride, str)):
            return nerfOverride
        
    attack, defence, stamina, nerfAmount = calcPoGoStatsFromBaseStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], nerfOverride)

    lv40CP = determineCPFromBaseStat(attack, defence, stamina, 40)
    lv50CP = determineCPFromBaseStat(attack, defence, stamina, 50)

    nerfText = getNerfText(nerfAmount)

    return f'This pokemon should have the following stats{nerfText}:\nLv 40 Max CP: {lv40CP}\nLv 50 Max CP: {lv50CP}\nAttack: {attack}\nDefence: {defence}\nStamina: {stamina}'
        

async def convertToGoStatsFromName(monName, nerfOverride=None):
    dexNum = getDexNum(monName)

    if dexNum == -1:
        return f'The pokemon \'{monName}\' was not recognized!'
    
    monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{dexNum}')

    if monData is None:
        return f'An error occured while checking the api!'

    stats = []

    for i in range(6):
        stats.append(int(monData['stats'][i]['base_stat']))

    if nerfOverride is not None:
        nerfOverride = calcNerfOverride(nerfOverride)
        if (isinstance(nerfOverride, str)):
            return nerfOverride
    
    attack, defence, stamina, nerfAmount = calcPoGoStatsFromBaseStats(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], nerfOverride)

    lv40CP = determineCPFromBaseStat(attack, defence, stamina, 40)
    lv50CP = determineCPFromBaseStat(attack, defence, stamina, 50)

    nerfText = getNerfText(nerfAmount)

    return f'This pokemon should have the following stats{nerfText}:\nLv 40 Max CP: {lv40CP}\nLv 50 Max CP: {lv50CP}\nAttack: {attack}\nDefence: {defence}\nStamina: {stamina}'

def calcNerfOverride(nerfOverride):
    if nerfOverride == '9nerf':
        return 0.91
    elif nerfOverride == '3nerf':
        return 0.97
    elif nerfOverride == 'nonerf':
        return 1.00
    else:
        return f'The nerf exception \'{nerfOverride}\' was not recognized!\n`noNerf`, `3Nerf` and `9Nerf` are the only valid exceptions!'

def getNerfText(nerfAmount):
    if nerfAmount == 0.91:
        return '(After a 9% nerf)'
    elif nerfAmount == 0.97:
        return '(After a 3% nerf)'
    return ''

def determineCPFromBaseStat(attack, defence, stamina, level):
    cpMultiplier = getPoGoCPMultiplier(level)
    calculatedAttack = calcPoGoStat(attack, 15, cpMultiplier)
    calculatedDefence = calcPoGoStat(defence, 15, cpMultiplier)
    calculatedStamina = calcPoGoStat(stamina, 15, cpMultiplier)

    cp = calcPoGoCP(calculatedAttack, calculatedDefence, calculatedStamina)

    return cp
#endregion