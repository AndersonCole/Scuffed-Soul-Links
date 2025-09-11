""" 
Logs into discord as the soul link bot using the token from the textfile,
and reads and responds to messages with a certain prefix.

Cole Anderson, Dec 2023
"""
import discord
from functions.shared_functions import assignReactionEmoji
from commands.misc_commands import miscShuckleCommands
from commands.soul_link_commands import soulLinkCommands
from commands.routes_commands import routesCommands
from commands.dps_commands import dpsCommands, maxCommands
from commands.pogo_event_commands import pogoEventCommands
from commands.pvp_commands import pvpCommands
from commands.mc_commands import minecraftCommands
import Paginator

class DiscordClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return
        
        response = None
        file = None

        #region bot commands
        if message.content.startswith('$shuckle '):
            await message.add_reaction(assignReactionEmoji('Shuckle'))
            
            response = await miscShuckleCommands(message.content[9:], message.author, message.guild)

        elif message.content.startswith('$sl '):
            await message.add_reaction(assignReactionEmoji('Soul Links'))

            response, file = await soulLinkCommands(message.content[4:], message.author, message.guild)

        elif message.content.startswith('$routes '):
            await message.add_reaction(assignReactionEmoji('Routes'))
            
            response = await routesCommands(message.content[8:], message.author, message.guild)

        elif message.content.startswith('$dps '):
            await message.add_reaction(assignReactionEmoji('DPS'))
            
            response, file = await dpsCommands(message.content[5:], message.author)

        elif message.content.startswith('$max '):
            await message.add_reaction(assignReactionEmoji('Max'))

            response, file = await maxCommands(message.content[5:])

        elif message.content.startswith('$pogo '):
            await message.add_reaction(assignReactionEmoji('PoGo'))

            response = await pogoEventCommands(message.content[6:])

        elif message.content.startswith('$pvp '):
            await message.add_reaction(assignReactionEmoji('PVP'))

            response = await pvpCommands(message.content[5:])

        elif message.content.startswith('$mc '):
            await message.add_reaction(assignReactionEmoji('Minecraft'))

            response = await minecraftCommands(message.content[4:], message.author)

        elif message.content == '$coins':
            await message.add_reaction(assignReactionEmoji('Coins'))

            response = await miscShuckleCommands(message.content[1:])

        elif message.content.startswith('$format '):
            await message.add_reaction(assignReactionEmoji('Mimikyu'))

            response = await miscShuckleCommands(message.content[1:])

        elif 'is about to be grinded into kakera by **anderson499**' in message.content:
            await message.add_reaction(assignReactionEmoji('Shuckle'))

            response = await miscShuckleCommands('mudae ' + message.content)
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
                await Paginator.Simple().start(message.channel, pages=response)

## Set up and log in
if __name__ == "__main__":
    client = DiscordClient()
    with open('tokens/bot_token.txt') as file:
        token = file.read()
    client.run(token)