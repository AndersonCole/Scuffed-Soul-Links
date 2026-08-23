from functions.pogo_functions import *
from functions.shared_functions import pogoAddMon, pogoDeleteMon, pogoListMons, formatTextForBackend

async def pogoMiscCommands(userInput, author, guild):
    if userInput == 'help':
        response = await pogoHelp()

    #region events
    elif userInput == 'events help':
        response = await pogoEventsHelp()

    elif userInput.startswith('events '):
        response = await createEventsEmbeds(userInput[7:])
    #endregion

    #region odds
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
    #endregion

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

    elif userInput.startswith('make-csv '):
        response = await getCSVFromInput(formatTextForBackend(userInput[8:]))

    #region tracking commands
    elif userInput.startswith('user-nickname '):
        splitInput = re.split(r'[,]+', userInput[14:])
        if len(splitInput) == 2:
            response = await addUserNickname(splitInput[0].strip(), splitInput[1].strip())
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput.startswith('track '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[6:])
            if len(splitInput) >= 2:
                response = await trackMon(splitInput[0], splitInput[1:], author.mention)
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput.startswith('untrack '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[8:])
            if len(splitInput) >= 2:
                response = await removeTrackedMon(splitInput[0], splitInput[1:], author.mention)
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput.startswith('tracked '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[8:])
            if len(splitInput) == 2:
                response = await checkTrackedMon(splitInput[0], splitInput[1].strip(), guild)
            else:
                response = 'Theres a new more verbose command for showing multiple tracked mons!\nTry using `$pogo tracked-list`'
        else:
            response = await checkTrackedMon(userInput[8:], author.mention, guild)

    elif userInput.startswith('tracked-list '):
        if '{' in userInput and '}' in userInput:
            monGroup = re.search(r'\{([^}]*)\}', userInput[13:])
            userInput = userInput.replace(monGroup.group(1), '')

            splitInput = re.split(r'[,]+', userInput[13:])
            splitMonInput = re.split(r'[,]+', monGroup.group(1))
            if len(splitInput) == 2:
                response = await checkTrackedListMons(splitMonInput, splitInput[1], author.mention, guild)
            elif len(splitInput) == 3:
                response = await checkTrackedListMons(splitMonInput, splitInput[1], splitInput[2].strip(), guild)
            else:
                response = 'I don\'t know wtf you\'re trying to input!'

        elif ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[13:])
            if len(splitInput) == 2:
                response = await checkTrackedListMons(splitInput[0], splitInput[1], author.mention, guild)
            elif len(splitInput) == 3:
                response = await checkTrackedListMons(splitInput[0], splitInput[1], splitInput[2].strip(), guild)
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = 'Invalid input! Use commas \',\' in between values!'
    #endregion

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