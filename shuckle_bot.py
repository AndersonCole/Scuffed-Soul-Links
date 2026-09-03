import discord
from functions.shared_functions import assignReactionEmoji, loadDataVariableFromFile, formatTextForBackend
from dictionaries.shared_dictionaries import sharedFileLocations
from commands.misc_commands import miscShuckleCommands
from commands.soul_link_commands import soulLinkCommands
from commands.routes_commands import routesCommands
from commands.dps_commands import dpsCommands, maxCommands
from commands.pogo_commands import pogoMiscCommands
from commands.pvp_commands import pvpCommands
from commands.mc_commands import minecraftCommands
from util.shuckle_paginator import ShucklePaginator

class DiscordClient(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        
        if message.author == self.user:
            return
        
        response = None
        file = None

        if message.content.startswith('$'):
            message.content = message.content.lower()

        elif 'is about to be grinded into kakera by **anderson499**' in message.content:
            await message.add_reaction(assignReactionEmoji('Shuckle'))

            response = await miscShuckleCommands('mudae ' + message.content)

        #region bot commands
        if message.content.startswith('$shuckle'):
            await message.add_reaction(assignReactionEmoji('Shuckle'))

            userCommand = message.content[len('$shuckle'):].lstrip('-, ')
            
            response = await miscShuckleCommands(userCommand, message.author, message.guild)

        elif message.content.startswith('$sl'):
            await message.add_reaction(assignReactionEmoji('Soul Links'))

            userCommand = message.content[len('$sl'):].lstrip('-, ')

            response = await soulLinkCommands(userCommand, message.author, message.guild)

        elif message.content.startswith('$routes'):
            await message.add_reaction(assignReactionEmoji('Routes'))

            userCommand = message.content[len('$routes'):].lstrip('-, ')

            response = await routesCommands(userCommand, message.author, message.guild)

        elif message.content.startswith('$dps'):
            await message.add_reaction(assignReactionEmoji('DPS'))

            userCommand = message.content[len('$dps'):].lstrip('-, ')

            response, file = await dpsCommands(userCommand, message.author)

        elif message.content.startswith('$max'):
            await message.add_reaction(assignReactionEmoji('Max'))

            userCommand = message.content[len('$max'):].strip('-, ')

            response, file = await maxCommands(userCommand, message.author)

        elif message.content.startswith('$pogo'):
            await message.add_reaction(assignReactionEmoji('PoGo'))

            userCommand = message.content[len('$pogo'):].strip('-, ')

            response = await pogoMiscCommands(userCommand, message.author, message.guild)

        elif message.content.startswith('$pvp'):
            await message.add_reaction(assignReactionEmoji('PVP'))

            userCommand = message.content[len('$pogo'):].strip('-, ')

            response = await pvpCommands(userCommand, message.author)

        elif message.content.startswith('$mc'):
            await message.add_reaction(assignReactionEmoji('Minecraft'))

            userCommand = message.content[len('$mc'):].strip('-, ')

            response = await minecraftCommands(userCommand, message.author)

        elif message.content == '$coins':
            await message.add_reaction(assignReactionEmoji('Coins'))

            response = await miscShuckleCommands(message.content[1:])

        elif message.content.startswith('$format'):
            await message.add_reaction(assignReactionEmoji('Mimikyu'))

            response = await miscShuckleCommands(message.content[1:])
        #endregion

        if response is not None:
            if (isinstance(response, str)):
                await message.channel.send(response)
            elif (isinstance(response, discord.File)):
                await message.channel.send(file=response)
            elif (isinstance(response, discord.Embed)):
                if file is not None:
                    await message.channel.send(embed=response, file=file)
                else:
                    await message.channel.send(embed=response)
            elif (isinstance(response, list)):
                #handles list[discord.Embed] and list[tuple(discord.Embed, bytes, str, str)]
                await ShucklePaginator().start(message.channel, pages=response)

## Set up and log in
if __name__ == "__main__":
    client = DiscordClient()
    client.run(loadDataVariableFromFile(sharedFileLocations.get('BotToken'), readJson=False))