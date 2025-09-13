mcFileLocations = {
    'ServerPort': 'text_files/minecraft_server/serverPort.txt',
    'RconIp': 'text_files/minecraft_server/rconIp.txt',
    'RconPort': 'text_files/minecraft_server/rconPort.txt',
    'RconPassword': 'text_files/minecraft_server/rconPassword.txt',
    'GoogleDrive': 'text_files/minecraft_server/googleDriveLink.txt',
    'ModInfo': 'text_files/minecraft_server/modInfo.txt',
    'Moai': 'text_files/minecraft_server/moai.txt',
    'Boats': 'text_files/minecraft_server/boats.txt'
}

mcImagePaths = {
    'AmberShuckle': 'https://i.imgur.com/oC02eDj.png',
    'ShinyAmberShuckle': 'https://i.imgur.com/Np0NjY2.png'
}

dimensions = [
    {'Name': 'Overworld', 'CmdName': 'minecraft:overworld'}, 
    {'Name': 'Nether', 'CmdName': 'minecraft:the_nether'}, 
    {'Name': 'End', 'CmdName': 'minecraft:the_end'},
    {'Name': 'Anu\'s Lair', 'CmdName': 'fossil:anu_lair'}
]

defaultModifiers = {
    'Dimension': 'minecraft:overworld',
    'XCoordinate': 0,
    'ZCoordinate': 0,

    'GridSearch': False,
    'GridRange': 250,

    'SearchFor': 'biome',
    'Target': ''
}