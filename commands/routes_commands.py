import regex as re
from functions.routes_functions import *

async def routesCommands(userInput, author, guild):
    if await checkStrongestSoldier(int(author.mention[2:-1]), guild):
        if userInput == 'help':
            response = await routesHelp()

        elif userInput.startswith('add '):
            if ',' in userInput:
                splitInput = re.split(r'[,]+', userInput[4:])
                if len(splitInput) == 3:
                    response = await addRoute(splitInput[0].strip(), int(splitInput[1]), int(splitInput[2]), author.mention)
                else:
                    response = 'Invalid input! Check `$routes help`'
            else:
                response = 'Invalid input! Use commas \',\' in between values!'

        elif userInput.startswith('walk '):
            if ',' in userInput:
                splitInput = re.split(r'[,]+', userInput[5:])
                if len(splitInput) == 4:
                    response = await walkRoute(splitInput[0].strip(), int(splitInput[1]), splitInput[2].strip(), int(splitInput[3]), author.mention)
                else:
                    response = 'Invalid input! Check `$routes help`'
            else:
                response = 'Invalid input! Use commas \',\' in between values!'

        elif userInput == 'list':
            response = await listRoutes(author.mention)

        elif userInput == 'today':
            response = await printoutDay(author.mention)

        elif userInput == 'stats':
            response = await printoutRoutes(author.mention)

        else:
            response = 'Command not recognized. Try using ```$routes help```'
    else:
        response = 'Only routes strongest soldiers may use these commands. Begone non-believer!'

    return response