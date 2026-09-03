import regex as re
from functions.routes_functions import *
from functions.shared_functions import formatCommand, formatSplitInput

async def routesCommands(userInput, author, guild):
    if await checkStrongestSoldier(author.id, guild):
        if userInput == 'help':
            response = await routesHelp()

        elif userInput.startswith('add'):
            userInput = formatCommand('add', userInput)
                                        
            splitInput = formatSplitInput(userInput)
        
            if splitInput is None:
                response = 'Invalid input! Use commas \',\' in between values!'

            if len(splitInput) == 3:
                response = await addRoute(splitInput[0], int(splitInput[1]), int(splitInput[2]), author.id)
            else:
                response = 'Invalid input! Get some `$routes help`'

        elif userInput.startswith('walk'):
            userInput = formatCommand('walk', userInput)
                                                    
            splitInput = formatSplitInput(userInput)
        
            if splitInput is None:
                response = 'Invalid input! Use commas \',\' in between values!'

            if len(splitInput) == 4:
                response = await walkRoute(splitInput[0], int(splitInput[1]), splitInput[2], int(splitInput[3]), author.id)
            else:
                response = 'Invalid input! Get some `$routes help`'

        elif userInput == 'list':
            response = await listRoutes(author.id)

        elif userInput == 'today':
            response = await printoutDay(author.id)

        elif userInput == 'stats':
            response = await printoutRoutes(author.id)

        else:
            response = 'I\'ve never seen that routes command before! You typed it horribly wrong! Get some `$routes help`!'
    else:
        response = 'Only routes strongest soldiers may use these commands. Begone non-believer!'

    return response