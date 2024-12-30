""" 
Contains the functions relating to the Minecraft Server

Cole Anderson, Dec 2024
"""

import discord
from rcon.source import Client

with open('text_files/minecraft_server/serverIp.txt', 'r') as file:
    serverIp = file.read()

with open('text_files/minecraft_server/rconIp.txt', 'r') as file:
    rconIp = file.read()

with open('text_files/minecraft_server/rconPort.txt', 'r') as file:
    rconPort = int(file.read())

with open('text_files/minecraft_server/rconPassword.txt', 'r') as file:
    rconPassword = file.read()

def mcHelp():
    return ""

def mcSay(message):
    with Client(rconIp, rconPort, passwd=rconPassword) as client:
        response = client.run(f'say {message}')

    print(response)

    return response