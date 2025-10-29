import regex as re
from functions.soul_link_functions import *

async def soulLinkCommands(userInput, author, guild):
    if userInput == 'help':
        response = await help()

    elif userInput.startswith('new-sl '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[7:])

            if not len(splitInput) > 3:
                response = 'Specify more than one player!\nIf you\'re trying to just do a nuzlocke, set Shuckle as player 2!'
            else:
                response = await createNewRun(splitInput[0].strip(), splitInput[1].strip(), [player.strip() for player in splitInput[2:]], guild)
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput.startswith('encounter '):
        splitInput = re.split(r'[,]+', userInput[10:])
        if len(splitInput) == 2:
            if re.search(r'<@\d+>', splitInput[1].strip()) is not None:
                response = await encounterMonGroup(splitInput[0].strip(), [splitInput[1]])
            else:
                response = await encounterMon(splitInput[0].strip(), splitInput[1].strip(), author.mention)
        elif len(splitInput) > 2:
            response = await encounterMonGroup(splitInput[0].strip(), splitInput[1:])
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput == 'encounters':
        response = await listEncounters()

    elif userInput == 'links':
        response = await listLinks()
    
    elif userInput.startswith('link-data '):
        if re.search(r'<@\d+>', userInput[10:].strip()) is not None:
            splitInput = re.split(r'[\s]+', userInput[10:])
            
            linkInfo = ' '.join(word for word in splitInput[1:])
            response = await getLinkData(linkInfo.strip(), splitInput[0])
        else:
            response = await getLinkData(userInput[10:].strip(), author.mention)

    elif userInput.startswith('evolve '):
        response = await evolveMon(userInput[7:].strip(), author.mention)

    elif userInput.startswith('undo-evolve '):
        response = await undoEvolveMon(userInput[12:].strip(), author.mention)

    elif userInput.startswith('death '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[6:])

            response = await newDeath(splitInput[0].strip(), ','.join(word for word in splitInput[1:]))
        else:
            response = 'Invalid input! Use commas \',\' in between values!'
    
    elif userInput.startswith('undo-death '):
        response = await undoDeath(userInput[11:].strip())
    
    elif userInput == 'deaths':
        response = await listDeaths()

    elif userInput.startswith('select-run '):
        response = selectRun(userInput[11:].strip())

    elif userInput == 'runs':
        response = await listRuns()

    elif userInput.startswith('choose-team '):
        if ',' in userInput[12:]:
            links = re.split(r'[,]+', userInput[12:])
            response = await chooseTeam(links, author.mention)
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput == 'next-battle':
        response = await nextBattle()
    
    elif userInput == 'progress':
        response = await progressRun()

    elif userInput.startswith('add-note '):
        response = await addNote(userInput[9:])

    elif userInput.startswith('ask-shuckle '):
        response = await askShuckle(userInput[12:])

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

    elif userInput.startswith('dex '):
        if ',' in userInput:
            splitInput = re.split(r'[,]+', userInput[4:])
            response = await makePokedexEmbed(splitInput[0].strip(), splitInput[1].strip())
        else:
            response = await makePokedexEmbed(userInput[4:], None)

    elif userInput.startswith('catch '):
        splitInput = re.split(r'[\s-.]+', userInput[6:])
        mon = ' '.join(word for word in splitInput[:-1])

        response = await calculateCatchRate(mon, splitInput[-1])

    elif userInput.startswith('moves '):
        splitInput = re.split(r'[\s-.]+', userInput[6:])
        mon = ' '.join(word for word in splitInput[:-1])

        response = await showMoveSet(mon, splitInput[-1])

    elif userInput.startswith('add-nickname '):
        splitInput = re.split(r'[,]+', userInput[13:])
        if len(splitInput) == 2:
            response = await addNickname(splitInput[0], splitInput[1])
        else:
            response = 'Invalid input! Use commas \',\' in between values!'

    elif userInput == 'nicknames':
        response = await seeNicknames()

    elif userInput == 'reset':
        response = resetFocus()

    elif userInput == 'rare-candies':
        response = await makeRareCandiesEmbed()

    else:
        response = 'Command not recognized. Try using ```$sl help```'

    return response