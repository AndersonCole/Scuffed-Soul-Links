from functions.pvp_functions import *

async def pvpCommands(userInput):
    if userInput == 'help':
        response = await pvpHelp()
    
    elif userInput == 'img':
        response = await getPvpRanksImg()

    else:
        response = 'Its on my list to do more here, check back soonish'
    
    return response