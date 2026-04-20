import json
import regex as re
import random
import aiohttp
from diskcache import Cache
from PIL import Image
from io import BytesIO
from datetime import datetime
import math
import discord
import copy
from dictionaries.shared_dictionaries import sharedFileLocations, reactionEmojis, types, pogoCPMultipliers, sharedEmbedColours

pokeApiCache = Cache('./cache/poke_api')

#region file load save
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
#endregion

pokemon = loadDataVariableFromFile(sharedFileLocations.get('Pokemon'))

pogoPokemon = loadDataVariableFromFile(sharedFileLocations.get('PoGoPokemon'))

#region poke api
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
#endregion

#region misc commands
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

def assignReactionEmoji(command):
    return rollForShiny(reactionEmojis.get(command).get('Normal'), reactionEmojis.get(command).get('Shiny'))

def loadShucklePersonality(variant):
    with open(f'text_files/chat_gpt_instructions/{variant}Shuckle.txt', 'r') as file:
        systemContent = file.read()

    return systemContent

def addPaginatedEmbedFields(fieldTitle, fieldContent, embed, embeds, extraEmbedData=None):
    for title, content in zip(fieldTitle, fieldContent):
        embed.add_field(name=title,
                        value=content,
                        inline=True)
    
    if extraEmbedData is not None:
        embeds.append((copy.deepcopy(embed), extraEmbedData[0], extraEmbedData[1], extraEmbedData[2]))
    else:
        embeds.append(copy.deepcopy(embed))

    embed.clear_fields()

    return embed, embeds
#endregion

#region text formatting
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
#endregion

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

#region nicknames and searching pokemon file
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

def getMon(dexNum):
    try:
        return [obj for obj in pokemon if obj['DexNum'] == dexNum][0]
    except:
        return None

def getMonName(dexNum):
    try:
        mon = [obj for obj in pokemon if obj['DexNum'] == dexNum][0]['Name']
        return formatTextForDisplay(mon)
    except:
        return None
    
def buildNicknameLookupTable():
    global nicknameLookup

    nicknameLookup = {}
    for mon in pokemon:
        baseName = mon['Name']
        nicknameLookup[baseName] = baseName
        for nickname in mon['Nicknames']:
            nicknameLookup[nickname] = baseName

buildNicknameLookupTable()
#endregion

#region PoGo stats
def pogoRound(num, decimalPlaces=0):
    multiplier = 10 ** decimalPlaces
    return math.floor(num * multiplier + 0.5) / multiplier

def calcPoGoStat(baseStat, iv, cpMultiplier):
    calculatedStat = (baseStat + iv)*cpMultiplier

    return calculatedStat

def getPoGoCPMultiplier(level):
    return pogoCPMultipliers.get(level, 0)

def calcPoGoCP(attack, defence, stamina):
    cp = max(10, math.floor((attack*(defence**0.5)*(stamina**0.5))/10))
    return cp

def calcPoGoStatsFromBaseStats(hp, attack, defence, spAttack, spDefence, speed, nerfAmount=None):

    staminaGo = math.floor((1.75*hp) + 50)
    attackScaled = pogoRound(((7/4)*max(attack, spAttack)) + ((1/4)*min(attack, spAttack)))
    defenceScaled = pogoRound(((5/4)*max(defence, spDefence)) + ((3/4)*min(defence, spDefence)))

    speedMult = ((speed-75)/500) + 1

    attackGo = pogoRound(attackScaled * speedMult)
    defenceGo = pogoRound(defenceScaled * speedMult)

    if nerfAmount is None:
        cpMultiplier = getPoGoCPMultiplier(40)
        lv40CP = calcPoGoCP(calcPoGoStat(attackGo, 15, cpMultiplier),
                            calcPoGoStat(defenceGo, 15, cpMultiplier),
                            calcPoGoStat(staminaGo, 15, cpMultiplier))
        if lv40CP >= 4000:
            nerfAmount = 0.91
        else:
            nerfAmount = 1.00

    staminaNerfed = pogoRound(staminaGo * nerfAmount)
    attackNerfed = pogoRound(attackGo * nerfAmount)
    defenceNerfed = pogoRound(defenceGo * nerfAmount)

    return attackNerfed, defenceNerfed, staminaNerfed, nerfAmount
#endregion

#region PoGo mon registry
def checkDuplicatePoGoMon(monName):
    monName = formatTextForBackend(monName)

    if len([obj for obj in pogoPokemon if obj['Name'] == monName]) >= 1:
        return True
    return False

async def pogoAddMon(monName, attack, defence, stamina):
    monName = checkForNickname(monName)

    if checkDuplicatePoGoMon(monName):
        return 'That pokemon is already registered!'

    if (1000 < attack or attack <= 0) or (1000 < defence or defence <= 0) or (1000 < stamina or stamina <= 0):
        return 'Make sure the stats are greater than 0 or less than 1000!'
    
    dexNum = getDexNum(monName)

    if dexNum == -1:
        return f'The pokemon \'{formatTextForDisplay(monName)}\' was not recognized!'

    pogoPokemon.append({
        'Name': monName,
        'ImageDexNum': dexNum,
        'Attack': attack,
        'Defence': defence,
        'Stamina': stamina,
        'Moves': []
    })

    await saveDataVariableToFile(sharedFileLocations.get('PoGoPokemon'), pogoPokemon)

    return f'Pokemon \'{formatTextForDisplay(monName)}\' added successfully!'

async def pogoDeleteMon(monName):
    monName = checkForNickname(monName)

    if not checkDuplicatePoGoMon(monName):
        return 'That pokemon is not even registered yet!'

    for mon in pogoPokemon:
        if mon['Name'] == monName:
            pogoPokemon.remove(mon)
            break

    await saveDataVariableToFile(sharedFileLocations.get('PoGoPokemon'), pogoPokemon)

    return 'Mon deleted successfully!'

async def pogoListMons():
    embeds = []

    embed = discord.Embed(title=f'Registered Pokemon',
                            description='',
                            color=sharedEmbedColours.get('Default'))
    
    fieldTitles = ('Mon', 'Stats')
    fieldContent = ['', '']
    pageCount = 15

    for i, mon in enumerate(pogoPokemon, start=1):
        fieldContent[0] += f'{formatTextForDisplay(mon["Name"])}\n'
        fieldContent[1] += f'{mon["Attack"]} | {mon["Defence"]} | {mon["Stamina"]}\n'
        
        if i % pageCount == 0:
            embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
            fieldContent = ['', '']
    
    if fieldContent[0] != '':
        embed, embeds = addPaginatedEmbedFields(fieldTitles, fieldContent, embed, embeds)
    
    return embeds
#endregion