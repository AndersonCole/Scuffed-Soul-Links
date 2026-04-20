from functions.pogo_functions import *
from functions.shared_functions import pogoAddMon, pogoDeleteMon, pogoListMons

async def pogoMiscCommands(userInput):
    if userInput == 'help':
        response = await pogoHelp()

    elif userInput == 'events help':
        response = await pogoEventsHelp()

    elif userInput.startswith('events '):
        response = await createEventsEmbeds(userInput[7:])

    elif userInput.startswith('stats '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[6:])
            if len(splitInput) == 7:
                response = await convertToGoStats(splitInput[:-1], nerfOverride=splitInput[-1].strip().lower())
            elif len(splitInput) == 6:
                response = await convertToGoStats(splitInput)
            elif len(splitInput) == 2:
                response = await convertToGoStatsFromName(splitInput[0], nerfOverride=splitInput[1].strip().lower())
            else:
                response = 'Invalid input! Make sure you add all 6 stats comma separated!'
        else:
            response = await convertToGoStatsFromName(userInput[6:])

    elif userInput == 'odds modifiers':
        response = oddsModifiers()

    elif userInput.startswith('odds '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[5:])
            if len(splitInput) >= 2:
                response = await calculateOdds(splitInput[0].strip(), splitInput[1:])
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = await calculateOdds(userInput[5:].strip())

    #region mons add delete read
    elif userInput.startswith('add-mon '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[8:])
            if len(splitInput) == 4:
                response = await pogoAddMon(splitInput[0].strip(), int(splitInput[1]), int(splitInput[2]), int(splitInput[3]))
            else:
                response = 'Invalid input! Check `$pogo help`'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'
    
    elif userInput.startswith('delete-mon '):
        response = await pogoDeleteMon(userInput[11:])

    elif userInput == 'list-mons':
        response = await pogoListMons()
    #endregion

    else:
        response = 'I don\'t know what you\'re trying to input!'
        
    return response