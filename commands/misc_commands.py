import regex as re
from dictionaries.shared_dictionaries import sharedFileLocations
from functions.shared_functions import loadDataVariableFromFile
from functions.misc_functions import *

admins = loadDataVariableFromFile(sharedFileLocations.get('Admins'), readJson=True)

async def miscShuckleCommands(userInput, author=None, guild=None):

    if userInput == 'help':
        response = shuckleHelp()
    
    elif userInput.startswith('add-nickname '):
        splitInput = re.split(r'[,]+', userInput[13:])
        if len(splitInput) == 2:
            response = await addNickname(splitInput[0], splitInput[1])
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput.startswith('remove-nickname '):
        response = await removeNickname(userInput[16:])

    elif userInput == 'nicknames':
        response = listNicknames()

    elif userInput == 'coins':
        with open('tokens/coins.txt') as file:
            response = file.read()
    
    elif userInput.startswith('format '):
        response = mimikyuFormat(userInput[7:])

    elif userInput == 'Execute Order 66':
        response = order66(guild)

    elif userInput == 'Heal The World':
        if author.id in admins:
            response = healTheWorld(guild)
        else:
            response = 'One cannot hope to heal the world without a strong conviction...'

    elif userInput.startswith('mudae '):
        response = (f'Your divorce papers are ready. So sad to see a blossoming relationship end so soon...\n' +
                    f'But make sure to get that Mr. Krabs gif ready!\n```$divorce {userInput[6:].split("**")[1]}```')
    
    else:
        response = 'I don\'t know what you\'re trying to input!'

    return response