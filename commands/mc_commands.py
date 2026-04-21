import regex as re
from dictionaries.shared_dictionaries import sharedFileLocations
from functions.shared_functions import loadDataVariableFromFile
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

    elif userInput == 'locate help':
        response = await mcLocateHelp()

    elif userInput.startswith('locate '):
        if await serverOnline():
            if ',' in userInput:
                splitInput = re.split(r'[,]+', userInput[7:].strip())
                if len(splitInput) >= 2:
                    response = await mcLocate(author.name, splitInput)
                else:
                    response = 'I don\'t know wtf you\'re trying to input!'
            else:
                response = await mcLocate(author.name, [userInput[7:].strip()])
        else:
            response = 'The server\'s offline!'

    elif userInput.startswith('loot '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[5:].strip())
            if len(splitInput) == 2:
                response = await mcLoot(splitInput[0].lower().strip(), splitInput[1].lower().strip())
            else:
               response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = 'I don\'t know wtf you\'re trying to input!'

    elif userInput[0:4] == 'say ':
        if await serverOnline():
            await mcSay(userInput[4:], author.name.capitalize())
        
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
        response = 'I don\'t know wtf you\'re trying to input!'
    
    return response