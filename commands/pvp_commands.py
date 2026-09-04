from functions.pvp_functions import *
from functions.shared_functions import formatCommand, formatSplitInput, handleAddPoGoMon, pogoDeleteMon, pogoListMons

async def pvpCommands(userInput, author):
    if userInput == 'help':
        response = await pvpHelp()
    
    elif userInput == 'modifiers':
        response = pvpModifiers()

    elif userInput.startswith('check'):
        userInput = formatCommand('check', userInput)
            
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = await pvpRankCheck(userInput)
    
        elif len(splitInput) >= 2:
            response = await pvpRankCheck(splitInput[0], splitInput[1:])
        else:
            response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'

    elif userInput.startswith('list-fakes'):
        response = await listFakeRankOnes(formatCommand('list-fakes', userInput))

    elif userInput.startswith('scanner-system'):
        userInput = formatCommand('scanner-system', userInput)
                    
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = await specifyScannerSystem(userInput, author.id)

        elif len(splitInput) >= 2:
            response = await specifyScannerSystem(splitInput[0], author.id, splitInput[1:])
        else:
            response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'

    elif userInput.startswith('tracking-string'):
        userInput = formatCommand('tracking-string', userInput)
                            
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = await getTrackingString(userInput, author.id)
        
        elif len(splitInput) >= 2:
            response = await getTrackingString(splitInput[0], author.id, splitInput[1:])
        else:
            response = 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'

    elif userInput == 'img':
        response = await getPvpRanksImg()

    #region mons add delete read
    elif userInput.startswith('add-mon'):
        response = await handleAddPoGoMon(userInput, '$pvp help')

    elif userInput.startswith('delete-mon'):
        response = await pogoDeleteMon(formatCommand('delete-mon', userInput))

    elif userInput.startswith('list-mons'):
        response = await pogoListMons()
    #endregion

    else:
        response = 'I\'ve never seen that pvp command before! You typed it horribly wrong! Get some `$pvp help`!'
    
    return response