""" 
Contains the functions relating to routes. 
Usually returns data in a discord embed

Cole Anderson, Apr 2024
"""

import discord
import copy
from datetime import datetime
from functions.shared_functions import loadDataVariableFromFile, saveDataVariableToFile
from dictionaries.routes_dictionaries import routesFileLocations, routesImagePaths

routes = loadDataVariableFromFile(routesFileLocations.get('Routes'))

walkedRoutes = loadDataVariableFromFile(routesFileLocations.get('WalkedRoutes'))

async def checkStrongestSoldier(user_id, guild):
    user = guild.get_member(user_id)
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
                          color=9029154)
    
    embed.set_thumbnail(url=routesImagePaths.get('ZygardeCell'))
    
    return embed

#region text parsing functions
def getRoute(route_name, user):
    try:
        return [obj for obj in routes if obj['Name'].lower() == route_name.lower() and obj['User'] == user][0]
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

def getCellPercentage(times_walked, cell_count):
    try:
        return f'{((cell_count/times_walked)*100):.1f}%'
    except:
        return 'None found'

def getDirection(direction):
    if str(direction[0]).lower() == 'r':
        return 'Reversed'
    return 'Normal'
#end region

#region routes commands
async def addRoute(route_name, distance, times_walked, user):
    routes.append({
        'Name': route_name,
        'Distance': distance,
        'TimesWalked': times_walked,
        'User': user
    })

    await saveDataVariableToFile(routesFileLocations.get('Routes'), routes)

    return 'Route added successfully!'

async def walkRoute(route_name, distance, direction, cell_count, user):

    route_data = getRoute(route_name, user)

    if route_data == None:
        return 'The name of the route was invalid, or you were not the one who created this route!'
    
    currentDate = datetime.now().date().strftime("%Y-%m-%d")

    walkedRoutes.append({
        'Name': route_data['Name'],
        'Cells': cell_count,
        'Distance': distance,
        'Direction': direction,
        'BadgeLevel': getBadgeLevel(route_data['TimesWalked'] + 1),
        'Date': currentDate,
        'User': user
    })

    [obj for obj in routes if obj['Name'].lower() == route_name.lower() and obj['User'] == user][0]['TimesWalked'] += 1

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
    users_routes = [obj for obj in routes if obj['User'] == user]

    if len(users_routes) == 0:
        return 'You haven\'t created any routes yet! Use ```$routes help``` to get started! Zygarde needs YOU!', None

    embed = discord.Embed(title=f'Routes',
                          description=f'{user}',
                          color=9029154)
    
    routes_string = ''

    for route in users_routes:
        routes_string += f'{route["Name"]}\n'

    embed.add_field(name='',
                    value=routes_string,
                    inline=True)

    embed.set_thumbnail(url=routesImagePaths.get('ZygardeCell'))

    return embed

async def printoutDay(user):
    todays_routes = [obj for obj in walkedRoutes if obj['Date'] == datetime.now().date().strftime("%Y-%m-%d") and obj['User'] == user]

    if len(todays_routes) == 0:
        return 'No routes logged today! Get out there soldier, Zygarde needs YOUR help to destroy ML!', None

    embed = discord.Embed(title=f'Today\'s Routes',
                          description=f'{user}',
                          color=9029154)
    
    routes_string = ''

    for today_route in todays_routes:
        route = [obj for obj in routes if obj['Name'] == today_route['Name'] and obj['User'] == user][0]

        routes_string += (f'Name: {today_route["Name"]}\n'
                          f'Distance: {today_route["Distance"]}m/{route["Distance"]}m\n'
                          f'Direction: {getDirection(today_route["Direction"])}\n'
                          f'Cells: {today_route["Cells"]}\n'
                          f'Badge Level: {getBadgeLevel(route["TimesWalked"])}\n\n')

    embed.add_field(name='',
                    value=routes_string,
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
                        color=9029154)
        
        no_badge_walked = 0
        no_badge_cells = 0
        bronze_walked = 0
        bronze_cells = 0
        silver_walked = 0
        silver_cells = 0
        gold_walked = 0
        gold_cells = 0

        for walked in walkedRoutes:
            if walked['Name'] == route['Name'] and walked['User'] == route['User']:
                if walked['BadgeLevel'] == 'Bronze':
                    bronze_walked += 1
                    bronze_cells += walked['Cells']
                elif walked['BadgeLevel'] == 'Silver':
                    silver_walked += 1
                    silver_cells += walked['Cells']
                elif walked['BadgeLevel'] == 'Gold':
                    gold_walked += 1
                    gold_cells += walked['Cells']
                else:
                    no_badge_walked += 1
                    no_badge_cells += walked['Cells']
        
        times_walked = no_badge_walked + bronze_walked + silver_walked + gold_walked
        total_cells = no_badge_cells + bronze_cells + silver_cells + gold_cells

        if times_walked > 0:
            stats_string = (f'Route Distance: {route["Distance"]}m\n'
                            f'Times Walked: {times_walked}\n'
                            f'Total Cells: {total_cells}\n\n'
                            f'Cell% No Badge: {getCellPercentage(no_badge_walked, no_badge_cells)}\n'
                            f'Cell% Bronze Badge: {getCellPercentage(bronze_walked, bronze_cells)}\n'
                            f'Cell% Silver Badge: {getCellPercentage(silver_walked, silver_cells)}\n'
                            f'Cell% Gold Badge: {getCellPercentage(gold_walked, gold_cells)}\n'
                            f'Cell% Overall: {getCellPercentage(times_walked, total_cells)}')

            embed.add_field(name='',
                            value=stats_string,
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