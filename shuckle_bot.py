""" 
Logs into discord as the soul link bot using the token from the textfile,
and reads and responds to messages with a certain prefix.

Cole Anderson, Dec 2023
"""
import discord
import random
import regex as re
from functions.soul_link_functions import *
from functions.routes_functions import *
from functions.dps_functions import *
from functions.mc_server_functions import *
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

        #region bot commands
        if message.content[0:14] == '$shuckle help':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')

            embed = discord.Embed(title=f'Shuckle Bot Commands',
                                description='```$sl help``` Shows all the soul link commands\n' +
                                            '```$routes help``` Shows all the routes commands\n' +
                                            '```$dps help``` Shows all the PoGo dps commands\n' +
                                            '```$max help``` Shows all the PoGo dynamax commands\n' +
                                            '```$mc help``` Shows all minecraft server commands\n' +
                                            '```$format help``` Shows how to call the mimikyu format command\n' +
                                            '```$pvp``` Brings up the pvp rank reqs image',
                                color=3553598)

            rand_num = random.randint(1, 100)
            if rand_num == 69:
                file = discord.File('images/shiny_swole_shuckle.png', filename='shiny_swole_shuckle.png')
                embed.set_thumbnail(url='attachment://shiny_swole_shuckle.png')
            else: 
                file = discord.File('images/swole_shuckle.png', filename='swole_shuckle.png')
                embed.set_thumbnail(url='attachment://swole_shuckle.png')
            
            await message.channel.send(embed=embed, file=file)

        #region soul links
        elif message.content[0:4] == '$sl ':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')
            input = message.content[4:]

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
                        if len(input) == 1 and ' ' in input:
                            players = re.split(r'[\s]+', input[0].strip())
                            
                        elif len(input) > 1:
                            players = [player.strip() for player in input]
                            
                        else:
                            raise Exception('Specify more than one player!\nIf you\'re trying to just do a nuzlocke, set Shuckle as player 2!')
                        
                        response = await createNewRun(game, name, players)
                        if response != 'Success':
                            await message.channel.send(response)
                        else:
                            await createRole(players, message.guild)
                            await message.channel.send('Run Created! Focus set to the newly created run')

                    except Exception as ex:
                        await message.channel.send(ex)
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')

            elif input[0:10] == 'encounter ':
                if ',' in input:
                    input = re.split(r'[,]+', input[10:])
                    if len(input) == 2:
                        if re.search(r'<@\d+>', input[1].strip()) is not None:
                            response = await encounterMonGroup(input[0].strip(), [input[1]])
                        else:
                            response = await encounterMon(input[0].strip(), input[1].strip(), message.author.mention)
                    elif len(input) > 2:
                        encounter_name = input[0].strip()
                        input.pop(0)
                        response = await encounterMonGroup(encounter_name, input)
                        
                    await message.channel.send(response)
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')

            elif input[0:10] == 'encounters':
                embeds = await listEncounters()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:5] == 'links':
                embeds = await listLinks()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)
            
            elif input[0:10] == 'link-data ':
                if re.search(r'<@\d+>', input[10:].strip()) is not None:
                    input = re.split(r'[\s]+', input[10:])
                    player_name = input[0]
                    input.pop(0)
                    input = ' '.join(word for word in input)
                    embed = await getLinkData(str(input).strip(), player_name)
                else:
                    embed = await getLinkData(str(input[10:]).strip(), message.author.mention)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(embed=embed)

            elif input[0:7] == 'evolve ':
                response = await evolveMon(str(input[7:]).strip(), message.author.mention)

                await message.channel.send(response)

            elif input[0:12] == 'undo-evolve ':
                response = await undoEvolveMon(str(input[12:]).strip(), message.author.mention)

                await message.channel.send(response)

            elif input[0:6] == 'death ':
                if ',' in input:
                    input = re.split(r'[,]+', input[10:])
                    encounter_name = input[0].strip()
                    input.pop(0)

                    response = await newDeath(encounter_name, ','.join(word for word in input))
                        
                    await message.channel.send(response)
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')
            
            elif input[0:11] == 'undo-death ':
                response = await undoDeath(input[11:].strip())
                    
                await message.channel.send(response)
            
            elif input[0:6] == 'deaths':
                embeds = await listDeaths()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:11] == 'select-run ':
                response = selectRun(input[11:].strip())

                await message.channel.send(response)

            elif input[0:4] == 'runs':
                embeds = await listRuns()

                await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:12] == 'choose-team ':
                if ',' in input[12:]:
                    links = re.split(r'[,]+', input[12:])
                    response = await chooseTeam(links, message.author.mention)
                    await message.channel.send(response)
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')

            elif input[0:11] == 'next-battle':
                response = await nextBattle()

                await message.channel.send(response)
            
            elif input[0:8] == 'progress':
                response = await progressRun()

                await message.channel.send(response)

            elif input[0:9] == 'add-note ':
                response = await addNote(input[9:])

                await message.channel.send(response)

            elif input[0:12] == 'ask-shuckle ':
                response = await askShuckle(input[14:])

                await message.channel.send(response)

            elif input[0:6] == 'random':
                response = await pingUser()

                await message.channel.send(response)

            elif input[0:7] == 'win-run':
                response = await setRunStatus('Victory', message.guild)

                await message.channel.send(response)

            elif input[0:8] == 'fail-run':
                response = await setRunStatus('Defeat', message.guild)

                await message.channel.send(response)

            elif input[0:11] == 'undo-status':
                response = await setRunStatus('In Progress', message.guild)
                
                await message.channel.send(response)

            elif input[0:8] == 'run-info':
                embeds = await seeStats()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)                    

            elif input[0:4] == 'dex ':
                mon = input[4:]

                embed, file = await makePokedexEmbed(mon)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(file=file, embed=embed)

            elif input[0:6] == 'catch ':
                user_inputs = re.split(r'[\s-.]+', input[6:])
                level = user_inputs[-1]
                user_inputs.pop(-1)
                mon = ' '.join(word for word in user_inputs)

                embed = await calculateCatchRate(mon, level)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(embed=embed)

            elif input[0:6] == 'moves ':
                user_inputs = re.split(r'[\s-.]+', input[6:])
                level = user_inputs[-1]
                user_inputs.pop(-1)
                mon = ' '.join(word for word in user_inputs)

                embed = await showMoveSet(mon, level)

                if(type(embed) == type('')):
                    await message.channel.send(embed)
                else:
                    await message.channel.send(embed=embed)

            elif input[0:13] == 'add-nickname ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[13:])
                    if len(user_inputs) == 2:
                        response = await addNickname(user_inputs[0], user_inputs[1])

                        await message.channel.send(response)
                    else:
                        await message.channel.send('Invalid input! Check `$sl help`')
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')

            elif input[0:9] == 'nicknames':
                embed = await seeNicknames()

                await message.channel.send(embed=embed)

            elif input[0:5] == 'reset':
                response = resetFocus()

                await message.channel.send(response)

            elif input[0:12] == 'rare-candies':
                embeds = await makeRareCandiesEmbed()
                
                await Paginator.Simple().start(message.channel, pages=embeds)

            else:
                await message.channel.send('Command not recognized. Try using ```$sl help```')
        #endregion

        #region routes
        elif message.content[0:8] == '$routes ':
            await message.add_reaction('<:Zygarde_Cell:1231761804032610384>')
            input = message.content[8:]

            if await checkStrongestSoldier(int(message.author.mention[2:-1]), message.guild):
                if input == 'help':
                    embed, file = await routesHelp()
                    await message.channel.send(file=file, embed=embed)

                elif input[0:4] == 'add ':
                    if ',' in input:
                        user_inputs = re.split(r'[,]+', input[4:])
                        if len(user_inputs) == 3:
                            embed = await addRoute(user_inputs[0].strip(), int(user_inputs[1]), int(user_inputs[2]), message.author.mention)
                            await message.channel.send(embed)
                        else:
                            await message.channel.send('Invalid input! Check `$routes help`')
                    else:
                        await message.channel.send('Invalid input! Use commas \',\' in between values!')

                elif input[0:5] == 'walk ':
                    if ',' in input:
                        user_inputs = re.split(r'[,]+', input[5:])
                        if len(user_inputs) == 4:
                            embed = await walkRoute(user_inputs[0].strip(), int(user_inputs[1]), user_inputs[2].strip(), int(user_inputs[3]), message.author.mention)
                            await message.channel.send(embed)
                        else:
                            await message.channel.send('Invalid input! Check `$routes help`')
                    else:
                        await message.channel.send('Invalid input! Use commas \',\' in between values!')

                elif input[0:4] == 'list':
                    embed, file = await listRoutes(message.author.mention)

                    if(type(embed) == type('')):
                        await message.channel.send(embed)
                    else:
                        await message.channel.send(file=file, embed=embed)

                elif input[0:5] == 'today':
                    embed, file = await printoutDay(message.author.mention)

                    if(type(embed) == type('')):
                        await message.channel.send(embed)
                    else:
                        await message.channel.send(file=file, embed=embed)

                elif input[0:5] == 'stats':
                    embeds = await printoutRoutes(message.author.mention)

                    if(type(embeds) == type('')):
                        await message.channel.send(embeds)
                    else:
                        await Paginator.Simple().start(message.channel, pages=embeds)

                else:
                    await message.channel.send('Command not recognized. Try using ```$routes help```')
            else:
                await message.channel.send('Only routes strongest soldiers may use these commands. Begone non-believer!')
        #endregion
        
        #region pvp
        elif message.content == '$pvp':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')

            file = discord.File('images/pvp.png', filename='pvp.png')

            await message.channel.send(file=file)
        #endregion

        #region coins
        elif message.content == '$coins':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinyGimmighoul:1386804181670564032>')
            else: 
                await message.add_reaction('<:Gimmighoul:1386804101865668658>')

            with open('tokens/coins.txt') as file:
                link = file.read()

            await message.channel.send(link)
        #endregion

        #region mimikyu format
        elif message.content[0:8] == "$format ":
            input = message.content[8:]
            try:
                if input == 'help':
                    raise Exception()
                
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
                await message.channel.send("Mimikyu Lives On! But... you've still learned nothing and went and fucked something up.\n Only send messages like this ```$format Gym 1, Misty, 20, Route 3, Route 4``` In this order, Name of the previous battle ex. Gym 1, name of the next battle ex. Gym 2 or Misty, level cap for the next battle, encounters before the next battle.")
        #endregion

        #region mudae
        elif 'is about to be grinded into kakera by **anderson499**' in message.content:
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')
            input = message.content[4:]

            await message.channel.send(f'Your divorce papers are ready. So sad to see a blossoming relationship end so soon...\n' +
                                 f'But make sure to get that Mr. Krabs gif ready!\n```$divorce {message.content.split("**")[1]}```')
        #endregion

        #region pogo dps
        elif message.content[0:5] == '$dps ':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')

            input = message.content[5:]

            if input == 'help':
                embed, file = await dpsHelp()
                await message.channel.send(file=file, embed=embed)
            
            elif input == 'modifiers':
                embeds = await raidModifiers()
                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:8] == 'add-mon ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[8:])
                    if len(user_inputs) == 4:
                        embed = await dpsAddMon(user_inputs[0].strip(), int(user_inputs[1]), int(user_inputs[2]), int(user_inputs[3]))
                        await message.channel.send(embed)
                    else:
                        await message.channel.send('Invalid input! Check `$dps help`')
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')
            
            elif input[0:9] == 'add-move ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[9:])
                    if len(user_inputs) == 5:
                        embed = await dpsAddFastMove(user_inputs[0].strip(), int(user_inputs[1]), int(user_inputs[2]), int(user_inputs[3]), user_inputs[4].strip())
                        await message.channel.send(embed)
                    elif len(user_inputs) == 6:
                        embed = await dpsAddChargedMove(user_inputs[0].strip(), int(user_inputs[1]), int(user_inputs[2]), int(user_inputs[3]), int(user_inputs[4]), user_inputs[5].strip())
                        await message.channel.send(embed)
                    else:
                        await message.channel.send('Invalid input! Check `$dps help`')
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')
            
            elif input[0:12] == 'add-moveset ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[12:])
                    if len(user_inputs) >= 2:
                        embed = await dpsAddMoveset(user_inputs[0].strip(), user_inputs[1:])
                        await message.channel.send(embed)
                    else:
                        await message.channel.send('Invalid input! Check `$dps help`')
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')

            elif input[0:15] == 'remove-moveset ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[15:])
                    if len(user_inputs) >= 2:
                        embed = await dpsRemoveMoveset(user_inputs[0].strip(), user_inputs[1:])
                        await message.channel.send(embed)
                    else:
                        await message.channel.send('Invalid input! Check `$dps help`')
                else:
                    await message.channel.send('Invalid input! Use commas \',\' in between values!')

            elif input[0:10] == 'list-moves':
                embeds = await listDPSMoves()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:17] == 'list-move-changes':
                embeds = await listDPSMoveChanges()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:9] == 'list-mons':
                embeds = await listDPSMons()

                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)
            
            elif input[0:12] == 'delete-move ':
                embed = await deleteDPSMove(input[12:])

                await message.channel.send(embed)

            elif input[0:11] == 'delete-mon ':
                embed = await deleteDPSMon(input[11:])

                await message.channel.send(embed)

            elif input[0:6] == 'check ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[6:])
                    if len(user_inputs) >= 2:
                        embed, file = await dpsCheck(user_inputs[0].strip(), 'raids', user_inputs[1:])
                        if(type(embed) == type('')):
                            await message.channel.send(embed)
                        elif file is None:
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(embed=embed, file=file)
                    else:
                        await message.channel.send('I don\'t know wtf you\'re trying to input!')
                else:
                    embed, file = await dpsCheck(input[6:].strip(), 'raids')
                    if(type(embed) == type('')):
                        await message.channel.send(embed)
                    elif file is None:
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(embed=embed, file=file)

            elif input[0:9] == 'add-note ':
                embed = await addDPSNote(input[9:])

                await message.channel.send(embed)
            
            elif input[0:12] == 'delete-notes':
                embed = await clearDPSNotes()

                await message.channel.send(embed)

            elif input[0:12] == 'check-notes ':
                embed = await readDPSNotes(message.author, input[12:])

                await message.channel.send(embed)

            elif input[0:7] == 'symbol ':
                embed = await getDPSSymbol(input[7:])

                await message.channel.send(embed)

            else:
                await message.channel.send('I don\'t know wtf you\'re trying to input!')
        #endregion

        #region pogo dynamax
        elif message.content[0:5] == '$max ':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')

            input = message.content[5:]

            if input == 'help':
                embed, file = await dynamaxHelp()
                await message.channel.send(file=file, embed=embed)
            
            elif input == 'modifiers':
                embeds = await dynamaxModifiers()
                if(type(embeds) == type('')):
                    await message.channel.send(embeds)
                else:
                    await Paginator.Simple().start(message.channel, pages=embeds)

            elif input[0:6] == 'check ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[6:])
                    if len(user_inputs) >= 2:
                        embed, file = await dpsCheck(user_inputs[0].strip(), 'dmax', user_inputs[1:])
                        if(type(embed) == type('')):
                            await message.channel.send(embed)
                        elif file is None:
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(embed=embed, file=file)
                    else:
                        await message.channel.send('I don\'t know wtf you\'re trying to input!')
                else:
                    embed, file = await dpsCheck(input[6:].strip(), 'dmax')
                    if(type(embed) == type('')):
                        await message.channel.send(embed)
                    elif file is None:
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(embed=embed, file=file)
            else:
                await message.channel.send('I don\'t know wtf you\'re trying to input!')
        #endregion
        
        #region minecraft server
        elif message.content[0:4] == '$mc ':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:AmberShinyShuckle:1323169482964996160>')
            else: 
                await message.add_reaction('<:AmberShuckle:1323169451033759745>')

            input = message.content[4:]

            if input == 'help':
                embed, file = await mcHelp()
                await message.channel.send(file=file, embed=embed)

            elif input == 'setup':
                embeds = await mcSetup()

                await Paginator.Simple().start(message.channel, pages=embeds)

            elif input == 'save':
                if await serverOnline():
                    await mcSave(message.author.name)

                    await message.channel.send('Sent a server save request!')
                else:
                    await message.channel.send('The server\'s offline!')

            elif input == 'info':
                if await serverOnline():
                    embed, file = await mcInfo()
                    if(type(embed) == type('')):
                        await message.channel.send(embed)
                    else:
                        await message.channel.send(file=file, embed=embed)
                else:
                    await message.channel.send('The server\'s offline!')

            elif input == 'locate help':
                embed, file = await mcLocateHelp()
                await message.channel.send(file=file, embed=embed)

            elif input[0:7] == 'locate ':
                if await serverOnline():
                    if ',' in input:
                        user_inputs = re.split(r'[,]+', input[7:].strip())
                        if len(user_inputs) >= 2:
                            response = await mcLocate(message.author.name, user_inputs)
                            if(type(response) == type('')):
                                await message.channel.send(response)
                            else:
                                await Paginator.Simple().start(message.channel, pages=response)
                        else:
                            await message.channel.send('I don\'t know wtf you\'re trying to input!')
                    else:
                        response = await mcLocate(message.author.name, [input[7:].strip()])
                        if(type(response) == type('')):
                            await message.channel.send(response)
                        else:
                            await Paginator.Simple().start(message.channel, pages=response)
                else:
                    await message.channel.send('The server\'s offline!')

            elif input[0:5] == 'loot ':
                if ',' in input:
                    user_inputs = re.split(r'[,]+', input[5:].strip())
                    if len(user_inputs) == 2:
                        response = await mcLoot(user_inputs[0].lower().strip(), user_inputs[1].lower().strip())
                        await message.channel.send(response)
                    else:
                        await message.channel.send('I don\'t know wtf you\'re trying to input!')

            elif input[0:4] == 'say ':
                if await serverOnline():
                    await mcSay(input[4:], message.author.name.capitalize())
                
                    await message.channel.send('Sent the server a message!')
                else:
                    await message.channel.send('The server\'s offline!')
            
            elif input == 'start':
                if not await serverOnline():
                    await message.channel.send('Attempting to start server...')

                    response = await mcStart()

                    await message.channel.send(response)
                else:
                    await message.channel.send('The server is already online!')

            elif input == 'stop':
                if message.author.mention[2:-1] == '341722760852013066':
                    if await serverOnline():
                        await message.channel.send('Stopping the server in a minute!')

                        await mcBeginStop()
                    else:
                        await message.channel.send('The server\'s already offline!')
                else:
                    await message.channel.send('Get outta here, Anderson only!')

            elif input == 'restart':
                if message.author.mention[2:-1] == '341722760852013066':
                    if await serverOnline():
                        await message.channel.send('Beginning restart process! Try connecting in like 2 minutes!')

                        await mcRestart()
                    else:
                        await message.channel.send('The server\'s offline! Just use `$mc start` instead!')
                else:
                    await message.channel.send('Get outta here, Anderson only!')
            
            else:
                await message.channel.send('I don\'t know wtf you\'re trying to input!')
        #endregion

        #region Order 66
        elif message.content[0:25] == 'Shuckle, Execute Order 66':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')

            await message.channel.send('It shall be done')

            guild = message.guild

            try:
                for i in range(66):
                    role = await guild.create_role(name=f'Fraud Role #{i}')

                    await role.edit(color=9314812)

                    user = guild.get_member(341696864833241090)

                    await user.add_roles(role)
            except Exception as ex:
                print(ex)

        elif message.content[0:23] == 'Shuckle, Heal The World':
            rand_num = random.randint(1, 100)
            if rand_num == 69:
                await message.add_reaction('<:ShinySwoleShuckle:1188674339260878941>')
            else: 
                await message.add_reaction('<:SwoleShuckle:1187641763960205392>')

            if message.author.mention[2:-1] == '341722760852013066':
                await message.channel.send('And it shall be done, as it was in the beginning, as it has always been\nPeace shall descend graciously upon the land, and all will be mended')

                guild = message.guild
                
                all_roles = await guild.fetch_roles()

                try:
                    for role in all_roles:
                        if "Fraud Role" in role.name:
                            await role.delete()
                except Exception as ex:
                    print(ex)
            else:
                await message.channel.send('One cannot hope to heal the world without a strong conviction...')
        #endregion
        #endregion

## Set up and log in
client = DiscordClient()
with open('tokens/bot_token.txt') as file:
    token = file.read()
client.run(token)