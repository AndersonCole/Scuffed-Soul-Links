""" 
Contains the functions relating to PoGo events

Cole Anderson, Aug 2025
"""

import discord
import requests
import copy
import random
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from dictionaries.shared_dictionaries import sharedImagePaths
from dictionaries.pogo_event_dictionaries import eventColours, filterLists, timezones
from functions.shared_functions import formatTextForDisplay

#region help command
async def eventsHelp():
    file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
    shinyFile = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')

    embed = discord.Embed(title='Shuckles PoGo Event Commands',
                            description='```$pogo events``` Shows upcoming and current events\n' +
                                        '```$pogo commDays``` Shows upcoming community days\n' +
                                        '```$pogo hourEvents``` Shows Max Mondays, Spotlight Hours and Raid Hours\n' +
                                        '```$pogo raids``` Shows upcoming raid boss changovers, and other raid events\n' +
                                        '```$pogo gbl``` Shows upcoming GBL league rotations\n\n' +
                                        'All data is scraped from LeekDuck', 
                            color=3553598)

    embed.set_author(name='Data Source', url='https://github.com/bigfoott/ScrapedDuck')

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url='attachment://shiny_swole_shuckle.png')
        return embed, shinyFile
    else:
        embed.set_thumbnail(url='attachment://swole_shuckle.png')
        return embed, file
    
#endregion

#region commands
async def retrieveEventsFromAPI(eventFilterList):
    events = (requests.get(f'https://raw.githubusercontent.com/bigfoott/ScrapedDuck/data/events.json')).json()
    sortedEvents = sorted(events, key=lambda x: x['start'], reverse=False)

    filteredEvents = []
    for event in sortedEvents:
        if event['eventType'] in eventFilterList:
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
    if length > 50:
        return '\n'
    return ''

async def createEventsEmbeds(filterFor):
    filterList = filterLists.get(filterFor.lower().strip(), None)
    if filterList is None:
        return 'I don\'t understand what events you\'re trying to get info on!\n\nCheck `$pogo help` to see all valid searches!'
    
    events = await retrieveEventsFromAPI(filterList)

    if len(events) == 0:
        return 'There was no data on the requested events!'
    
    embeds = []
    
    embed = discord.Embed()

    firstEmbed = discord.Embed(title='Upcoming PoGo Events',
                                color=eventColours.get(filterFor.lower().strip(), 3553598))
    firstEmbed.set_author(name='More Info at LeekDuck', url='https://leekduck.com/events')

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        firstEmbed.set_thumbnail(url=sharedImagePaths.get('ShinyShuckle'))
        embed.set_thumbnail(url=sharedImagePaths.get('ShinyShuckle'))
    else: 
        firstEmbed.set_thumbnail(url=sharedImagePaths.get('Shuckle'))
        embed.set_thumbnail(url=sharedImagePaths.get('Shuckle'))

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

        embed.colour = eventColours.get(event['eventType'], 3553598)

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