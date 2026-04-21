import discord
import copy
from datetime import datetime
from functions.shared_functions import loadDataVariableFromFile, saveDataVariableToFile, addPaginatedEmbedFields
from dictionaries.routes_dictionaries import routesFileLocations, routesImagePaths, routesEmbedColour

routes = loadDataVariableFromFile(routesFileLocations.get('Routes'))

walkedRoutes = loadDataVariableFromFile(routesFileLocations.get('WalkedRoutes'))

async def checkStrongestSoldier(userId, guild):
    user = guild.get_member(userId)
    role = discord.utils.get(guild.roles, name="Routes Strongest Soldier")

    if role in user.roles:
        return True
    return False

async def routesHelp():
    embed = discord.Embed(title=f'Routes Strongest Soldier\'s Commands',
                          description='```$routes add Best Route, 501, 0``` Creates a new route from the name, distance and times walked given\n' +
                                      '```$routes walk Best Route, 480, R, 1``` Logs a walked route from the name, distance, direction (Normal or Reverse) and cells found\n' +
                                      '```$routes list``` Lists all the routes you\'ve added\n' +
                                      '```$routes today``` Lists out all the routes you completed today\n' +
                                      '```$routes stats``` Lists out all the stats for every route you\'ve made', 
                          color=routesEmbedColour)
    
    embed.set_thumbnail(url=routesImagePaths.get('ZygardeCell'))
    
    return embed

#region text parsing functions
def getRoute(routeName, user):
    try:
        return [obj for obj in routes if obj['Name'].lower() == routeName.lower() and obj['User'] == user][0]
    except:
        return None

def getBadgeLevel(count):
    if count >= 100:
        return 'Gold'
    elif count >= 20:
        return 'Silver'
    elif count >= 5:
        return 'Bronze'
    else:
        return 'No'

def getCellPercentage(timesWalked, cellCount):
    try:
        return f'{((cellCount/timesWalked)*100):.1f}%'
    except:
        return 'None found'

def getDirection(direction):
    if str(direction[0]).lower() == 'r':
        return 'Reversed'
    return 'Normal'
#end region

#region routes commands
async def addRoute(routeName, distance, timesWalked, user):
    routes.append({
        'Name': routeName,
        'Distance': distance,
        'TimesWalked': timesWalked,
        'User': user
    })

    await saveDataVariableToFile(routesFileLocations.get('Routes'), routes)

    return 'Route added successfully!'

async def walkRoute(routeName, distance, direction, cellCount, user):

    routeData = getRoute(routeName, user)

    if routeData == None:
        return 'The name of the route was invalid, or you were not the one who created this route!'
    
    currentDate = datetime.now().date().strftime("%Y-%m-%d")

    walkedRoutes.append({
        'Name': routeData['Name'],
        'Cells': cellCount,
        'Distance': distance,
        'Direction': direction,
        'BadgeLevel': getBadgeLevel(routeData['TimesWalked'] + 1),
        'Date': currentDate,
        'User': user
    })

    [obj for obj in routes if obj['Name'].lower() == routeName.lower() and obj['User'] == user][0]['TimesWalked'] += 1

    await saveDataVariableToFile(routesFileLocations.get('WalkedRoutes'), walkedRoutes)
    await saveDataVariableToFile(routesFileLocations.get('Routes'), routes)

    todayCellCount = 0
    todaysRoutes = [obj for obj in walkedRoutes if obj['Date'] == currentDate and obj['User'] == user]

    for route in todaysRoutes:
        todayCellCount += route['Cells']

    if(todayCellCount == 3):
        return 'Route logged. Good work out there soldier, Zygarde rewards your efforts!'

    return 'Route logged. Continue on soldier.'
#endregion

#region printouts
async def listRoutes(user):
    usersRoutes = [obj for obj in routes if obj['User'] == user]

    if len(usersRoutes) == 0:
        return 'You haven\'t created any routes yet! Use ```$routes help``` to get started! Zygarde needs YOU!', None

    embeds = []

    embed = discord.Embed(title=f'Routes',
                          description=f'{user}',
                          color=routesEmbedColour)
    
    embed.set_thumbnail(url=routesImagePaths.get('ZygardeCell'))

    fieldTitles = ['']
    fieldContent = ['']

    pageCount = 20
    for i, route in enumerate(usersRoutes, start=1):
        fieldContent[0] += f'{route["Name"]}\n'

        if i % pageCount == 0:
                embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
                fieldContent = ['']

    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)

    return embeds

