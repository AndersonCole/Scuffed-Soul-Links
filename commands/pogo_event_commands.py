from functions.pogo_event_functions import *

async def pogoEventCommands(userInput):
    if userInput == 'help':
        response = await eventsHelp()

    else:
        response = await createEventsEmbeds(userInput)
        
    return response