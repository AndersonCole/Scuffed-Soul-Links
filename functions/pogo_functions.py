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
from fractions import Fraction
from dictionaries.shared_dictionaries import sharedImagePaths, sharedEmbedColours
from dictionaries.pogo_dictionaries import eventColours, filterLists, timezones, defaultOddsModifiers
from functions.shared_functions import (
    formatTextForDisplay, getMonFromName, getPokeAPISpriteUrl, getTypesFromPokeAPI, getTypeColour, rollForShiny, pokemon
)

#region help command
async def pogoHelp():
    embed = discord.Embed(title='Shuckles PoGo Commands',
                            description='```$pogo events``` Shows upcoming and current events. All event data is scraped from LeekDuck\n' +
                                        '```$pogo commDays``` Shows upcoming community days\n' +
                                        '```$pogo hourEvents``` Shows Max Mondays, Spotlight Hours and Raid Hours\n' +
                                        '```$pogo raids``` Shows upcoming raid boss changovers, and other raid events\n' +
                                        '```$pogo gbl``` Shows upcoming GBL league rotations\n\n' +
                                        '```$pogo odds Shuckle``` Shows the odds of getting something\n' +
                                        '```$pogo odds modifiers``` Lists out all the available odds modifers\n',
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

#odds command
def oddsModifiers():
    embed = discord.Embed(title='Shuckles PoGo Odds Modifiers',
                            description='```$pogo odds Shuckle, 15/15/15``` IVs: Sets the minimum acceptable IVs\n' +
                                        '```$pogo odds Shuckle, Floor10``` Floor: Sets the iv floor of the encounter\n\n' +
                                        '```$pogo odds Shuckle, ShinyChance20``` ShinyChance: Sets the odds of getting a shiny\n' +
                                        '```$pogo odds Shuckle, BackgroundChance10``` BackgroundChance: Sets the odds of getting a background\n' +
                                        '```$pogo odds Shuckle, ExtraChance10``` ExtraChance: Sets the odds of getting something extra, like a special move\n\n' +
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
    return f'{extraText} and '

def tryingForShiny(shinyChance):
    if shinyChance is not None:
        return True
    return False

async def calculateOdds(monName, extraInputs=None):
    modifiers = copy.deepcopy(defaultOddsModifiers)

    if extraInputs != None:
        modifiers, errorText = determineModifierValues([str(i).strip().lower() for i in extraInputs], modifiers)
        if errorText != '':
            return errorText
        
    mon = getMonFromName(monName)

    if mon is None:
        return f'\'{monName}\' was not recognized as a valid pokemon! Don\'t you want the embed to look good?'
    
    totalIvCombos = (16 - modifiers['Floor']) ** 3
    
    acceptableAttackIvs = 16 - modifiers['Ivs']['Attack']
    acceptableDefenceIvs = 16 - modifiers['Ivs']['Defence']
    acceptableStaminaIvs = 16 - modifiers['Ivs']['Stamina']

    acceptableIvCombos = acceptableAttackIvs * acceptableDefenceIvs * acceptableStaminaIvs

    totalProbability = acceptableIvCombos / totalIvCombos

    inverseProbability = totalIvCombos / acceptableIvCombos

    extraOddsText = ''

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

    attemptsFor50 = math.ceil(math.log(0.5) / math.log(1 - totalProbability))

    attemptsFor95 = math.ceil(math.log(0.05) / math.log(1 - totalProbability))

    embed = discord.Embed(title=f'PoGo Odds Calulation for {formatTextForDisplay(mon["Name"])}',
                          description=(f'Target: {getExtraText(extraOddsText)}{getIvText(modifiers["Ivs"])}\n' +
                                       f'**1/{(inverseProbability):.1f}**\n\n' +
                                       f'{attemptsFor50} attempts for a 50% chance\n' +
                                       f'{attemptsFor95} attempts for a 95% chance'),
                          color=getTypeColour((await getTypesFromPokeAPI(mon['DexNum']))[0]))
    
    embed.set_thumbnail(url=getPokeAPISpriteUrl(mon['DexNum'], rollShiny=False, forceShiny=tryingForShiny(modifiers['ShinyChance'])))
    
    return embed

        
def determineModifierValues(extraInputs, modifiers):
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
        elif input.startswith('shinychance'):
            try:
                shinyChance = int(input[11:])
                modifiers['ShinyChance'] = shinyChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid shiny chance!\n'
        elif input.startswith('backgroundchance'):
            try:
                backgroundChance = int(input[16:])
                modifiers['BackgroundChance'] = backgroundChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid background chance!\n'
        elif input.startswith('extrachance'):
            try:
                extraChance = int(input[11:])
                modifiers['ExtraChance'] = extraChance
            except:
                errorText += f'\'{input}\' wasn\'t understood as a valid extra chance!\n'
        
        else:
            errorText += f'The input \'{input}\' was not understood!\n'

    if modifiers['Floor'] > modifiers['Ivs']['Attack']:
        modifiers['Ivs']['Attack'] = modifiers['Floor']
    if modifiers['Floor'] > modifiers['Ivs']['Defence']:
        modifiers['Ivs']['Defence'] = modifiers['Floor']
    if modifiers['Floor'] > modifiers['Ivs']['Stamina']:
        modifiers['Ivs']['Stamina'] = modifiers['Floor']

    return modifiers, errorText
#endregion