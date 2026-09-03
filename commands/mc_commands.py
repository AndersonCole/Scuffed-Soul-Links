import regex as re
from dictionaries.shared_dictionaries import sharedFileLocations
from functions.shared_functions import formatCommand, formatSplitInput, loadDataVariableFromFile
from functions.mc_server_functions import *

owner = int(loadDataVariableFromFile(sharedFileLocations.get('Owner'), readJson=False))
admins = loadDataVariableFromFile(sharedFileLocations.get('Admins'), readJson=True)

async def minecraftCommands(userInput, author):
    if userInput == 'help':
        response = await mcHelp()

    elif userInput == 'setup':
        response = await mcSetup()

    elif userInput == 'save':
        if author.id in admins:
            if await serverOnline():
                await mcSave(author.name)

                response = 'Sent a server save request!'
            else:
                response = 'The server\'s offline!'
        else:
            response = 'Get outta here, admins only!'

    elif userInput == 'info':
        if await serverOnline():
            response = await mcInfo()
        else:
            response = 'The server\'s offline!'

    elif userInput.startswith('locate'):
        userInput = formatCommand('locate', userInput)

        if userInput == 'help':
            response = await mcLocateHelp()

        elif await serverOnline():
            splitInput = formatSplitInput(userInput)
        
            if splitInput is None:
                response = await mcLocate(author.name, userInput)
        
            if len(splitInput) >= 2:
                response = await mcLocate(author.name, splitInput)
            else:
                response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'
        else:
            response = 'The server\'s offline!'

    elif userInput.startswith('loot'):
        userInput = formatCommand('loot', userInput)
                        
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = 'I don\'t understand your input as a valid XYZ co-ordinate!'

        if len(splitInput) == 2:
            response = await mcLoot(splitInput[0], splitInput[1])
        else:
            response = 'I don\'t understand your input as a valid XYZ co-ordinate!'

    elif userInput.startswith('say'):
        if await serverOnline():
            await mcSay(formatCommand('say', userInput), author.name.capitalize())
        
            response = 'Sent the server a message!'
        else:
            response = 'The server\'s offline!'
    
    elif userInput == 'lockdown':
        if author.id == owner:
            if await serverOnline():
                response = 'Beginning area lockdown!'

                await mcBeginLockdown()
            else:
                response = 'The server\'s offline!'
        else:
            response = 'Get outta here, admin only!'

    elif userInput == 'start':
        if author.id in admins:
            if not await serverOnline():
                response = await mcStart()
            else:
                response = 'The server is already online!'
        else:
            response = 'Get outta here, admins only!'

    elif userInput == 'stop':
        if author.id in admins:
            if await serverOnline():
                response = 'Stopping the server in a minute!'

                await mcBeginStop()
            else:
                response = 'The server\'s already offline!'
        else:
            response = 'Get outta here, admins only!'

    elif userInput == 'restart':
        if author.id in admins:
            if await serverOnline():
                response = 'Beginning restart process! Try connecting in like 2 minutes!'

                await mcRestart()
            else:
                response = 'The server\'s offline! Just use `$mc start` instead!'
        else:
            response = 'Get outta here, admins only!'
    
    elif userInput == 'backup':
        if author.id == owner:
            if await serverOnline():
                response = 'Backup starting in 5 minutes!'

                await mcBackup()
            else:
                response = 'The server\'s offline, so I\'m starting the backup process right now! The server should stay offline while the backup is happening!'

                await mcOfflineBackup()
        else:
            response = 'Get outta here, admins only!'

    else:
        response = 'I\'ve never seen that minecraft server command before! You typed it horribly wrong! Get some `$mc help`!'
    
    return response