async def printoutDay(user):
    todaysRoutes = [obj for obj in walkedRoutes if obj['Date'] == datetime.now().date().strftime("%Y-%m-%d") and obj['User'] == user]

    if len(todaysRoutes) == 0:
        return 'No routes logged today! Get out there soldier, Zygarde needs YOUR help to destroy ML!', None

    embed = discord.Embed(title=f'Today\'s Routes',
                          description=f'{user}',
                          color=routesEmbedColour)
    
    routesText = ''

    for todayRoute in todaysRoutes:
        route = [obj for obj in routes if obj['Name'] == todayRoute['Name'] and obj['User'] == user][0]

        routesText += (f'Name: {todayRoute["Name"]}\n'
                          f'Distance: {todayRoute["Distance"]}m/{route["Distance"]}m\n'
                          f'Direction: {getDirection(todayRoute["Direction"])}\n'
                          f'Cells: {todayRoute["Cells"]}\n'
                          f'Badge Level: {getBadgeLevel(route["TimesWalked"])}\n\n')

    embed.add_field(name='',
                    value=routesText,
                    inline=True)

    embed.set_thumbnail(url=routesImagePaths.get('ZygardeCell'))

    return embed

async def printoutRoutes(user):
    embeds = []

    usersRoutes = [obj for obj in routes if obj['User'] == user]

    if len(usersRoutes) == 0:
        return 'You haven\'t created any routes yet! Use `$routes help` to get started! Zygarde needs YOU!'

    sortedRoutes = sorted(usersRoutes, key=lambda x: x['TimesWalked'], reverse=True)

    for route in sortedRoutes:
        embed = discord.Embed(title=f'{route["Name"]}',
                        description=f'Stats for {route["User"]}',
                        color=routesEmbedColour)
        
        timesWalked = [0, 0, 0, 0]
        cellCount = [0, 0, 0, 0]

        for walked in walkedRoutes:
            if walked['Name'] == route['Name'] and walked['User'] == route['User']:
                if walked['BadgeLevel'] == 'Bronze':
                    timesWalked[1] += 1
                    cellCount[1] += walked['Cells']
                elif walked['BadgeLevel'] == 'Silver':
                    timesWalked[2] += 1
                    cellCount[2] += walked['Cells']
                elif walked['BadgeLevel'] == 'Gold':
                    timesWalked[3] += 1
                    cellCount[3] += walked['Cells']
                else:
                    timesWalked[0] += 1
                    cellCount[0] += walked['Cells']

        if sum(timesWalked) > 0:
            statsText = (f'Route Distance: {route["Distance"]}m\n'
                            f'Times Walked: {sum(timesWalked)}\n'
                            f'Total Cells: {sum(cellCount)}\n\n'
                            f'Cell% No Badge: {getCellPercentage(timesWalked[0], cellCount[0])}\n'
                            f'Cell% Bronze Badge: {getCellPercentage(timesWalked[1], cellCount[1])}\n'
                            f'Cell% Silver Badge: {getCellPercentage(timesWalked[2], cellCount[2])}\n'
                            f'Cell% Gold Badge: {getCellPercentage(timesWalked[3], cellCount[3])}\n'
                            f'Cell% Overall: {getCellPercentage(sum(timesWalked), sum(cellCount))}')

            embed.add_field(name='',
                            value=statsText,
                            inline=True)
            
            badge = getBadgeLevel(route['TimesWalked'])

            embed.set_thumbnail(url=routesImagePaths.get(f'{badge}Badge'))

            embeds.append(copy.deepcopy(embed))

            embed.clear_fields()

    if len(embeds) > 0:
        return embeds
    else:
        return 'You haven\'t walked any routes yet! Get out there soldier, Zygarde needs YOUR help to destroy ML!'
#endregion