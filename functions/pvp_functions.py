""" 
Contains the functions relating to pogo pvp

Cole Anderson, Sep 2025
"""

import discord
import random
from dictionaries.shared_dictionaries import sharedImagePaths

async def pvpHelp():
    embed = discord.Embed(title=f'Shuckle\'s Pvp Commands',
                                description='```$pvp img``` Gets the pvp rank reqs image',
                                color=3553598)

    rand_num = random.randint(1, 100)
    if rand_num == 69:
        embed.set_thumbnail(url=sharedImagePaths.get('ShinyShuckle'))
    else: 
        embed.set_thumbnail(url=sharedImagePaths.get('Shuckle'))
    
    return embed

async def getPvpRanksImg():
    return discord.File('images/pvp.png', filename='pvp.png')

