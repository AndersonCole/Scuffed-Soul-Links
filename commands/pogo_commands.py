from functions.pogo_functions import *
from functions.shared_functions import formatCommand, formatSplitInput, handleAddPoGoMon, pogoDeleteMon, pogoListMons, formatTextForBackend

async def pogoMiscCommands(userInput, author, guild):
    if userInput == 'help':
        response = await pogoHelp()

    #region events
    elif userInput.startswith('events'):
        userInput = formatCommand('events', userInput)
        
        if userInput == 'help':
            response = await pogoEventsHelp()

        else:
            response = await createEventsEmbeds(userInput)
    #endregion

    #region odds
    elif userInput.startswith('odds'):
        userInput = formatCommand('odds', userInput)
                
        if userInput == 'modifiers':
            response = oddsModifiers()

        else:
            splitInput = formatSplitInput(userInput)
                    
            if splitInput is None:
                await calculateOdds(userInput)

            if len(splitInput) >= 2:
                response = await calculateOdds(splitInput[0], splitInput[1:])
            else:
                response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'
    #endregion

    #region stats
    elif userInput.startswith('stats'):
        userInput = formatCommand('stats', userInput)

        splitInput = formatSplitInput(userInput)

        if splitInput is None:
            response = await convertToGoStatsFromName(userInput)

        if len(splitInput) == 7:
            response = await convertToGoStats(splitInput[:-1], nerfOverride=splitInput[-1])
        elif len(splitInput) == 6:
            response = await convertToGoStats(splitInput)
        elif len(splitInput) == 2:
            response = await convertToGoStatsFromName(splitInput[0], nerfOverride=splitInput[1])
        else:
            response = 'Invalid input! Make sure you add all 6 stats comma separated!'
    #endregion

    #region tracking commands
    elif userInput.startswith('tracked'):
        userInput = formatCommand('tracked', userInput)

        if userInput == '':
            response = 'Invalid input! Specify something you want to see tracked info on!'

        else:
            csvMonGroup = None
            if '{' in userInput and '}' in userInput:
                csvMonGroup = re.search(r'\{([^}]*)\}', userInput)
                userInput = userInput.replace(f'{csvMonGroup.group(1)}', '')

            splitInput = formatSplitInput(userInput)

            userInput = [userInput] if splitInput is None else splitInput

            response = await determineTrackedResponse(userInput, author.id, guild, monGroup=formatSplitInput(csvMonGroup.group(1)))

    elif userInput.startswith('track'):
        userInput = formatCommand('track', userInput)
        
        splitInput = formatSplitInput(userInput)

        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'

        if len(splitInput) >= 2:
            response = await trackMon(splitInput[0], splitInput[1:], author.id)
        else:
            response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'

    elif userInput.startswith('untrack'):
        userInput = formatCommand('untrack', userInput)
                
        splitInput = formatSplitInput(userInput)

        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'

        if len(splitInput) >= 2:
            response = await removeTrackedMon(splitInput[0], splitInput[1:], author.id)
        else:
            response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'
    #endregion

    #region mons add delete read
    elif userInput.startswith('add-mon'):
        response = await handleAddPoGoMon(userInput, '$pogo help')

    elif userInput.startswith('delete-mon'):
        response = await pogoDeleteMon(formatCommand('delete-mon', userInput))

    elif userInput.startswith('list-mons'):
        response = await pogoListMons()
    #endregion

    else:
        response = 'I\'ve never seen that pogo command before! You typed it horribly wrong! Get some `$pogo help`!'
        
    return response