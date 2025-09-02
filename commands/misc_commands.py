import discord
import random
from dictionaries.shared_dictionaries import sharedImagePaths

async def miscShuckleCommands(userInput, author=None, guild=None):

    if userInput == 'help':
        response = discord.Embed(title=f'Shuckle Bot Commands',
                                description='```$sl help``` Shows all the soul link commands\n' +
                                            '```$routes help``` Shows all the routes commands\n' +
                                            '```$dps help``` Shows all the PoGo dps commands\n' +
                                            '```$max help``` Shows all the PoGo dynamax commands\n' +
                                            '```$pvp help``` Shows all the PoGo Pvp commands\n' +
                                            '```$pogo help``` Shows all the PoGo event commands\n' +
                                            '```$mc help``` Shows all minecraft server commands\n' +
                                            '```$format help``` Shows how to call the mimikyu format command\n' +
                                            '```$coins``` Gets the coins link',
                                color=3553598)

        rand_num = random.randint(1, 100)
        if rand_num == 69:
            response.set_thumbnail(url=sharedImagePaths.get('ShinyShuckle'))
        else: 
            response.set_thumbnail(url=sharedImagePaths.get('Shuckle'))
    
    elif userInput == 'coins':
        with open('tokens/coins.txt') as file:
            response = file.read()
    
    elif userInput.startswith('format '):
        userInput = userInput[7:]
        try:
            if userInput == 'help':
                raise Exception()
            
            if ',' in userInput:
                splitInput = userInput.split(',')
                battle_name = splitInput[0].strip()
                level_cap = int(splitInput[1])
                encounters = []
                for text in splitInput[2:]:
                    encounters.append(text.strip())

                encounters_text = '['
                if encounters == []:
                    encounters_text += ']'
                for encounter in encounters:
                    if encounter == encounters[-1]:
                        encounters_text += f'\'{encounter}\']'
                    else:
                        encounters_text += f'\'{encounter}\', '
                    
                response = '{' + f'\'Stage\': 0, \'Battle-Name\': \'{battle_name}\', \'Level-Cap\': {level_cap}, \'Encounters\': {encounters_text}' + '}'
            else:
                raise Exception()
        except:
            response = 'Mimikyu Lives On! But... you\'ve still learned nothing and went and fucked something up.\n Only send messages like this ```$format Misty, 20, Route 3, Route 4``` In this order, name of the next battle ex. Gym 2 or Misty, level cap for the next battle, encounters before the next battle.'

    elif userInput == 'Execute Order 66':
        try:
            for i in range(66):
                role = await guild.create_role(name=f'Fraud Role #{i}')

                await role.edit(color=9314812)

                user = guild.get_member(341696864833241090)

                await user.add_roles(role)
        except Exception as ex:
            print(ex)
        
        response = 'It has been done'

    elif userInput == 'Heal The World':
        if author.mention[2:-1] == '341722760852013066':
            response = 'And it shall be done, as it was in the beginning, as it has always been\nPeace shall descend graciously upon the land, and all will be mended'
            
            all_roles = await guild.fetch_roles()

            try:
                for role in all_roles:
                    if 'Fraud Role' in role.name:
                        await role.delete()
            except Exception as ex:
                print(ex)
        else:
            response = 'One cannot hope to heal the world without a strong conviction...'

    elif userInput.startswith('mudae '):
        response = f'Your divorce papers are ready. So sad to see a blossoming relationship end so soon...\nBut make sure to get that Mr. Krabs gif ready!\n```$divorce {userInput[6:].split("**")[1]}```'
    
    else:
        response = 'I don\'t know what you\'re trying to input!'

    return response