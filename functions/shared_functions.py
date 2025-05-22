import json
import regex as re
from dictionaries.shared_dictionaries import sharedFileLocations, types

def loadDataVariableFromFile(filePath, readJson=True):
    with open(filePath, 'r') as file:
        if readJson:
            data = json.loads(file.read())
        else:
            data = file.read()

    return data

async def saveDataVariableToFile(filePath, content, writeJson=True):
    with open(filePath, 'w') as file:
        if writeJson:
            file.write(json.dumps(content))
        else:
            file.write(content)

async def saveAndLoadDataVariable(filePath, content, readWriteJson=True):
    await saveDataVariableToFile(filePath, content, readWriteJson)
    return loadDataVariableFromFile(filePath, readWriteJson)

def loadShucklePersonality(variant):
    with open(f'text_files/chat_gpt_instructions/{variant}Shuckle.txt', 'r') as file:
        systemContent = file.read()

    return systemContent

def formatTextForBackend(text):
    formatted_text = re.sub(r'\s', '-', str(text).strip().lower())
    return formatted_text

def formatTextForDisplay(text):
    words = re.split(r'[\s-.]+', text)
    text = ' '.join(word.capitalize() for word in words)
    return text

def formatCapitalize(text):
    text = text.lower()
    text = text.capitalize()
    return text

def verifyMoveType(moveType):
    moveType = formatCapitalize(moveType)
    temp = [obj for obj in types if obj['Name'] == moveType]
    if len(temp) == 1:
        return True
    return False

def getDexNum(monName):
    monName = formatTextForBackend(monName)
    try:
        return [obj for obj in pokemon if obj['Name'] == monName][0]['DexNum']
    except:
        return -1

def getOriginalNameFromNickname(monName):
    pokemon = loadDataVariableFromFile('text_files/shared/pokemon.txt')
        
    monName = formatTextForBackend(monName)

    try:
        dexNum = [obj for obj in pokemon if obj['Name'] == monName and obj['Nickname']][0]['DexNum']
        return [obj for obj in pokemon if obj['DexNum'] == dexNum][0]['Name']
    except:
        return None

pokemon = loadDataVariableFromFile(sharedFileLocations.get('Pokemon'))