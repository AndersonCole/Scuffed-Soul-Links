from functions.dps_functions import *
from functions.shared_functions import formatCommand, formatSplitInput, handleAddPoGoMon, pogoDeleteMon, pogoListMons

#region dps
async def dpsCommands(userInput, author):
    file = None

    if userInput == ('help'):
        response = await dpsHelp()
    
    elif userInput == ('modifiers'):
        response = await raidModifiers()

    elif userInput.startswith('check'):
        response, file = await handleDpsCheck(userInput, 'raids', author.id)

    elif userInput.startswith('batch-check'):
        response = handleBatchDpsCheck(userInput, 'raids', author.id)

    elif userInput.startswith('super-max'):
        response = await addSuperMax(formatCommand('super-max', userInput))
    
    elif userInput.startswith('add-note'):
        response = await addDPSNote(formatCommand('add-note', userInput))
    
    elif userInput == ('delete-notes'):
        response = await clearDPSNotes()

    elif userInput.startswith('check-notes'):
        response = await readDPSNotes(author, formatCommand('check-notes', userInput))

    elif userInput.startswith('default-modifiers'):
        response = await getUserModifiers('raids', author.id)

    elif userInput.startswith('set-modifiers'):
        response = await handleSetModifiers(userInput, 'raids', author.id)

    elif userInput == ('reset-modifiers'):
        response = await resetUserModifiers('raids', author.id)

    #region mons and moves add del read
    elif userInput.startswith('add-mon'):
        response = await handleAddPoGoMon(userInput, '$max help')
    
    elif userInput.startswith('delete-mon'):
        response = await pogoDeleteMon(formatCommand('delete-mon', userInput))

    elif userInput.startswith('list-mons'):
        response = await pogoListMons()

    elif userInput.startswith('add-moveset'):
        response = await handleAddPoGoDpsMoveset(userInput)

    elif userInput.startswith('remove-moveset'):
        response = await handleRemovePoGoDpsMoveset(userInput)

    elif userInput.startswith('add-move'):
        response = await handleAddPoGoDpsMove(userInput, '$max help')
    
    elif userInput.startswith('delete-move'):
        response = await dpsDeleteMove(formatCommand('delete-move', userInput))

    elif userInput.startswith('list-moves'):
        response = await dpsListMoves()
    #endregion

    else:
        response = 'I\'ve never seen that dps command before! You typed it horribly wrong! Get some `$dps help`!'

    return response, file
#endregion

#region dmax
async def maxCommands(userInput, author):
    file = None

    if userInput == ('help'):
        response = await dynamaxHelp()
    
    elif userInput == ('modifiers'):
        response = await dynamaxModifiers()

    elif userInput.startswith('check'):
        response, file = await handleDpsCheck(userInput, 'dmax', author.id)

    elif userInput.startswith('batch-check'):
        response = handleBatchDpsCheck(userInput, 'dmax', author.id)

    elif userInput.startswith('default-modifiers'):
        response = await getUserModifiers('dmax', author.id)

    elif userInput.startswith('set-modifiers'):
        response = await handleSetModifiers(userInput, 'dmax', author.id)

    elif userInput.startswith('reset-modifiers'):
        response = await resetUserModifiers('dmax', author.id)

    #region mons, moves add del read
    elif userInput.startswith('add-mon'):
        response = await handleAddPoGoMon(userInput, '$max help')
    
    elif userInput.startswith('delete-mon'):
        response = await pogoDeleteMon(formatCommand('delete-mon', userInput))

    elif userInput.startswith('list-mons'):
        response = await pogoListMons()

    elif userInput.startswith('add-moveset'):
        response = await handleAddPoGoDpsMoveset(userInput)

    elif userInput.startswith('remove-moveset'):
        response = await handleRemovePoGoDpsMoveset(userInput)

    elif userInput.startswith('add-move'):
        response = await handleAddPoGoDpsMove(userInput, '$max help')
    
    elif userInput.startswith('delete-move'):
        response = await dpsDeleteMove(formatCommand('delete-move', userInput))

    elif userInput.startswith('list-moves'):
        response = await dpsListMoves()
    #endregion

    else:
        response = 'I\'ve never seen that max command before! You typed it horribly wrong! Get some `$max help`!'

    return response, file
#endregion

#region shared command parse logic
async def handleDpsCheck(userInput, battleSystem, authorId):
    userInput = formatCommand('check', userInput)
    
    splitInput = formatSplitInput(userInput)

    if splitInput is None:
        return await dpsCheck(userInput, battleSystem, authorId)

    if len(splitInput) >= 2:
        return await dpsCheck(splitInput[0], battleSystem, authorId, splitInput[1:])
    else:
        return 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?', None
    
async def handleBatchDpsCheck(userInput, battleSystem, authorId):
    userInput = formatCommand('batch-check', userInput)
            
    splitInput = formatSplitInput(userInput)

    if splitInput is None:
        if battleSystem == 'raids':
            return 'Just use `$dps check` if you\'re only gonna check one mon!'
        else:
            return 'Just use `$max check` if you\'re only gonna check one mon!'

    if len(splitInput) >= 2:
        return await batchDpsCheck(splitInput, battleSystem, authorId)
    else:
        return 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'

async def handleSetModifiers(userInput, battleSystem, authorId):
    userInput = formatCommand('set-modifiers', userInput)
                
    splitInput = formatSplitInput(userInput)
    
    if splitInput is None:
        return await setUserModifiers([userInput], battleSystem, authorId)

    return await setUserModifiers(splitInput, battleSystem, authorId)

#region moves add del read
async def handleAddPoGoDpsMove(userInput, helpCommand):
    userInput = formatCommand('add-move', userInput)
                    
    splitInput = formatSplitInput(userInput)
    
    if splitInput is None:
        return 'Invalid input! Use commas \',\' in between values!'

    if len(splitInput) == 5:
        return await dpsAddFastMove(splitInput, int(splitInput[1]), int(splitInput[2]), int(splitInput[3]), splitInput[4])
    elif len(splitInput) == 6:
        return await dpsAddChargedMove(splitInput, int(splitInput[1]), int(splitInput[2]), int(splitInput[3]), int(splitInput[4]), splitInput[5])
    else:
        return f'Invalid input! Get some `{helpCommand}`!'
    
async def handleAddPoGoDpsMoveset(userInput):
    userInput = formatCommand('add-moveset', userInput)
    
    splitInput = formatSplitInput(userInput)
            
    if splitInput is None:
        return 'Invalid input! Use commas \',\' in between values!'

    if len(splitInput) >= 2:
        return await dpsAddMoveset(splitInput[0], splitInput[1:])
    else:
        return 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'

async def handleRemovePoGoDpsMoveset(userInput):
    userInput = formatCommand('remove-moveset', userInput)
            
    splitInput = formatSplitInput(userInput)
            
    if splitInput is None:
        return 'Invalid input! Use commas \',\' in between values!'

    if len(splitInput) >= 2:
        return await dpsRemoveMoveset(splitInput[0], splitInput[1:])
    else:
        return 'This code path shouldn\'t be reachable! How on earth did you mess up your command that badly?'
#endregion
#endregion