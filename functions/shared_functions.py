import json
import regex as re
import random
import aiohttp
from diskcache import Cache
from PIL import Image
from io import BytesIO
from datetime import datetime
from dictionaries.shared_dictionaries import sharedFileLocations, reactionEmojis, types

pokeApiCache = Cache('./cache/poke_api')

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

pokemon = loadDataVariableFromFile(sharedFileLocations.get('Pokemon'))

async def getPokeApiJsonData(url, session=None):
    if '/pokemon/' in url:
        label = 'pokemon'
    elif '/pokemon-species/' in url:
        label = 'species'
    elif '/move/' in url:
        label = 'move'
    elif '/machine/' in url:
        label = 'tm'
    else:
        return None
    
    cacheKey = f'{label}:{url.lower().replace("https://pokeapi.co/api/v2/", "")}'

    if cacheKey in pokeApiCache:
        return pokeApiCache[cacheKey]
    
    try:
        if session is None:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()

                    data = await response.json()
                
        else:
            async with session.get(url) as response:
                response.raise_for_status()

                data = await response.json()

        pokeApiCache.set(cacheKey, data, expire=86400*30)
        return data
            
    except Exception as ex:
        print(ex)
        return None

def getPokeAPISpriteUrl(dexNum, baseUrlAddition=None, extension='.png', rollShiny=True, forceShiny=False):
    baseURL = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'
    if baseUrlAddition is not None:
        baseURL += baseUrlAddition
    sprite = f'{baseURL}{dexNum}{extension}'
    shinySprite = f'{baseURL}shiny/{dexNum}{extension}'

    if forceShiny:
        return shinySprite
    if rollShiny:
        return rollForShiny(sprite, shinySprite)
    return sprite

async def getTypesFromPokeAPI(dexNum):
    monTypes = []

    try:
        if dexNum < 0:
            raise Exception
        
        monData = await getPokeApiJsonData(f'https://pokeapi.co/api/v2/pokemon/{dexNum}')

        if monData is None:
            raise Exception
        
        monTypes.append(str(monData['types'][0]['type']['name']).capitalize())
        if len(monData['types']) > 1:
            monTypes.append(str(monData['types'][1]['type']['name']).capitalize())
    except:
        monTypes.append('???')

    return monTypes

shinyDays = loadDataVariableFromFile(sharedFileLocations.get('ShinyDays'))

def rollForShiny(normal, shiny, randNum=None):
    currentDate = datetime.now().date().strftime("%m/%d")

    if currentDate in shinyDays:
        return shiny
    
    if randNum is None:
        randNum = random.randint(1, 100)
    
    if randNum == 69:
        return shiny
    return normal

async def openHttpImage(url, bigImg=True):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = BytesIO(await response.read())
                return Image.open(image_data).convert('RGBA')
    if not bigImg:
        return Image.open(f'images/evo_helpers/small_missing_no.png').convert('RGBA')
    return Image.open(f'images/evo_helpers/missing_no.png').convert('RGBA')

def loadShucklePersonality(variant):
    with open(f'text_files/chat_gpt_instructions/{variant}Shuckle.txt', 'r') as file:
        systemContent = file.read()

    return systemContent

def formatTextForBackend(text):
    formattedText = re.sub(r'\s', '-', str(text).strip().lower())
    return formattedText

def formatTextForDisplay(text):
    words = re.split(r'[\s-.]+', text)
    text = ' '.join(word.lower().capitalize() for word in words)
    return text

def formatCapitalize(text):
    text = text.lower()
    return text.capitalize()

def getTypeEmoji(type, moveCategory=None):
    category = 'Physical'
    if moveCategory is not None:
        category = moveCategory

    return f'<:_:{[obj for obj in types if obj["Name"] == type][0]["Emoji"][category]}>'

def getTypeColour(type):
    try:
        return [obj for obj in types if obj['Name'] == type][0]['Colour']
    except:
        return None
    
def verifyMoveType(moveType):
    moveType = formatCapitalize(moveType)
    temp = [obj for obj in types if obj['Name'] == moveType]
    if len(temp) == 1:
        return True
    return False

def checkForNickname(monName):
    monName = formatTextForBackend(monName)

    return nicknameLookup.get(monName)

def getMonFromName(monName):
    monName = checkForNickname(monName)

    try:
        return [obj for obj in pokemon if obj['Name'] == monName][0]
    except:
        return None

def getDexNum(monName):
    try:
        return getMonFromName(monName)['DexNum']
    except:
        return -1

def buildNicknameLookupTable():
    global nicknameLookup

    nicknameLookup = {}
    for mon in pokemon:
        baseName = mon['Name']
        nicknameLookup[baseName] = baseName
        for nickname in mon['Nicknames']:
            nicknameLookup[nickname] = baseName

buildNicknameLookupTable()

def assignReactionEmoji(command):
    return rollForShiny(reactionEmojis.get(command).get('Normal'), reactionEmojis.get(command).get('Shiny'))