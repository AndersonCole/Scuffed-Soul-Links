from functions.pogo_functions import *

async def pogoMiscCommands(userInput):
    if userInput == 'help':
        response = await pogoHelp()

    elif userInput == 'odds modifiers':
        response = oddsModifiers()

    elif userInput.startswith('odds'):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[5:])
            if len(splitInput) >= 2:
                response = await calculateOdds(splitInput[0].strip(), splitInput[1:])
            else:
                response = 'I don\'t know wtf you\'re trying to input!'
        else:
            response = await calculateOdds(userInput[5:].strip())

    else:
        response = await createEventsEmbeds(userInput)
        
    return response