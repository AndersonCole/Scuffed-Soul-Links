""" 
Logs into discord as the soul link bot using the token from the textfile,
and reads and responds to messages with a certain prefix.

Cole Anderson, Dec 2023
"""
import discord
import random
import regex as re
from soul_link_functions import *
import Paginator

## MYClient Class Definition

class MyClient(discord.Client):
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
        
        if message.content[0:4] == '$sl ':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')
            input = message.content[4:]

            global version_group
            global most_recent_version_group

            global run_name

            if input[0:] == 'help':
                embed, file = await help()
                await message.channel.send(file=file, embed=embed)

            elif input[0:7] == 'new-sl ':
                if ',' in input:
                    input = re.split(r'[,]+', input[7:])
                    try:
                        game = input[0].strip()
                        name = input[1].strip()
                        input.pop(0)
                        input.pop(0)
                        if len(input) == 1:
                            input = str(input[0]).strip()
                            if ' ' in input:
                                players = re.split(r'[\s]+', input)
                                version_group, run_name, msg = await createNewRun(game, name, players)
                                if msg != 'Success':
                                    await message.channel.send(msg)
                                else:
                                    await createRole(run_name, players, message.guild)
                                    await message.channel.send('Run Created! Focus set to the newly created run')
                            else:
                                await message.channel.send("Specify more than one player!")
                        elif len(input) > 1:
                            players = [player.strip() for player in input]
                            
                            version_group, run_name, msg = await createNewRun(game, name, players)
                            if msg != 'Success':
                                await message.channel.send(msg)
                            else:
                                await createRole(run_name, players, message.guild)
                                await message.channel.send('Run Created! Focus set to the newly created run')
                        else:
                            raise Exception('Specify more than one player!')
                    except Exception as ex:
                        await message.channel.send(ex)
                else:
                    await message.channel.send("Invalid input! Use commas ',' in between values!")

            elif input[0:10] == 'encounter ':
                if ',' in input:
                    input = re.split(r'[,]+', input[10:])
                    if len(input) == 2:
                        if re.search(r'<@\d+>', input[1].strip()) is not None:
                            response = await encounterMonGroup(input[0].strip(), [input[1]], run_name)
                        else:
                            response = await encounterMon(input[0].strip(), input[1].strip(), message.author.mention, run_name)
                    elif len(input) > 2:
                        encounter_name = input[0].strip()
                        input.pop(0)
                        response = await encounterMonGroup(encounter_name, input, run_name)
                        
                    await message.channel.send(response)
                else:
                    await message.channel.send("Invalid input! Use commas ',' in between values!")

            elif input[0:14] == 'see-encounters':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    embeds = await listEncounters(run_name)

                    if(type(embeds) == type('')):
                        await message.channel.send(embeds)
                    else:
                        await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:5] == 'links':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    embeds = await listLinks(run_name)

                    if(type(embeds) == type('')):
                        await message.channel.send(embeds)
                    else:
                        await Paginator.Simple().start(message.channel, pages=embeds)
            
            elif input [0:10] == 'link-name ':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await getLinkName(run_name, str(input[10:]).strip(), message.author.mention)

                    await message.channel.send(response)

            elif input[0:10] == 'new-death ':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    if ',' in input:
                        input = re.split(r'[,]+', input[10:])
                        encounter_name = input[0].strip()
                        input.pop(0)

                        response = await newDeath(encounter_name, ','.join(word for word in input), run_name)
                            
                        await message.channel.send(response)
                    else:
                        await message.channel.send("Invalid input! Use commas ',' in between values!")
            
            elif input[0:11] == 'undo-death ':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await undoDeath(input[11:].strip(), run_name)
                        
                    await message.channel.send(response)
            
            elif input[0:6] == 'deaths':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    embeds = await listDeaths(run_name)

                    if(type(embeds) == type('')):
                        await message.channel.send(embeds)
                    else:
                        await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:11] == 'select-run ':
                version_group, run_name, msg = selectRun(input[11:].strip())

                if msg == 'Success':
                    await message.channel.send(f'Focus set to run {run_name}!')
                else:
                    await message.channel.send(msg)

            elif input[0:8] == 'see-runs':
                embeds = await listRuns()

                await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:12] == 'choose-team ':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    if ',' in input[12:]:
                        links = re.split(r'[,]+', input[12:])
                        response = await chooseTeam(run_name, links, message.author.mention)
                        await message.channel.send(response)
                    else:
                        await message.channel.send("Invalid input! Use commas ',' in between values!")

            elif input[0:7] == 'battles':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await nextBattle(run_name)
                    await message.channel.send(response)
            
            elif input[0:8] == 'progress':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await progressRun(run_name)
                    await message.channel.send(response)

            elif input[0:9] == 'add-note ':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await addNote(run_name, input[9:])
                    await message.channel.send(response)

            elif input[0:14] == 'create-reason ':
                response = await createReason(input[14:])

                await message.channel.send(response)

            elif input[0:11] == 'random-user':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await pingUser(run_name)

                    await message.channel.send(response)

            elif input[0:7] == 'win-run':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await setRunStatus(run_name, 'Victory')
                    await message.channel.send(response)

            elif input[0:8] == 'fail-run':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await setRunStatus(run_name, 'Defeat')
                    await message.channel.send(response)

            elif input[0:11] == 'undo-status':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    response = await setRunStatus(run_name, 'In Progress')
                    await message.channel.send(response)

            elif input[0:8] == 'see-info':
                if run_name == '':
                    await message.channel.send('Select a run first using $sl select-run!')
                else:
                    embeds = await seeStats(run_name)

                    if(type(embeds) == type('')):
                        await message.channel.send(embeds)
                    else:
                        await Paginator.Simple().start(message.channel, pages=embeds)                    

            elif input[0:4] == 'dex ':
                mon = input[4:]

                if version_group == '':
                    embed, file = await makePokedexEmbed(mon, most_recent_version_group)
                else:
                    embed, file = await makePokedexEmbed(mon, version_group)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(file=file, embed=embed)

            elif input[0:6] == 'catch ':
                user_inputs = re.split(r'[\s-.]+', input[6:])
                level = user_inputs[-1]
                user_inputs.pop(-1)
                mon = ' '.join(word for word in user_inputs)

                if version_group == '':
                    embed = await calculateCatchRate(mon, level, most_recent_version_group)
                else:
                    embed = await calculateCatchRate(mon, level, version_group)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(embed=embed)

            elif input[0:6] == 'moves ':
                user_inputs = re.split(r'[\s-.]+', input[6:])
                level = user_inputs[-1]
                user_inputs.pop(-1)
                mon = ' '.join(word for word in user_inputs)

                if version_group == '':
                    embed = await showMoveSet(mon, level, most_recent_version_group)
                else:
                    embed = await showMoveSet(mon, level, version_group)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(embed=embed)

            elif input[0:13] == 'add-nickname ':
                user_inputs = re.split(r'[\s-.]+', input[13:])
                dex_num = user_inputs[-1]
                user_inputs.pop(-1)
                nickname = '-'.join(word.lower() for word in user_inputs)

                response = await addNickname(nickname, dex_num)

                await message.channel.send(response)

            elif input[0:13] == 'see-nicknames':

                embed = await seeNicknames()

                await message.channel.send(embed=embed)

            elif input[0:5] == 'reset':
                version_group = ''
                run_name = ''

                await message.channel.send('Run unfocused!')

            else:
                await message.channel.send('Command not recognized. Try using ```$sl help```')
            
        #mimikyu format command
        elif message.content[0:8] == "$format ":
            input = message.content[8:]
            try:
                if ',' in input:
                    input = str(input).split(",")
                    name = str(input[0]).strip()
                    next_name = str(input[1]).strip()
                    level_cap = int(input[2])
                    input.pop(0)
                    input.pop(0)
                    input.pop(0)
                    encounters = []
                    for text in input:
                        encounters.append(str(text).strip())

                    encounters_text = '['
                    if encounters == []:
                        encounters_text += ']'
                    for encounter in encounters:
                        if encounter == encounters[-1]:
                            encounters_text += f'\'{encounter}\']'
                        else:
                            encounters_text += f'\'{encounter}\', '
                        
                    await message.channel.send('{' + f'\'Stage\': , \'Name\': \'{name}\', \'Battle-Name\': \'{next_name}\', \'Level-Cap\': {level_cap}, \'Encounters\': {encounters_text}' + '}')
                    await message.delete()
                else:
                    raise Exception()
            except:
                await message.channel.send("U fucked something up. Only send messages like this ```$format Gym 1, Misty, 20, Route 3, Route 4``` In this order, Name of the previous battle ex. Gym 1, name of the next battle ex. Gym 2 or Misty, level cap for the next battle, encounters before the next battle.")


version_group = ''
most_recent_version_group = 'scarlet-violet'

run_name = ''

## Set up and log in
client = MyClient()
with open("tokens/bot_token.txt") as file:
    token = file.read()
client.run(token)