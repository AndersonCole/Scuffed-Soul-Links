from functions.dps_functions import *

async def dpsCommands(userInput, author):
    file = None

    if userInput == 'help':
        response = await dpsHelp()
    
    elif userInput == 'modifiers':
        response = await raidModifiers()

    elif userInput.startswith('add-mon '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[8:])
            if len(splitInput) == 4:
                response = await dpsAddMon(splitInput[0].strip(), int(splitInput[1]), int(splitInput[2]), int(splitInput[3]))
            else:
                response = 'Invalid input! Check `$dps help`'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'
    
    elif userInput.startswith('add-move '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[9:])
            if len(splitInput) == 5:
                response = await dpsAddFastMove(splitInput[0].strip(), int(splitInput[1]), int(splitInput[2]), int(splitInput[3]), splitInput[4].strip())
            elif len(splitInput) == 6:
                response = await dpsAddChargedMove(splitInput[0].strip(), int(splitInput[1]), int(splitInput[2]), int(splitInput[3]), int(splitInput[4]), splitInput[5].strip())
            else:
                response = 'Invalid input! Check `$dps help`'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'
    
    elif userInput.startswith('add-moveset '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[12:])
            if len(splitInput) >= 2:
                response = await dpsAddMoveset(splitInput[0].strip(), splitInput[1:])
            else:
                response = 'Invalid input! Check `$dps help`'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput.startswith('remove-moveset '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[15:])
            if len(splitInput) >= 2:
                response = await dpsRemoveMoveset(splitInput[0].strip(), splitInput[1:])
            else:
                response = 'Invalid input! Check `$dps help`'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput == 'list-moves':
        response = await listDPSMoves()

    elif userInput == 'list-move-changes':
        response = await listDPSMoveChanges()

    elif userInput == 'list-mons':
        response = await listDPSMons()
    
    elif userInput.startswith('delete-move '):
        response = await deleteDPSMove(userInput[12:])

    elif userInput.startswith('delete-mon '):
        response = await deleteDPSMon(userInput[11:])

    elif userInput.startswith('check '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[6:])
            if len(splitInput) >= 2:
                response, file = await dpsCheck(splitInput[0].strip(), 'raids', splitInput[1:])
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response, file = await dpsCheck(userInput[6:].strip(), 'raids')

    elif userInput.startswith('add-note '):
        response = await addDPSNote(userInput[9:])
    
    elif userInput == 'delete-notes':
        response = await clearDPSNotes()

    elif userInput.startswith('check-notes '):
        response = await readDPSNotes(author, userInput[12:])

    elif userInput.startswith('symbol '):
        response = await getDPSSymbol(userInput[7:])

    else:
        response = 'I don\'t know wtf you\'re trying to input!'

    return response, file

async def maxCommands(userInput):
    file = None

    if userInput == 'help':
        response = await dynamaxHelp()
    
    elif userInput == 'modifiers':
        response = await dynamaxModifiers()

    elif userInput.startswith('check '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[6:])
            if len(splitInput) >= 2:
                response, file = await dpsCheck(splitInput[0].strip(), 'dmax', splitInput[1:])
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response, file = await dpsCheck(userInput[6:].strip(), 'dmax')
    else:
        response = 'I don\'t know wtf you\'re trying to input!'

    return response, file