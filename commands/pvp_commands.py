from functions.pvp_functions import *
from functions.shared_functions import pogoAddMon, pogoDeleteMon, pogoListMons

async def pvpCommands(userInput):
    if userInput == 'help':
        response = await pvpHelp()
    
    elif userInput == 'modifiers':
        response = pvpModifiers()

    elif userInput.startswith('check '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[6:])
            if len(splitInput) >= 2:
                response = await pvpRankCheck(splitInput[0].strip(), splitInput[1:])
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = await pvpRankCheck(userInput[6:].strip())

    elif userInput.startswith('list-fakes'):
        if ' ' in userInput:
            response = await listFakeRankOnes(userInput[11:])
        else:
            response = await listFakeRankOnes()

    elif userInput == 'img':
        response = await getPvpRanksImg()

    #region mons add delete read
    elif userInput.startswith('add-mon '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[8:])
            if len(splitInput) == 4:
                response = await pogoAddMon(splitInput[0].strip(), int(splitInput[1]), int(splitInput[2]), int(splitInput[3]))
            else:
                response = 'Invalid input! Check `$pvp help`'
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