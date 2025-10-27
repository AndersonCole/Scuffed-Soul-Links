""" 
Contains the functions relating to pogo pvp

Cole Anderson, Sep 2025
"""

import discord
from dictionaries.shared_dictionaries import sharedImagePaths
from functions.shared_functions import rollForShiny

async def pvpHelp():
    embed = discord.Embed(title=f'Shuckle\'s Pvp Commands',
                                description='```$pvp img``` Gets the pvp rank reqs image',
                                color=3553598)

    embed.set_thumbnail(url=rollForShiny(sharedImagePaths.get('Shuckle'), sharedImagePaths.get('ShinyShuckle')))
    
    return embed

async def getPvpRanksImg():
    return discord.File('images/pvp.png', filename='pvp.png')

