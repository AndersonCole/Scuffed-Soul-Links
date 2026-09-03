import regex as re
from functions.soul_link_functions import *
from functions.shared_functions import formatCommand, formatSplitInput, getUserIdFromNickname

async def soulLinkCommands(userInput, author, guild):
    if userInput == 'help':
        response = await soulLinksHelp()

    elif userInput.startswith('new-sl'):
        userInput = formatCommand('new-sl', userInput)
        
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'

        if len(splitInput) >= 4:
            response = await createNewRun(splitInput[0], splitInput[1], splitInput[2:], guild)
        else:
            response = 'Specify more than one player!\nIf you\'re trying to just do a nuzlocke, set Shuckle as player 2!'

    elif userInput.startswith('encounter'):
        userInput = formatCommand('encounter', userInput)
        
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'

        if len(splitInput > 2):
            response = await encounterMonGroup(splitInput[0], splitInput[1:])
        elif len(splitInput == 2):
            if getUserIdFromNickname(splitInput[1]) is not None:
                response = await encounterMonGroup(splitInput[0], splitInput[1:])
            else:
                response = await encounterMon(splitInput[0], splitInput[1], author.id)
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput == 'encounters':
        response = await listEncounters()

    elif userInput == 'links':
        response = await listLinks()
    
    elif userInput.startswith('link-data'):
        userInput = formatCommand('link-data', userInput)
                
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = await getLinkData(userInput, author.id)

        else:
            response = await getLinkData(splitInput[0], splitInput[1])

    elif userInput.startswith('evolve'):
        response = await evolveMon(formatCommand('evolve', userInput), author.id)

    elif userInput.startswith('undo-evolve'):
        response = await undoEvolveMon(formatCommand('undo-evolve', userInput), author.id)

    elif userInput.startswith('death'):
        userInput = formatCommand('death', userInput)
                        
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'
        else:
            response = await newDeath(splitInput[0], ','.join(word for word in splitInput[1:]))
    
    elif userInput.startswith('undo-death'):
        response = await undoDeath(formatCommand('undo-death', userInput))
    
    elif userInput == 'deaths':
        response = await listDeaths()

    elif userInput.startswith('select-run'):
        response = selectRun(formatCommand('select-run', userInput))

    elif userInput == 'runs':
        response = await listRuns()

    elif userInput.startswith('choose-team'):
        userInput = formatCommand('choose-team', userInput)
                                
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'
        else:
            response = await chooseTeam(splitInput, author.id)

    elif userInput == 'next-battle':
        response = await nextBattle()
    
    elif userInput == 'progress':
        response = await progressRun()

    elif userInput.startswith('add-note'):
        response = await addNote(formatCommand('add-note', userInput))

    elif userInput.startswith('ask-shuckle'):
        response = await askShuckle(formatCommand('ask-shuckle', userInput))

    elif userInput == 'random':
        response = await pingUser()

    elif userInput == 'win-run':
        response = await setRunStatus('Victory', guild)

    elif userInput == 'fail-run':
        response = await setRunStatus('Defeat', guild)

    elif userInput == 'undo-status':
        response = await setRunStatus('In Progress', guild)

    elif userInput == 'run-info':
        response = await seeStats()

    elif userInput.startswith('dex'):
        userInput = formatCommand('dex', userInput)
                                        
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = await makePokedexEmbed(userInput, None)
        else:
            response = await makePokedexEmbed(splitInput[0], splitInput[1])

    elif userInput.startswith('moves'):
        userInput = formatCommand('moves', userInput)
                                                
        splitInput = formatSplitInput(userInput)
    
        if splitInput is None:
            response = 'Invalid input! Use commas \',\' in between values!'
        else:
            response = await showMoveSet(splitInput[0], splitInput[1])

    elif userInput == 'reset':
        response = resetFocus()

    elif userInput == 'rare-candies':
        response = await makeRareCandiesEmbed()

    else:
        response = 'I\'ve never seen that soul links command before! You typed it horribly wrong! Get some `$routes help`!'

    return response